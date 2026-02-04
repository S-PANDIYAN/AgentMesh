"""
Goal Evaluator - Evaluates goal achievement and suggests refinements.
Core component of the agentic reasoning loop.
"""
from typing import List, Dict, Any, Tuple
from datetime import datetime
from core.models import (
    Goal, GoalEvaluation, AgentReport, SuccessCriteria,
    GoalStatus
)


class GoalEvaluator:
    """
    Evaluates whether a goal has been achieved and suggests refinements.
    
    This is the "Evaluate" step in the Goal → Plan → Act → Evaluate → Refine loop.
    """
    
    def __init__(self):
        """Initialize the goal evaluator."""
        self.evaluation_history = []
    
    def evaluate_goal(
        self,
        goal: Goal,
        agent_reports: List[AgentReport],
        iteration: int
    ) -> GoalEvaluation:
        """
        Evaluate if goal is achieved based on agent reports.
        
        Args:
            goal: The goal being evaluated
            agent_reports: Reports from agents for this iteration
            iteration: Current iteration number
        
        Returns:
            GoalEvaluation with achievement status and refinement suggestions
        """
        criteria = goal.success_criteria
        
        # Calculate metrics
        confidence_score = self._calculate_confidence(agent_reports)
        conflicts_detected = self._count_conflicts(agent_reports)
        consensus_reached = self._check_consensus(agent_reports)
        agent_agreement = self._calculate_agreement(agent_reports)
        findings_count = sum(len(r.findings) for r in agent_reports)
        
        # Check success criteria
        criteria_met = self._check_success_criteria(
            criteria=criteria,
            confidence=confidence_score,
            conflicts=conflicts_detected,
            consensus=consensus_reached,
            agent_reports=agent_reports
        )
        
        # Determine if goal is achieved
        goal_achieved = all(criteria_met.values())
        
        # Generate refinement suggestions if not achieved
        refinement_suggestions = []
        stopping_reason = None
        
        if not goal_achieved:
            refinement_suggestions = self._generate_refinements(
                criteria_met=criteria_met,
                agent_reports=agent_reports,
                iteration=iteration,
                max_iterations=goal.max_iterations
            )
            
            # Determine stopping reason if applicable
            if iteration >= goal.max_iterations:
                stopping_reason = "Maximum iterations reached"
            elif not refinement_suggestions:
                stopping_reason = "No refinement strategies available"
        else:
            stopping_reason = "Success criteria met"
        
        # Create evaluation
        evaluation = GoalEvaluation(
            iteration=iteration,
            timestamp=datetime.now(),
            goal_achieved=goal_achieved,
            confidence_score=confidence_score,
            conflicts_detected=conflicts_detected,
            consensus_reached=consensus_reached,
            findings_count=findings_count,
            agent_agreement_score=agent_agreement,
            refinement_suggestions=refinement_suggestions,
            stopping_reason=stopping_reason,
            metadata={
                'criteria_met': criteria_met,
                'agent_count': len(agent_reports),
                'decision_distribution': self._get_decision_distribution(agent_reports)
            }
        )
        
        self.evaluation_history.append(evaluation)
        return evaluation
    
    def _calculate_confidence(self, agent_reports: List[AgentReport]) -> float:
        """Calculate overall confidence from agent reports."""
        if not agent_reports:
            return 0.0
        
        # Weighted average confidence
        total_confidence = sum(r.confidence for r in agent_reports)
        return total_confidence / len(agent_reports)
    
    def _count_conflicts(self, agent_reports: List[AgentReport]) -> int:
        """Count decision conflicts between agents."""
        if len(agent_reports) < 2:
            return 0
        
        decisions = [r.decision for r in agent_reports]
        unique_decisions = set(decisions)
        
        # Conflict if agents disagree
        return max(0, len(unique_decisions) - 1)
    
    def _check_consensus(self, agent_reports: List[AgentReport]) -> bool:
        """Check if all agents reached consensus."""
        if not agent_reports:
            return False
        
        decisions = [r.decision for r in agent_reports]
        return len(set(decisions)) == 1
    
    def _calculate_agreement(self, agent_reports: List[AgentReport]) -> float:
        """
        Calculate agent agreement score (0.0-1.0).
        1.0 = all agree, 0.0 = maximum disagreement
        """
        if len(agent_reports) < 2:
            return 1.0
        
        decisions = [r.decision for r in agent_reports]
        decision_counts = {}
        for decision in decisions:
            decision_counts[decision] = decision_counts.get(decision, 0) + 1
        
        # Agreement = (most common decision count) / (total agents)
        max_agreement = max(decision_counts.values())
        return max_agreement / len(agent_reports)
    
    def _check_success_criteria(
        self,
        criteria: SuccessCriteria,
        confidence: float,
        conflicts: int,
        consensus: bool,
        agent_reports: List[AgentReport]
    ) -> Dict[str, bool]:
        """
        Check each success criterion.
        
        Returns:
            Dict mapping criterion name to whether it's met
        """
        criteria_met = {}
        
        # Confidence threshold
        criteria_met['min_confidence'] = confidence >= criteria.min_confidence
        
        # Conflict limit
        criteria_met['max_conflicts'] = conflicts <= criteria.max_conflicts
        
        # Consensus requirement
        if criteria.require_consensus:
            criteria_met['consensus'] = consensus
        else:
            criteria_met['consensus'] = True  # Not required
        
        # Required agent types
        if criteria.required_agent_types:
            agent_types = {r.agent_type.value for r in agent_reports}
            required_present = all(
                req in agent_types for req in criteria.required_agent_types
            )
            criteria_met['required_agents'] = required_present
        else:
            criteria_met['required_agents'] = True
        
        # Custom checks
        for check_name, check_value in criteria.custom_checks.items():
            # Custom validation logic (extensible)
            criteria_met[f'custom_{check_name}'] = True  # Default to True
        
        return criteria_met
    
    def _generate_refinements(
        self,
        criteria_met: Dict[str, bool],
        agent_reports: List[AgentReport],
        iteration: int,
        max_iterations: int
    ) -> List[str]:
        """
        Generate refinement suggestions based on unmet criteria.
        
        Returns:
            List of refinement strategy descriptions
        """
        suggestions = []
        
        # Low confidence - need more evidence
        if not criteria_met.get('min_confidence', False):
            avg_confidence = self._calculate_confidence(agent_reports)
            suggestions.append(
                f"Increase confidence (current: {avg_confidence:.2%}). "
                "Consider adding more specialized agents or requesting deeper analysis."
            )
        
        # Too many conflicts - need resolution
        if not criteria_met.get('max_conflicts', False):
            conflicts = self._count_conflicts(agent_reports)
            suggestions.append(
                f"Resolve {conflicts} decision conflicts. "
                "Apply conflict resolution strategies or request agent reconsideration."
            )
        
        # No consensus - need alignment
        if not criteria_met.get('consensus', False):
            decisions = self._get_decision_distribution(agent_reports)
            suggestions.append(
                f"Achieve consensus (current distribution: {decisions}). "
                "Request agents to review conflicting findings."
            )
        
        # Missing required agents
        if not criteria_met.get('required_agents', False):
            agent_types = {r.agent_type.value for r in agent_reports}
            suggestions.append(
                f"Ensure all required agent types are consulted (current: {agent_types})"
            )
        
        # Add iteration-based suggestions
        if iteration == 1:
            suggestions.append("First iteration - consider expanding analysis scope")
        elif iteration >= max_iterations - 1:
            suggestions.append("Final iteration - focus on decisive evidence")
        
        # If agents found issues, suggest focusing on those
        high_severity_findings = []
        for report in agent_reports:
            high_severity_findings.extend([
                f for f in report.findings 
                if 'critical' in str(f).lower() or 'high' in str(f).lower()
            ])
        
        if high_severity_findings:
            suggestions.append(
                f"Address {len(high_severity_findings)} high-severity findings "
                "before proceeding"
            )
        
        return suggestions if suggestions else ["No specific refinements available"]
    
    def _get_decision_distribution(self, agent_reports: List[AgentReport]) -> Dict[str, int]:
        """Get distribution of agent decisions."""
        decisions = {}
        for report in agent_reports:
            decisions[report.decision] = decisions.get(report.decision, 0) + 1
        return decisions
    
    def should_stop(self, evaluation: GoalEvaluation, goal: Goal) -> Tuple[bool, str]:
        """
        Determine if goal execution should stop.
        
        Returns:
            Tuple of (should_stop, reason)
        """
        # Success - stop
        if evaluation.goal_achieved:
            return True, "Goal achieved - success criteria met"
        
        # Max iterations reached
        if evaluation.iteration >= goal.max_iterations:
            return True, f"Maximum iterations ({goal.max_iterations}) reached"
        
        # No refinement strategies available
        if not evaluation.refinement_suggestions or \
           evaluation.refinement_suggestions[0] == "No specific refinements available":
            return True, "No refinement strategies available"
        
        # Consensus reached with high confidence (early stopping)
        if evaluation.consensus_reached and evaluation.confidence_score >= 0.95:
            return True, "Strong consensus reached - early stopping"
        
        # Continue
        return False, "Continue to next iteration"
    
    def get_summary(self, goal: Goal) -> Dict[str, Any]:
        """Get summary of all evaluations for a goal."""
        if not goal.evaluation_history:
            return {'status': 'No evaluations yet'}
        
        evaluations = goal.evaluation_history
        
        return {
            'total_iterations': len(evaluations),
            'final_status': goal.status.value,
            'goal_achieved': evaluations[-1].goal_achieved,
            'final_confidence': evaluations[-1].confidence_score,
            'consensus_reached': evaluations[-1].consensus_reached,
            'confidence_progression': [e.confidence_score for e in evaluations],
            'conflicts_progression': [e.conflicts_detected for e in evaluations],
            'stopping_reason': evaluations[-1].stopping_reason,
            'refinements_applied': len(goal.refinement_history)
        }
