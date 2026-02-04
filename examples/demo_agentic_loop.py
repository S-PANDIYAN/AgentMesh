"""
Demonstration of AgentMesh Agentic Loop (Goal-Driven Processing)
=================================================================

This demo shows the autonomous agentic reasoning loop in action:
Goal → Plan → Act → Evaluate → Refine → Repeat

The demo compares:
1. Single-pass task processing (traditional)
2. Multi-iteration goal-driven processing (agentic)

Watch how the system:
- Starts with initial agents
- Evaluates confidence and conflicts
- Refines agent selection based on evaluation
- Iterates until goal is achieved or stopping conditions met
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.models import (
    Goal, GoalStatus, SuccessCriteria, Task, AgentType
)
from core.message_bus import MessageBus
from core.agent_registry import AgentRegistry
from agents.coordinator_new import Coordinator
from agents.security_agent import SecurityAgent
from agents.performance_agent import PerformanceAgent
from agents.maintainability_agent import MaintainabilityAgent
from utils.logger import AgentMeshLogger

# Initialize logger
logger = AgentMeshLogger.get_logger("AgenticDemo")


def print_section(title: str):
    """Print formatted section header."""
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80 + "\n")


def print_evaluation(iteration: int, evaluation):
    """Print evaluation results."""
    print(f"\n📊 Iteration {iteration} Evaluation:")
    print(f"   • Goal Achieved: {evaluation.goal_achieved}")
    print(f"   • Confidence: {evaluation.confidence_score:.2%}")
    print(f"   • Conflicts: {evaluation.conflicts_detected}")
    print(f"   • Consensus: {evaluation.consensus_reached}")
    print(f"   • Agent Agreement: {evaluation.agent_agreement_score:.2%}")
    print(f"   • Findings: {evaluation.findings_count}")
    
    if evaluation.refinement_suggestions:
        print(f"\n   🔧 Refinement Suggestions:")
        for suggestion in evaluation.refinement_suggestions:
            print(f"      - {suggestion}")


def demo_single_pass_processing():
    """Demonstrate traditional single-pass processing."""
    print_section("PART 1: Traditional Single-Pass Processing")
    
    # Setup
    message_bus = MessageBus()
    agent_registry = AgentRegistry()
    
    # Register agents
    security_agent = SecurityAgent(message_bus, logger)
    performance_agent = PerformanceAgent(message_bus, logger)
    
    agent_registry.register_agent(security_agent, ["security", "vulnerability"])
    agent_registry.register_agent(performance_agent, ["performance", "optimization"])
    
    coordinator = Coordinator(message_bus, agent_registry, logger)
    
    # Create task
    code = """
def process_data(data):
    result = []
    for item in data:
        # Process each item
        processed = item * 2
        result.append(processed)
    return result
"""
    
    task = Task(
        task_id="demo-task-1",
        description="Review this data processing function",
        task_type="code_review",
        payload={"code": code}
    )
    
    print("📝 Task: Review data processing function")
    print(f"   Agents: {len(agent_registry.get_all_agents())}")
    print("\n⏱️  Processing...")
    
    # Process (single pass)
    report = coordinator.process_task(task)
    
    print(f"\n✅ Completed in {report.processing_time:.2f}s")
    print(f"   Decision: {report.decision}")
    print(f"   Confidence: {report.confidence_score:.2%}")
    print(f"   Findings: {len(report.findings)}")
    print(f"   Conflicts: {len(report.conflicts_resolved)}")
    
    print("\n💡 Limitation: Single-pass processing cannot refine based on results")
    print("   If confidence is low or conflicts exist, no automatic refinement occurs.")
    
    return report


def demo_agentic_loop_simple():
    """Demonstrate agentic loop with simple goal (achieves quickly)."""
    print_section("PART 2: Agentic Loop - Simple Goal (Quick Success)")
    
    # Setup
    message_bus = MessageBus()
    agent_registry = AgentRegistry()
    
    # Register agents
    security_agent = SecurityAgent(message_bus, logger)
    performance_agent = PerformanceAgent(message_bus, logger)
    
    agent_registry.register_agent(security_agent, ["security"])
    agent_registry.register_agent(performance_agent, ["performance"])
    
    coordinator = Coordinator(message_bus, agent_registry, logger)
    
    # Create goal with relaxed criteria
    code = """
