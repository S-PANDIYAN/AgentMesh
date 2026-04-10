"""
AgentMesh - Multi-Agent Collaboration Framework
Main entry point - Plugin-based architecture with dynamic agent loading.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

# Import framework initialization (no hardcoded agents!)
from framework_init import initialize_framework, print_framework_banner
from demo.demo_scenarios import DEMO_SCENARIOS, list_scenarios
from core.models import Task
from utils.helpers import create_separator, format_duration
from config import COLORS, PATHS
import time


def print_header():
    """Print application header."""
    print_framework_banner()


def print_menu():
    """Print main menu."""
    print("\n" + COLORS['OKBLUE'] + "═" * 70 + COLORS['ENDC'])
    print(COLORS['BOLD'] + "MAIN MENU" + COLORS['ENDC'])
    print(COLORS['OKBLUE'] + "═" * 70 + COLORS['ENDC'])
    print("1. Run Single Demo Scenario")
    print("2. Run All Demo Scenarios")
    print("3. Process Custom Code")
    print("4. View Task History")
    print("5. View System Statistics")
    print("6. Exit")
    print(COLORS['OKBLUE'] + "═" * 70 + COLORS['ENDC'])


def list_demo_scenarios():
    """Display available demo scenarios."""
    print("\n" + COLORS['OKBLUE'] + "Available Demo Scenarios:" + COLORS['ENDC'])
    print(COLORS['OKBLUE'] + "-" * 70 + COLORS['ENDC'])
    
    scenarios = list_scenarios()
    for i, scenario in enumerate(scenarios, 1):
        decision_color = {
            'APPROVE': COLORS['OKGREEN'],
            'BLOCK': COLORS['FAIL'],
            'NEEDS_REVISION': COLORS['WARNING']
        }.get(scenario['expected_decision'], COLORS['ENDC'])
        
        print(f"{i}. {scenario['name']}")
        print(f"   Expected: {decision_color}{scenario['expected_decision']}{COLORS['ENDC']}")
    
    print(COLORS['OKBLUE'] + "-" * 70 + COLORS['ENDC'])


def run_single_scenario(coordinator, history, scenario_key: str = None):
    """
    Run a single demo scenario.
    
    Args:
        coordinator: Coordinator instance
        history: Task history instance
        scenario_key: Optional specific scenario key
    """
    if scenario_key is None:
        list_demo_scenarios()
        choice = input("\nSelect scenario number (or 'q' to cancel): ").strip()
        
        if choice.lower() == 'q':
            return
        
        try:
            scenario_index = int(choice) - 1
            scenarios = list(DEMO_SCENARIOS.keys())
            scenario_key = scenarios[scenario_index]
        except (ValueError, IndexError):
            print(COLORS['FAIL'] + "Invalid selection!" + COLORS['ENDC'])
            return
    
    scenario = DEMO_SCENARIOS[scenario_key]
    
    print("\n" + COLORS['HEADER'] + "=" * 70 + COLORS['ENDC'])
    print(COLORS['BOLD'] + f"Running: {scenario['name']}" + COLORS['ENDC'])
    print(COLORS['HEADER'] + "=" * 70 + COLORS['ENDC'])
    
    # Create task
    task = Task(
        task_id=f"demo-{scenario_key}",
        description=f"Review demo code: {scenario['name']}",
        payload={'code': scenario['code']},
        task_type='code_review',
        priority='HIGH'
    )
    
    # Process task
    print("\n" + COLORS['OKBLUE'] + "Processing..." + COLORS['ENDC'])
    start_time = time.time()
    
    final_report = coordinator.process_task(task)
    
    duration = time.time() - start_time
    
    # Display results
    print("\n" + final_report.to_formatted_string())
    
    print(f"\n{COLORS['OKBLUE']}Processing time: {format_duration(duration)}{COLORS['ENDC']}")
    
    # Compare with expected
    print(f"\n{COLORS['BOLD']}Expected Decision:{COLORS['ENDC']} {scenario['expected_decision']}")
    print(f"{COLORS['BOLD']}Actual Decision:{COLORS['ENDC']} {final_report.final_decision.value}")
    
    if final_report.final_decision.value == scenario['expected_decision']:
        print(COLORS['OKGREEN'] + "✓ Matches expected result!" + COLORS['ENDC'])
    else:
        print(COLORS['WARNING'] + "⚠ Different from expected result" + COLORS['ENDC'])
    
    # Save to history
    history.add_task(task, final_report.agent_responses, final_report)


def run_all_scenarios(coordinator, history):
    """
    Run all demo scenarios.
    
    Args:
        coordinator: Coordinator instance
        history: Task history instance
    """
    print("\n" + COLORS['HEADER'] + "=" * 70 + COLORS['ENDC'])
    print(COLORS['BOLD'] + "Running All Demo Scenarios" + COLORS['ENDC'])
    print(COLORS['HEADER'] + "=" * 70 + COLORS['ENDC'])
    
    results = []
    
    for scenario_key, scenario in DEMO_SCENARIOS.items():
        print(f"\n{COLORS['OKBLUE']}Testing: {scenario['name']}{COLORS['ENDC']}")
        
        task = Task(
            task_id=f"batch-{scenario_key}",
            description=f"Batch test: {scenario['name']}",
            payload={'code': scenario['code']},
            task_type='code_review',
            priority='MEDIUM'
        )
        
        start_time = time.time()
        final_report = coordinator.process_task(task)
        duration = time.time() - start_time
        
        match = final_report.decision == scenario['expected_decision']
        results.append({
            'name': scenario['name'],
            'expected': scenario['expected_decision'],
            'actual': final_report.decision,
            'match': match,
            'findings': len(final_report.all_findings),
            'duration': duration
        })
        
        # Save to history
        history.add_task(task, final_report.agent_responses, final_report)
        
        status = COLORS['OKGREEN'] + "✓" if match else COLORS['FAIL'] + "✗"
        print(f"{status} {scenario['name']}: {final_report.decision.value}{COLORS['ENDC']}")
    
    # Summary
    print("\n" + COLORS['HEADER'] + "=" * 70 + COLORS['ENDC'])
    print(COLORS['BOLD'] + "BATCH TEST SUMMARY" + COLORS['ENDC'])
    print(COLORS['HEADER'] + "=" * 70 + COLORS['ENDC'])
    
    matches = sum(1 for r in results if r['match'])
    total = len(results)
    accuracy = (matches / total) * 100
    
    print(f"Total Scenarios: {total}")
    print(f"Correct Predictions: {matches}")
    print(f"Accuracy: {accuracy:.1f}%")
    print(f"Total Findings: {sum(r['findings'] for r in results)}")
    print(f"Total Time: {format_duration(sum(r['duration'] for r in results))}")
    
    print("\nDetailed Results:")
    for result in results:
        status_icon = "✓" if result['match'] else "✗"
        color = COLORS['OKGREEN'] if result['match'] else COLORS['FAIL']
        print(f"{color}{status_icon}{COLORS['ENDC']} {result['name']}")
        print(f"  Expected: {result['expected']} | Actual: {result['actual']}")
        print(f"  Findings: {result['findings']} | Time: {format_duration(result['duration'])}")


def process_custom_code(coordinator, history):
    """
    Process user-provided custom code.
    
    Args:
        coordinator: Coordinator instance
        history: Task history instance
    """
    print("\n" + COLORS['OKBLUE'] + "=" * 70 + COLORS['ENDC'])
    print(COLORS['BOLD'] + "Process Custom Code" + COLORS['ENDC'])
    print(COLORS['OKBLUE'] + "=" * 70 + COLORS['ENDC'])
    
    print("\nEnter your Python code to review.")
    print("Type 'END' on a new line when finished.")
    print(COLORS['OKBLUE'] + "-" * 70 + COLORS['ENDC'])
    
    lines = []
    while True:
        try:
            line = input()
            if line.strip() == 'END':
                break
            lines.append(line)
        except EOFError:
            break
    
    code = '\n'.join(lines)
    
    if not code.strip():
        print(COLORS['WARNING'] + "No code provided!" + COLORS['ENDC'])
        return
    
    # Get task description
    description = input("\nTask description (optional): ").strip()
    if not description:
        description = "Custom code review"
    
    # Create and process task
    task = Task(
        task_id="custom-" + str(int(time.time())),
        description=description,
        payload={'code': code},
        task_type='code_review',
        priority='MEDIUM'
    )
    
    print("\n" + COLORS['OKBLUE'] + "Processing..." + COLORS['ENDC'])
    start_time = time.time()
    
    final_report = coordinator.process_task(task)
    
    duration = time.time() - start_time
    
    # Display results
    print("\n" + final_report.to_formatted_string())
    print(f"\n{COLORS['OKBLUE']}Processing time: {format_duration(duration)}{COLORS['ENDC']}")
    
    # Save to history
    history.add_task(task, final_report.agent_responses, final_report)


def view_task_history(history):
    """
    Display task history.
    
    Args:
        history: Task history instance
    """
    print("\n" + COLORS['OKBLUE'] + "=" * 70 + COLORS['ENDC'])
    print(COLORS['BOLD'] + "Recent Task History" + COLORS['ENDC'])
    print(COLORS['OKBLUE'] + "=" * 70 + COLORS['ENDC'])
    
    recent = history.get_recent_tasks(limit=10)
    
    if not recent:
        print("\nNo tasks in history yet.")
        return
    
    for task in recent:
        print(f"\n{COLORS['BOLD']}Task ID:{COLORS['ENDC']} {task['task_id']}")
        print(f"Timestamp: {task['timestamp']}")
        print(f"Decision: {task['final_decision']}")
        print(f"Findings: {task['total_findings']}")
        print(f"Conflicts: {'Yes' if task['conflicts_detected'] else 'No'}")
        print(COLORS['OKBLUE'] + "-" * 70 + COLORS['ENDC'])


def view_statistics(history):
    """
    Display system statistics.
    
    Args:
        history: Task history instance
    """
    print("\n" + history.get_summary_report())


def main():
    """Main application entry point."""
    print_header()
    
    # Initialize framework (dynamic plugin loading!)
    coordinator, registry, history, logger = initialize_framework()
    
    print(COLORS['OKGREEN'] + "\n✓ Application ready - All plugins loaded!" + COLORS['ENDC'])
    print(COLORS['OKBLUE'] + f"  Registered agents: {registry.get_agent_count()}" + COLORS['ENDC'])
    
    # Main loop
    while True:
        print_menu()
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            run_single_scenario(coordinator, history)
        elif choice == '2':
            run_all_scenarios(coordinator, history)
        elif choice == '3':
            process_custom_code(coordinator, history)
        elif choice == '4':
            view_task_history(history)
        elif choice == '5':
            view_statistics(history)
        elif choice == '6':
            print("\n" + COLORS['OKGREEN'] + "Thank you for using AgentMesh!" + COLORS['ENDC'])
            break
        else:
            print(COLORS['FAIL'] + "Invalid option! Please try again." + COLORS['ENDC'])
        
        input("\n" + COLORS['OKBLUE'] + "Press Enter to continue..." + COLORS['ENDC'])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n" + COLORS['WARNING'] + "Application interrupted by user." + COLORS['ENDC'])
        sys.exit(0)
    except Exception as e:
        print(f"\n{COLORS['FAIL']}Error: {e}{COLORS['ENDC']}")
        sys.exit(1)
