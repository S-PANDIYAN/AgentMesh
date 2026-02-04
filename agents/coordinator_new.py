"""
Coordinator for AgentMesh Framework.
Generic orchestrator for multi-agent collaboration - domain-agnostic.
Now with autonomous agentic reasoning loop: Goal → Plan → Act → Evaluate → Refine → Repeat
With shared memory for stateful learning across iterations.
"""

from typing import List, Optional, Dict, Any
import time
from datetime import datetime

from core.models import (
    Task, AgentResponse, FinalReport, Goal, GoalReport, 
    GoalStatus, AgentReport, GoalEvaluation
)
from core.message_bus import MessageBus
from core.conflict_resolver import ConflictResolver
from core.aggregator import ReportAggregator
from core.agent_registry import AgentRegistry
from core.goal_evaluator import GoalEvaluator
from memory.shared_memory import SharedMemory, MemoryEntry


class Coordinator:
    """
    Framework Coordinator - orchestrates multi-agent collaboration.
    
    DOMAIN-AGNOSTIC: Does not know about specific agent types.
    Uses AgentRegistry to discover and delegate to specialist agents.
    """
    
    def __init__(self, message_bus: MessageBus, agent_registry: AgentRegistry, logger=None, memory: Optional[SharedMemory] = None):
        """
        Initialize the coordinator.
        
        Args:
            message_bus: Message bus for agent communication
            agent_registry: Registry of available specialist agents
            logger: Optional logger for tracking operations
            memory: Optional shared memory for stateful reasoning (auto-created if None)
        """
        self.message_bus = message_bus
        self.agent_registry = agent_registry
        self.logger = logger
        
        # Initialize conflict resolver and aggregator
        self.conflict_resolver = ConflictResolver(logger)
        self.aggregator = ReportAggregator(logger)
        
        # Initialize goal evaluator for autonomous reasoning
        self.goal_evaluator = GoalEvaluator()
        
        # Initialize shared memory for stateful learning
        self.memory = memory or SharedMemory()
        
        # Task statistics
        self.tasks_processed = 0
    
    def process_task(self, task: Task) -> FinalReport:
        """
        Process a task by delegating to specialist agents.
        FRAMEWORK-LEVEL: Works with any registered agents.
        
        Args:
            task: Task to process
            
        Returns:
            FinalReport with aggregated results
        """
        start_time = time.time()
        
        if self.logger:
            self.logger.log_task_received(task.task_id, task.description)
        
        # Step 1: Select agents using registry (automatic capability matching)
        selected_agents = self._select_agents_from_registry(task)
        
        if self.logger:
            self.logger.log_task_decomposed(task.task_id, len(selected_agents))
        
        # Step 2: Delegate to selected agents
        agent_responses = self._delegate_to_agents(task, selected_agents)
        
        # Step 3: Check for conflicts
        conflicts_resolved = []
        if self.conflict_resolver.detect_conflicts(agent_responses):
            conflict_record = self.conflict_resolver.resolve(
                agent_responses,
                conflict_domain=self._determine_conflict_domain(task)
            )
            conflicts_resolved.append(conflict_record)
        
        # Step 4: Aggregate results
        processing_time = time.time() - start_time
        final_report = self.aggregator.aggregate(
            task_id=task.task_id,
            agent_responses=agent_responses,
            conflicts_resolved=conflicts_resolved,
            processing_time=processing_time
        )
        
        self.tasks_processed += 1
        
        return final_report
    
    def process_goal(self, goal: Goal) -> GoalReport:
        """
        Process a goal using autonomous agentic reasoning loop.
        
        Architecture: Goal → Plan → Act → Evaluate → Refine → Repeat
        
        This method transforms the single-pass task processing into an iterative
        refinement loop that continues until the goal is achieved or stopping
        conditions are met.
        
        Args:
            goal: Goal to achieve with success criteria
            
        Returns:
            GoalReport with final results and goal achievement status
        """
        if self.logger:
            self.logger.info(f"🎯 Starting goal-driven processing: {goal.description[:100]}")
        
        # Start the goal
        goal.start()
        
        # Convert goal to task for agent processing
        base_task = self._goal_to_task(goal)
        
        start_time = time.time()
        
        # Main agentic loop: Plan → Act → Evaluate → Refine → Repeat
        while goal.should_continue():
            iteration = goal.current_iteration
            
            if self.logger:
                self.logger.info(f"🔄 Iteration {iteration}/{goal.max_iterations}")
            
            # MEMORY: Retrieve context from previous iterations
            memory_context = self.memory.get_context(goal.goal_id)
            if self.logger and memory_context['iterations'] > 0:
                self.logger.info(
                    f"💾 Memory context: {memory_context['iterations']} prev iterations, "
                    f"last confidence: {memory_context.get('last_confidence', 0):.2f}"
                )
            
            # PLAN: Select agents based on current goal state, previous evaluations, and memory
            agents = self._plan_agent_selection(goal, base_task, iteration, memory_context)
            
            if self.logger:
                agent_names = [a.__class__.__name__ for a in agents]
                self.logger.info(f"📋 Selected agents: {', '.join(agent_names)}")
            
            # ACT: Delegate to selected agents (with memory context available)
            agent_responses = self._delegate_to_agents(base_task, agents)
            
            # Store agent responses for this iteration
            goal.agent_responses_history.append(agent_responses)
            
            # Convert to AgentReport format for evaluation
            agent_reports = self._convert_to_agent_reports(agent_responses)
            
            # EVALUATE: Assess goal achievement and generate refinement suggestions
            evaluation = self.goal_evaluator.evaluate_goal(goal, agent_reports, iteration)
            goal.add_evaluation(evaluation)
            
            # MEMORY: Store iteration results in shared memory
            memory_entry = MemoryEntry(
                goal_id=goal.goal_id,
                iteration=iteration,
                timestamp=datetime.now(),
                agent_outputs=[{
                    'agent_id': resp.agent_id,
                    'agent_type': resp.agent_type.value,
                    'confidence': resp.confidence,
                    'decision': resp.recommendations[0] if resp.recommendations else None,
                    'findings_count': len(resp.findings)
                } for resp in agent_responses],
                conflicts=[{
                    'type': 'decision_disagreement',
                    'agents': list(set(resp.agent_id for resp in agent_responses))
                }] if evaluation.conflicts_detected > 0 else [],
                confidence_score=evaluation.confidence_score,
                refinements=evaluation.refinement_suggestions,
                insights={
                    'consensus_reached': evaluation.consensus_reached,
                    'agent_agreement_score': evaluation.agent_agreement_score,
                    'goal_achieved': evaluation.goal_achieved
                }
            )
            self.memory.store(memory_entry)
            
            if self.logger:
                self.logger.info(
                    f"📊 Evaluation - Achieved: {evaluation.goal_achieved}, "
                    f"Confidence: {evaluation.confidence_score:.2f}, "
                    f"Conflicts: {evaluation.conflicts_detected}, "
                    f"Consensus: {evaluation.consensus_reached}"
                )
            
            # MEMORY: Check for repeated patterns
            if self.memory.has_repeated_conflicts(goal.goal_id):
                if self.logger:
                    self.logger.warning("⚠️  Detected repeated conflicts - may need strategy change")
                # Add insight about repeated conflicts
                self.memory.add_insight(goal.goal_id, 'repeated_conflicts_detected', True)
            
            # Check stopping conditions
            should_stop, reason = self.goal_evaluator.should_stop(goal, evaluation)
            
            if should_stop:
                if self.logger:
                    self.logger.info(f"🛑 Stopping: {reason}")
                
                # Mark goal as complete (achieved or failed based on evaluation)
                if evaluation.goal_achieved:
                    goal.complete(success=True)
                else:
                    goal.complete(success=False)
                break
            
            # REFINE: Apply refinement strategies for next iteration
            if evaluation.refinement_suggestions:
                self._apply_refinements(goal, evaluation)
            
            # Increment iteration counter
            goal.current_iteration += 1
        
        # Final aggregation
        processing_time = time.time() - start_time
        
        # Get all agent responses from all iterations
        all_responses = [resp for iteration_resps in goal.agent_responses_history 
                        for resp in iteration_resps]
        
        # Resolve conflicts across all iterations
        conflicts_resolved = self.conflict_resolver.resolve_conflicts(
            all_responses,
            base_task.task_id
        )
        
        # Aggregate final report
        final_report = self.aggregator.aggregate(
            task_id=base_task.task_id,
            agent_responses=all_responses,
            conflicts_resolved=conflicts_resolved,
            processing_time=processing_time
        )
        
        # Create goal report
        goal_report = GoalReport(
            task_id=base_task.task_id,
            description=goal.description,
            findings=final_report.findings,
            recommendations=final_report.recommendations,
            confidence_score=final_report.confidence_score,
            conflicts_detected=final_report.conflicts_detected,
            conflicts_resolved=conflicts_resolved,
            agent_responses=all_responses,
            processing_time=processing_time,
            # Goal-specific fields
            goal_id=goal.goal_id,
            goal_status=goal.status,
            iterations_completed=goal.current_iteration,
            goal_achieved=goal.status == GoalStatus.ACHIEVED,
            success_criteria_met=goal.get_latest_evaluation().goal_achieved if goal.evaluation_history else False,
            evaluation_history=goal.evaluation_history,
            refinement_history=goal.refinement_history
        )
        
        self.tasks_processed += 1
        
        if self.logger:
            status_emoji = "✅" if goal_report.goal_achieved else "❌"
            self.logger.info(
                f"{status_emoji} Goal completed - Status: {goal.status.value}, "
                f"Iterations: {goal.current_iteration}, Time: {processing_time:.2f}s"
            )
        
        return goal_report
    
    def _goal_to_task(self, goal: Goal) -> Task:
        """Convert Goal to Task for agent processing."""
        return Task(
            task_id=goal.goal_id,
            description=goal.description,
            payload={}  # Could be extended to include goal-specific data
        )
    
    def _plan_agent_selection(self, goal: Goal, task: Task, iteration: int, memory_context: Dict[str, Any] = None) -> List:
        """
        Plan agent selection based on goal state, evaluation history, and memory.
        
        Refinement strategies:
        - First iteration: Use standard auto-selection
        - Subsequent iterations: Adjust based on evaluation feedback and memory
          * Low confidence → Add more specialized agents
          * Conflicts → Include conflict resolution specialists
          * Missing required types → Add required agent types
          * Repeated conflicts → Try different agent combinations
          * Learn from similar successful goals in memory
        """
        # Start with base agent selection
        agents = self._select_agents_from_registry(task)
        
        if iteration > 1 and goal.evaluation_history:
            latest_eval = goal.get_latest_evaluation()
            
            # MEMORY: Learn from successful refinements in this goal
            if memory_context and memory_context.get('iterations', 0) > 0:
                successful_refinements = self.memory.get_successful_refinements(goal.goal_id)
                if successful_refinements and self.logger:
                    self.logger.info(f"💡 Learning from {len(successful_refinements)} successful refinements")
            
            # MEMORY: Check if conflicts are repeating
            if memory_context and self.memory.has_repeated_conflicts(goal.goal_id):
                if self.logger:
                    self.logger.info("🔄 Repeated conflicts detected - trying different agent mix")
                # Shuffle agent selection to break the pattern
                all_agents = self.agent_registry.get_all_agents()
                if len(all_agents) > len(agents):
                    # Try agents we haven't used much
                    unused_agents = [a for a in all_agents if a not in agents]
                    if unused_agents:
                        agents = agents[:1] + unused_agents[:2]  # Keep one original, add two new
            
            # Low confidence: Try to add more agents
            if latest_eval.confidence_score < goal.success_criteria.min_confidence:
                # Get all available agents and add ones not yet used
                all_agents = self.agent_registry.get_all_agents()
                current_agent_types = {type(a).__name__ for a in agents}
                
                for agent in all_agents:
                    if type(agent).__name__ not in current_agent_types:
                        agents.append(agent)
                        if self.logger:
                            self.logger.info(f"➕ Adding agent for deeper analysis: {type(agent).__name__}")
                        break  # Add one at a time
            
            # Conflicts detected: Ensure diverse agent types
            if latest_eval.conflicts_detected > goal.success_criteria.max_conflicts:
                # Already handled by having multiple agents, but could add conflict specialists
                pass
            
            # Check for required agent types
            if goal.success_criteria.required_agent_types:
                current_types = {a.get_agent_type() for a in agents}
                for required_type in goal.success_criteria.required_agent_types:
                    if required_type not in current_types:
                        # Try to find an agent of this type
                        all_agents = self.agent_registry.get_all_agents()
                        for agent in all_agents:
                            if agent.get_agent_type() == required_type:
                                agents.append(agent)
                                if self.logger:
                                    self.logger.info(f"➕ Adding required agent type: {required_type.value}")
                                break
        
        return agents
    
    def _convert_to_agent_reports(self, agent_responses: List[AgentResponse]) -> List[AgentReport]:
        """Convert AgentResponse objects to AgentReport format for evaluation."""
        reports = []
        for response in agent_responses:
            report = AgentReport(
                agent_name=response.agent_id,
                agent_type=response.agent_type,
                confidence=response.confidence,
                findings=response.findings,
                decision=response.recommendations[0] if response.recommendations else None
            )
            reports.append(report)
        return reports
    
    def _apply_refinements(self, goal: Goal, evaluation: GoalEvaluation):
        """
        Apply refinement strategies based on evaluation feedback.
        
        This method tracks refinement application but actual adjustments
        happen in _plan_agent_selection for next iteration.
        """
        if self.logger:
            self.logger.info(f"🔧 Applying {len(evaluation.refinement_suggestions)} refinements")
        
        for suggestion in evaluation.refinement_suggestions:
            goal.refine(suggestion)
            if self.logger:
                self.logger.info(f"   • {suggestion}")
    
    def _select_agents_from_registry(self, task: Task) -> List:
        """
        Select agents from registry using automatic capability matching.
        DOMAIN-AGNOSTIC: Uses registry's auto-selection based on capabilities.
        
        Args:
            task: Task to analyze
            
        Returns:
            List of selected agents
        """
        # Combine task description and content for keyword matching
        # Extract code from payload if present, otherwise use empty string
        code_content = task.payload.get('code', '') if task.payload else ''
        task_text = task.description + " " + code_content
        
        # Use registry's auto-selection (or get all if none match)
        selected_agents = self.agent_registry.auto_select_agents(task_text)
        
        return selected_agents
    
    def _delegate_to_agents(self, task: Task, agents: List) -> List[AgentResponse]:
        """
        Delegate task to multiple agents.
        FRAMEWORK-LEVEL: Works with any agent that has process() method.
        
        Args:
            task: Task to delegate
            agents: List of specialist agents from registry
            
        Returns:
            List of agent responses
        """
        responses = []
        
        for agent in agents:
            if self.logger:
                self.logger.log_agent_assigned(agent.agent_id, task.task_id)
                self.logger.log_agent_started(agent.agent_id)
            
            try:
                # Generic delegation - just calls process()
                response = agent.process(task)
                responses.append(response)
                
                if self.logger:
                    self.logger.log_agent_completed(
                        agent.agent_id,
                        len(response.findings),
                        response.confidence
                    )
            
            except Exception as e:
                if self.logger:
                    self.logger.log_agent_failed(agent.agent_id, str(e))
                print(f"Warning: Agent {agent.agent_id} failed: {e}")
        
        return responses
    
    def _determine_conflict_domain(self, task: Task) -> str:
        """
        Determine conflict domain for resolution.
        Uses generic task analysis.
        
        Args:
            task: Task being processed
            
        Returns:
            Domain identifier
        """
        # Generic domain determination - can be overridden
        return "general"
    
    def get_statistics(self) -> dict:
        """
        Get coordinator statistics.
        
        Returns:
            Dictionary of statistics
        """
        return {
            'tasks_processed': self.tasks_processed,
            'registered_agents': self.agent_registry.get_agent_count(),
            'agent_types': [t.value for t in self.agent_registry.get_agent_types()]
        }
