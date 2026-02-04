"""
Task history management for AgentMesh.
Stores and retrieves historical task data.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import json
from pathlib import Path
from dataclasses import asdict

from core.models import Task, AgentResponse, Finding, FinalReport


class TaskHistory:
    """
    Manages historical task data for analysis and evaluation.
    """
    
    def __init__(self, storage_path: str = "./data/task_history.json"):
        """
        Initialize task history manager.
        
        Args:
            storage_path: Path to storage file
        """
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.tasks: List[Dict[str, Any]] = []
        self._load()
    
    def _load(self) -> None:
        """Load task history from file."""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    self.tasks = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load task history: {e}")
                self.tasks = []
        else:
            self.tasks = []
    
    def _save(self) -> None:
        """Save task history to file."""
        try:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.tasks, f, indent=2, default=str)
        except Exception as e:
            print(f"Error: Could not save task history: {e}")
    
    def add_task(self, task: Task, agent_responses: List[AgentResponse],
                 final_report: FinalReport, metadata: Dict[str, Any] = None) -> None:
        """
        Add a completed task to history.
        
        Args:
            task: The task that was processed
            agent_responses: All agent responses
            final_report: Final aggregated report
            metadata: Optional additional metadata
        """
        task_record = {
            'task_id': task.task_id,
            'timestamp': datetime.now().isoformat(),
            'task': {
                'description': task.description,
                'code': task.code[:500],  # Truncate for storage
                'priority': task.priority
            },
            'agents_involved': [
                {
                    'agent_type': resp.agent_type.value,
                    'decision': resp.decision.value,
                    'confidence': resp.confidence,
                    'findings_count': len(resp.findings)
                }
                for resp in agent_responses
            ],
            'final_decision': final_report.final_decision.value,
            'total_findings': len(final_report.all_findings),
            'findings_by_severity': {
                'CRITICAL': len([f for f in final_report.all_findings if f.severity.value == 'CRITICAL']),
                'HIGH': len([f for f in final_report.all_findings if f.severity.value == 'HIGH']),
                'MEDIUM': len([f for f in final_report.all_findings if f.severity.value == 'MEDIUM']),
                'LOW': len([f for f in final_report.all_findings if f.severity.value == 'LOW']),
                'INFO': len([f for f in final_report.all_findings if f.severity.value == 'INFO'])
            },
            'conflicts_detected': final_report.conflicts_detected,
            'metadata': metadata or {}
        }
        
        self.tasks.append(task_record)
        self._save()
    
    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific task by ID.
        
        Args:
            task_id: Task ID to retrieve
            
        Returns:
            Task record or None
        """
        for task in self.tasks:
            if task['task_id'] == task_id:
                return task
        return None
    
    def get_recent_tasks(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get most recent tasks.
        
        Args:
            limit: Maximum number of tasks to return
            
        Returns:
            List of recent task records
        """
        return sorted(self.tasks, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    def get_tasks_by_decision(self, decision: str) -> List[Dict[str, Any]]:
        """
        Get all tasks with a specific final decision.
        
        Args:
            decision: Decision to filter by (APPROVE/BLOCK/NEEDS_REVISION)
            
        Returns:
            List of matching task records
        """
        return [task for task in self.tasks if task['final_decision'] == decision]
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Calculate statistics across all tasks.
        
        Returns:
            Dictionary of statistics
        """
        if not self.tasks:
            return {
                'total_tasks': 0,
                'avg_findings': 0,
                'decision_distribution': {},
                'most_common_severity': None,
                'conflict_rate': 0
            }
        
        total_tasks = len(self.tasks)
        total_findings = sum(task['total_findings'] for task in self.tasks)
        conflicts = sum(1 for task in self.tasks if task['conflicts_detected'])
        
        # Decision distribution
        decisions = {}
        for task in self.tasks:
            decision = task['final_decision']
            decisions[decision] = decisions.get(decision, 0) + 1
        
        # Severity distribution
        severity_totals = {
            'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'INFO': 0
        }
        for task in self.tasks:
            for severity, count in task['findings_by_severity'].items():
                severity_totals[severity] += count
        
        most_common_severity = max(severity_totals.items(), key=lambda x: x[1])[0]
        
        return {
            'total_tasks': total_tasks,
            'avg_findings': total_findings / total_tasks,
            'decision_distribution': decisions,
            'severity_distribution': severity_totals,
            'most_common_severity': most_common_severity,
            'conflict_rate': conflicts / total_tasks,
            'conflicts_detected': conflicts
        }
    
    def search_by_finding_type(self, finding_type: str) -> List[Dict[str, Any]]:
        """
        Search for tasks that had a specific type of finding.
        Note: This is limited since we don't store full finding details.
        
        Args:
            finding_type: Type of finding to search for
            
        Returns:
            List of matching task records
        """
        # This is a simple implementation - in production you'd store more details
        results = []
        for task in self.tasks:
            # You could enhance this by storing finding types in the task record
            results.append(task)
        return results
    
    def get_agent_performance(self) -> Dict[str, Dict[str, Any]]:
        """
        Calculate performance metrics for each agent.
        
        Returns:
            Dictionary of agent performance metrics
        """
        agent_stats = {}
        
        for task in self.tasks:
            for agent_info in task['agents_involved']:
                agent_type = agent_info['agent_type']
                
                if agent_type not in agent_stats:
                    agent_stats[agent_type] = {
                        'tasks_processed': 0,
                        'total_findings': 0,
                        'avg_confidence': 0,
                        'decisions': {'APPROVE': 0, 'BLOCK': 0, 'NEEDS_REVISION': 0}
                    }
                
                agent_stats[agent_type]['tasks_processed'] += 1
                agent_stats[agent_type]['total_findings'] += agent_info['findings_count']
                agent_stats[agent_type]['avg_confidence'] += agent_info['confidence']
                agent_stats[agent_type]['decisions'][agent_info['decision']] += 1
        
        # Calculate averages
        for agent_type, stats in agent_stats.items():
            if stats['tasks_processed'] > 0:
                stats['avg_confidence'] /= stats['tasks_processed']
                stats['avg_findings'] = stats['total_findings'] / stats['tasks_processed']
        
        return agent_stats
    
    def clear_history(self) -> None:
        """Clear all task history."""
        self.tasks = []
        self._save()
    
    def export_to_json(self, output_path: str) -> None:
        """
        Export task history to JSON file.
        
        Args:
            output_path: Path to output file
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, indent=2, default=str)
    
    def get_summary_report(self) -> str:
        """
        Generate a summary report of task history.
        
        Returns:
            Formatted summary string
        """
        stats = self.get_statistics()
        agent_perf = self.get_agent_performance()
        
        lines = []
        lines.append("=" * 70)
        lines.append("TASK HISTORY SUMMARY")
        lines.append("=" * 70)
        lines.append(f"Total Tasks Processed: {stats['total_tasks']}")
        lines.append(f"Average Findings per Task: {stats['avg_findings']:.2f}")
        lines.append(f"Conflict Rate: {stats['conflict_rate']*100:.1f}%")
        lines.append("")
        
        lines.append("Decision Distribution:")
        for decision, count in stats['decision_distribution'].items():
            percentage = (count / stats['total_tasks']) * 100
            lines.append(f"  {decision}: {count} ({percentage:.1f}%)")
        lines.append("")
        
        lines.append("Severity Distribution:")
        for severity, count in stats['severity_distribution'].items():
            lines.append(f"  {severity}: {count}")
        lines.append("")
        
        lines.append("Agent Performance:")
        for agent_type, perf in agent_perf.items():
            lines.append(f"  {agent_type}:")
            lines.append(f"    Tasks: {perf['tasks_processed']}")
            lines.append(f"    Avg Findings: {perf['avg_findings']:.2f}")
            lines.append(f"    Avg Confidence: {perf['avg_confidence']*100:.1f}%")
        
        lines.append("=" * 70)
        
        return '\n'.join(lines)