def calculate_total(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
"""
    
    criteria = SuccessCriteria(
        min_confidence=0.75,  # Relaxed threshold
        max_conflicts=0,
        require_consensus=False
    )
    
    goal = Goal(
        goal_id="demo-goal-simple",
        description="Review this simple calculation function",
        success_criteria=criteria,
        max_iterations=5,
        task_type="code_review",
        payload={"code": code}
    )
    
    print("🎯 Goal: Review simple calculation function")
    print(f"   Success Criteria:")
    print(f"      - Min Confidence: {criteria.min_confidence:.0%}")
    print(f"      - Max Conflicts: {criteria.max_conflicts}")
    print(f"      - Require Consensus: {criteria.require_consensus}")
    print(f"   Max Iterations: {goal.max_iterations}")
    
    print("\n🔄 Starting agentic loop...")
    
    # Process with agentic loop
    report = coordinator.process_goal(goal)
    
    print(f"\n{'✅' if report.goal_achieved else '❌'} Goal Status: {report.goal_status.value}")
    print(f"   Iterations: {report.iterations_completed}")
    print(f"   Time: {report.processing_time:.2f}s")
    print(f"   Final Confidence: {report.confidence_score:.2%}")
    
    # Show evaluation history
    print(f"\n📈 Evaluation History ({len(report.evaluation_history)} iterations):")
    for eval in report.evaluation_history:
        print_evaluation(eval.iteration, eval)
    
    print("\n💡 Result: Simple goal achieved quickly with initial agents")
    
    return report


def demo_agentic_loop_complex():
    """Demonstrate agentic loop with complex goal (requires refinement)."""
    print_section("PART 3: Agentic Loop - Complex Goal (Iterative Refinement)")
    
    # Setup
    message_bus = MessageBus()
    agent_registry = AgentRegistry()
    
    # Register all agents (more available for refinement)
    security_agent = SecurityAgent(message_bus, logger)
    performance_agent = PerformanceAgent(message_bus, logger)
    maintainability_agent = MaintainabilityAgent(message_bus, logger)
    
    agent_registry.register_agent(security_agent, ["security", "vulnerability"])
    agent_registry.register_agent(performance_agent, ["performance", "optimization"])
    agent_registry.register_agent(maintainability_agent, ["maintainability", "code quality"])
    
    coordinator = Coordinator(message_bus, agent_registry, logger)
    
    # Create goal with high standards
    code = """
def process_user_input(user_data):
    # Process user input without validation
    processed = []
    for item in user_data:
        # Multiple nested loops - O(n^3) complexity
        for i in range(len(item)):
            for j in range(len(item)):
                result = item[i] + item[j]
                processed.append(result)
    return processed
"""
    
    criteria = SuccessCriteria(
        min_confidence=0.85,  # High threshold
        max_conflicts=0,
        require_consensus=True,  # All agents must agree
        required_agent_types=[AgentType.SECURITY, AgentType.PERFORMANCE]
    )
    
    goal = Goal(
        goal_id="demo-goal-complex",
        description="Thoroughly review this user input processing function",
        success_criteria=criteria,
        max_iterations=5,
        task_type="code_review",
        payload={"code": code}
    )
    
    print("🎯 Goal: Thoroughly review user input processing")
    print(f"   Success Criteria:")
    print(f"      - Min Confidence: {criteria.min_confidence:.0%}")
    print(f"      - Max Conflicts: {criteria.max_conflicts}")
    print(f"      - Require Consensus: {criteria.require_consensus}")
    print(f"      - Required Agent Types: {[t.value for t in criteria.required_agent_types]}")
    print(f"   Max Iterations: {goal.max_iterations}")
    print(f"   Available Agents: {len(agent_registry.get_all_agents())}")
    
    print("\n🔄 Starting agentic loop...")
    print("   Expect multiple iterations due to:")
    print("      • Complex code with security issues")
    print("      • Performance problems")
    print("      • High confidence threshold")
    print("      • Consensus requirement")
    
    # Process with agentic loop
    report = coordinator.process_goal(goal)
    
    print(f"\n{'✅' if report.goal_achieved else '❌'} Goal Status: {report.goal_status.value}")
    print(f"   Iterations: {report.iterations_completed}/{goal.max_iterations}")
    print(f"   Time: {report.processing_time:.2f}s")
    print(f"   Final Confidence: {report.confidence_score:.2%}")
    
    # Show evaluation history with progression
    print(f"\n📈 Evaluation Progression ({len(report.evaluation_history)} iterations):")
    for eval in report.evaluation_history:
        print_evaluation(eval.iteration, eval)
    
    # Show refinement history
    if report.refinement_history:
        print(f"\n🔧 Refinements Applied ({len(report.refinement_history)} total):")
        for i, refinement in enumerate(report.refinement_history, 1):
            print(f"   {i}. {refinement}")
    
    # Show confidence progression
    if len(report.evaluation_history) > 1:
        print("\n📊 Confidence Progression:")
        for eval in report.evaluation_history:
            bar_length = int(eval.confidence_score * 40)
            bar = "█" * bar_length + "░" * (40 - bar_length)
            print(f"   Iteration {eval.iteration}: {bar} {eval.confidence_score:.1%}")
    
    print("\n💡 Result: Complex goal required multiple iterations and refinements")
    print("   The agentic loop:")
    print("      1. Detected issues (low confidence, conflicts)")
    print("      2. Generated refinement suggestions")
    print("      3. Adjusted agent selection")
    print("      4. Re-evaluated until criteria met or max iterations")
    
    return report


def demo_comparison():
    """Compare single-pass vs agentic approaches."""
    print_section("PART 4: Comparison - Single-Pass vs Agentic Loop")
    
    comparison_table = """
┌────────────────────────────┬─────────────────────┬──────────────────────┐
│ Feature                    │ Single-Pass         │ Agentic Loop         │
├────────────────────────────┼─────────────────────┼──────────────────────┤
│ Iterations                 │ 1 (fixed)           │ 1-N (adaptive)       │
│ Refinement                 │ None                │ Automatic            │
│ Confidence Handling        │ Accept as-is        │ Improve iteratively  │
│ Conflict Resolution        │ One-time            │ Multi-pass           │
│ Agent Selection            │ Static              │ Dynamic/Refined      │
│ Goal Achievement           │ N/A                 │ Tracked & Verified   │
│ Stopping Conditions        │ After 1 pass        │ Multiple criteria    │
│ Convergence                │ No                  │ Yes                  │
│ Quality Assurance          │ Manual              │ Built-in             │
│ Use Case                   │ Simple reviews      │ Complex analysis     │
└────────────────────────────┴─────────────────────┴──────────────────────┘
"""
    
    print(comparison_table)
    
    print("\n🎯 When to Use Each Approach:")
    print("\n   Single-Pass Processing:")
    print("      • Simple, straightforward tasks")
    print("      • Time-sensitive operations")
    print("      • Low complexity requirements")
    print("      • Quick feedback needed")
    
    print("\n   Agentic Loop (Goal-Driven):")
    print("      • Complex analysis requiring thoroughness")
    print("      • High confidence requirements")
    print("      • Critical decisions (security, compliance)")
    print("      • Quality must be verified")
    print("      • Willing to trade time for accuracy")


def main():
    """Run all demonstrations."""
    print("\n" + "█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + "  AgentMesh Agentic Loop Demonstration".center(78) + "█")
    print("█" + "  Autonomous Goal-Driven Multi-Agent Processing".center(78) + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80)
    
    try:
        # Part 1: Single-pass
        demo_single_pass_processing()
        input("\n⏸️  Press Enter to continue to Part 2...")
        
        # Part 2: Simple agentic goal
        demo_agentic_loop_simple()
        input("\n⏸️  Press Enter to continue to Part 3...")
        
        # Part 3: Complex agentic goal with refinement
        demo_agentic_loop_complex()
        input("\n⏸️  Press Enter to continue to Part 4...")
        
        # Part 4: Comparison
        demo_comparison()
        
        print_section("Demo Complete!")
        print("✅ Successfully demonstrated:")
        print("   1. Traditional single-pass processing")
        print("   2. Agentic loop with simple goal")
        print("   3. Agentic loop with complex goal and refinement")
        print("   4. Comparison of approaches")
        
        print("\n🎓 Key Takeaways:")
        print("   • Agentic loop provides autonomous refinement")
        print("   • System can iteratively improve confidence")
        print("   • Goals track achievement with success criteria")
        print("   • Stopping conditions prevent infinite loops")
        print("   • Trade-off: More iterations = Higher quality + More time")
        
        print("\n📚 Learn More:")
        print("   • Check README.md for architecture details")
        print("   • See tests/test_agentic_loop.py for test coverage")
        print("   • Review core/goal_evaluator.py for evaluation logic")
        print("   • Explore agents/coordinator_new.py for loop implementation")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
