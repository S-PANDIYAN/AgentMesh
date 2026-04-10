#!/usr/bin/env python3
"""
AgentMesh CLI - Command-Line Interface for AgentMesh Framework
Provides terminal commands for code review, agent management, and benchmarking.
"""
import sys
import os
import time
import json
from pathlib import Path
from typing import Optional, List

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from rich.progress import Progress

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from framework_init import initialize_framework
from core.models import Task


console = Console()


class AgentMeshCLI:
    """CLI wrapper for AgentMesh framework."""
    
    def __init__(self):
        """Initialize the CLI with framework components."""
        console.print("[bold blue]Initializing AgentMesh Framework...[/bold blue]")
        self.registry, self.loader, self.coordinator, self.logger = initialize_framework()
        console.print(f"[green]✓[/green] Loaded {len(self.registry.list_agents())} agents\n")
    
    def review_file(self, filepath: str, priority: str = "MEDIUM", 
                   output_format: str = "text", save_report: bool = False) -> dict:
        """Review a code file using multiple agents."""
        
        # Read file
        if not os.path.exists(filepath):
            console.print(f"[red]✗[/red] File not found: {filepath}")
            return {'error': 'File not found'}
        
        with open(filepath, 'r', encoding='utf-8') as f:
            code_content = f.read()
        
        # Create task
        task = Task(
            task_id=f"cli-{int(time.time())}",
            description=f"Review code file: {filepath}",
            priority=priority,
            task_type="code_review",
            payload={'code': code_content, 'filename': filepath}
        )
        
        # Process with progress
        with Progress() as progress:
            task_progress = progress.add_task("[cyan]Processing review...", total=100)
            
            start_time = time.time()
            report = self.coordinator.process_task(task)
            processing_time = time.time() - start_time
            
            progress.update(task_progress, completed=100)
        
        # Prepare result
        result = {
            'file': filepath,
            'decision': report.final_decision,
            'confidence': report.confidence_score,
            'processing_time_ms': round(processing_time * 1000, 2),
            'agents_consulted': len(report.agent_reports),
            'findings': []
        }
        
        for agent_report in report.agent_reports:
            result['findings'].append({
                'agent': agent_report.agent_id,
                'decision': agent_report.decision,
                'confidence': agent_report.confidence,
                'issues': agent_report.findings
            })
        
        # Output based on format
        if output_format == "json":
            console.print_json(data=result)
        else:
            self._print_review_report(result)
        
        # Save report if requested
        if save_report:
            report_path = f"{filepath}.agentmesh-report.json"
            with open(report_path, 'w') as f:
                json.dump(result, f, indent=2)
            console.print(f"\n[green]✓[/green] Report saved to: {report_path}")
        
        return result
    
    def _print_review_report(self, result: dict):
        """Print formatted review report."""
        
        # Header
        console.print(Panel(
            f"[bold]Code Review Report[/bold]\n"
            f"File: {result['file']}\n"
            f"Decision: [{'green' if result['decision'] == 'APPROVE' else 'red'}]{result['decision']}[/]\n"
            f"Confidence: {result['confidence']:.1f}%\n"
            f"Processing Time: {result['processing_time_ms']}ms",
            title="AgentMesh Review",
            border_style="blue"
        ))
        
        # Agent findings
        console.print(f"\n[bold]Agent Findings ({result['agents_consulted']} agents):[/bold]\n")
        
        for finding in result['findings']:
            # Agent header
            decision_color = "green" if finding['decision'] == "APPROVE" else "red"
            console.print(f"[bold cyan]→ {finding['agent']}[/bold cyan] "
                         f"[{decision_color}]{finding['decision']}[/] "
                         f"({finding['confidence']:.0f}%)")
            
            # Issues
            if finding['issues']:
                for i, issue in enumerate(finding['issues'], 1):
                    console.print(f"  {i}. {issue}")
            else:
                console.print("  [dim]No issues found[/dim]")
            console.print()
    
    def list_agents_cmd(self, output_format: str = "text"):
        """List all available agents."""
        agents = self.registry.list_agents()
        
        if output_format == "json":
            agent_data = [
                {
                    'id': agent.agent_id,
                    'type': agent.agent_type.value,
                    'capabilities': self.registry.get_agent_capabilities(agent.agent_id),
                    'priority': self.registry._agent_priorities.get(agent.agent_id, 5)
                }
                for agent in agents
            ]
            console.print_json(data=agent_data)
        else:
            table = Table(title="Available Agents", show_header=True, header_style="bold magenta")
            table.add_column("ID", style="cyan")
            table.add_column("Type", style="green")
            table.add_column("Capabilities", style="yellow")
            table.add_column("Priority", justify="center")
            
            for agent in agents:
                capabilities = self.registry.get_agent_capabilities(agent.agent_id)
                priority = self.registry._agent_priorities.get(agent.agent_id, 5)
                
                table.add_row(
                    agent.agent_id,
                    agent.agent_type.value,
                    ", ".join(capabilities[:5]) + ("..." if len(capabilities) > 5 else ""),
                    str(priority)
                )
            
            console.print(table)
            console.print(f"\n[bold]Total:[/bold] {len(agents)} agents")
    
    def reload_plugins_cmd(self):
        """Reload all plugins."""
        console.print("[yellow]Reloading plugins...[/yellow]")
        
        results = self.loader.reload_all_plugins()
        
        # Re-register agents
        self.registry._agents.clear()
        self.registry._capabilities.clear()
        
        for plugin_name, plugin_info in self.loader.loaded_plugins.items():
            agent = self.loader.create_agent_instance(plugin_name, self.coordinator.message_bus)
            capabilities = plugin_info.get('capabilities', [])
            priority = plugin_info.get('priority', 5)
            
            self.registry.register(agent, capabilities=capabilities, priority=priority)
        
        # Print results
        table = Table(title="Plugin Reload Results")
        table.add_column("Plugin", style="cyan")
        table.add_column("Status", style="green")
        
        for plugin, status in results.items():
            status_text = "[green]✓ Success[/green]" if status else "[red]✗ Failed[/red]"
            table.add_row(plugin, status_text)
        
        console.print(table)
        console.print(f"\n[green]✓[/green] Reloaded {len(self.registry.list_agents())} agents")
    
    def benchmark_cmd(self, num_tasks: int = 100):
        """Run performance benchmark."""
        console.print(f"[bold blue]Running benchmark with {num_tasks} tasks...[/bold blue]\n")
        
        # Sample task
        sample_code = """
def process_payment(card_number, amount):
    if amount > 1000:
        return charge_card(card_number, amount)
    return True
"""
        
        # Run benchmark
        processing_times = []
        
        with Progress() as progress:
            task_progress = progress.add_task("[cyan]Processing tasks...", total=num_tasks)
            
            for i in range(num_tasks):
                task = Task(
                    task_id=f"bench-{i}",
                    description="Benchmark task",
                    priority="MEDIUM",
                    task_type="code_review",
                    payload={'code': sample_code}
                )
                
                start = time.time()
                self.coordinator.process_task(task)
                elapsed = time.time() - start
                
                processing_times.append(elapsed * 1000)  # Convert to ms
                progress.update(task_progress, advance=1)
        
        # Calculate statistics
        avg_time = sum(processing_times) / len(processing_times)
        min_time = min(processing_times)
        max_time = max(processing_times)
        throughput = 1000 / avg_time  # tasks per second
        
        # Print results
        console.print(Panel(
            f"[bold]Benchmark Results[/bold]\n\n"
            f"Tasks Processed: {num_tasks}\n"
            f"Average Time: {avg_time:.2f}ms\n"
            f"Min Time: {min_time:.2f}ms\n"
            f"Max Time: {max_time:.2f}ms\n"
            f"Throughput: {throughput:.0f} tasks/second",
            title="Performance",
            border_style="green"
        ))
    
    def select_agents_cmd(self, description: str, weighted: bool = False):
        """Select agents for a task description."""
        selected = self.registry.auto_select_agents(description, use_weighted=weighted)
        
        console.print(f"\n[bold]Task:[/bold] {description}")
        console.print(f"[bold]Selection Mode:[/bold] {'Weighted' if weighted else 'Standard'}\n")
        
        if selected:
            table = Table(title="Selected Agents")
            table.add_column("Agent ID", style="cyan")
            table.add_column("Type", style="green")
            table.add_column("Capabilities", style="yellow")
            
            for agent in selected:
                caps = self.registry.get_agent_capabilities(agent.agent_id)
                table.add_row(
                    agent.agent_id,
                    agent.agent_type.value,
                    ", ".join(caps[:3]) + ("..." if len(caps) > 3 else "")
                )
            
            console.print(table)
            console.print(f"\n[green]✓[/green] Selected {len(selected)} agents")
        else:
            console.print("[yellow]No agents selected[/yellow]")


# Click CLI commands
@click.group()
@click.version_option(version="1.0.0")
def cli():
    """AgentMesh - Multi-Agent Code Review Framework"""
    pass


@cli.command()
@click.argument('filepath', type=click.Path(exists=True))
@click.option('--priority', type=click.Choice(['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']), 
              default='MEDIUM', help='Task priority')
@click.option('--format', 'output_format', type=click.Choice(['text', 'json']), 
              default='text', help='Output format')
@click.option('--save', is_flag=True, help='Save report to file')
def review(filepath: str, priority: str, output_format: str, save: bool):
    """Review a code file using multiple agents."""
    cli_instance = AgentMeshCLI()
    cli_instance.review_file(filepath, priority, output_format, save)


@cli.command()
@click.option('--format', 'output_format', type=click.Choice(['text', 'json']), 
              default='text', help='Output format')
def agents(output_format: str):
    """List all available agents."""
    cli_instance = AgentMeshCLI()
    cli_instance.list_agents_cmd(output_format)


@cli.command()
def reload():
    """Reload all plugins."""
    cli_instance = AgentMeshCLI()
    cli_instance.reload_plugins_cmd()


@cli.command()
@click.option('--tasks', type=int, default=100, help='Number of tasks to run')
def benchmark(tasks: int):
    """Run performance benchmark."""
    cli_instance = AgentMeshCLI()
    cli_instance.benchmark_cmd(tasks)


@cli.command()
@click.argument('description')
@click.option('--weighted', is_flag=True, help='Use weighted selection')
def select(description: str, weighted: bool):
    """Select agents for a task description."""
    cli_instance = AgentMeshCLI()
    cli_instance.select_agents_cmd(description, weighted)


if __name__ == '__main__':
    cli()
