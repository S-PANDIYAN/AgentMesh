"""
Performance Analyzer Agent
Specializes in performance optimization and efficiency analysis.

PLUGIN for AgentMesh Framework
"""

from typing import List
import re

from agents.base_agent import BaseAgent
from core.models import Task, Finding, Severity, AgentType
from core.message_bus import MessageBus


# Plugin metadata
PLUGIN_NAME = "PerformanceAgent"
PLUGIN_VERSION = "1.0.0"
PLUGIN_CAPABILITIES = [
    'performance', 'optimization', 'efficiency', 'speed', 'slow',
    'optimize', 'efficient', 'query', 'loop', 'database', 'cache',
    'n+1', 'bottleneck', 'latency', 'throughput', 'scalability'
]


class PerformanceAgent(BaseAgent):
    """
    Agent specialized in performance analysis.
    Identifies inefficient code patterns, database query issues, and optimization opportunities.
    """
    
    def __init__(self, message_bus: MessageBus):
        super().__init__(
            agent_id="performance-agent",
            agent_type=AgentType.PERFORMANCE,
            message_bus=message_bus
        )
        
        # Performance anti-patterns
        self.performance_patterns = {
            "N_PLUS_ONE_QUERY": {
                "indicators": [r'for\s+\w+\s+in\s+.*?:', r'\.query\(', r'\.get\(', r'\.filter\('],
                "severity": Severity.HIGH,
                "confidence": 0.80
            },
            "INEFFICIENT_LOOP": {
                "patterns": [
                    r'for\s+.*?\s+in\s+.*?:\s*\n\s+.*?\.append\(',  # List comprehension candidate
                    r'for\s+.*?\s+in\s+range\(len\(',  # Should use enumerate
                ],
                "severity": Severity.MEDIUM,
                "confidence": 0.85
            },
            "MULTIPLE_DB_CALLS": {
                "patterns": [r'\.query\(.*?\n.*?\.query\('],
                "severity": Severity.MEDIUM,
                "confidence": 0.75
            },
        }
    
    def _analyze(self, task: Task) -> List[Finding]:
        """
        Perform performance analysis.
        
        Args:
            task: Task containing code to analyze
            
        Returns:
            List of performance findings
        """
        findings = []
        code = task.payload.get('code', '')
        lines = code.split('\n')
        
        # Check for N+1 query problems
        findings.extend(self._check_n_plus_one_queries(code, lines))
        
        # Check for inefficient loops
        findings.extend(self._check_inefficient_loops(code, lines))
        
        # Check for inefficient data structures
        findings.extend(self._check_data_structures(code, lines))
        
        # Check for repeated calculations
        findings.extend(self._check_repeated_calculations(code, lines))
        
        # Check for inefficient string operations
        findings.extend(self._check_string_operations(code, lines))
        
        return findings
    
    def _check_n_plus_one_queries(self, code: str, lines: List[str]) -> List[Finding]:
        """Check for N+1 query problems (database queries in loops)."""
        findings = []
        
        in_loop = False
        loop_start = 0
        indent_stack = []
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            indent = len(line) - len(line.lstrip())
            
            # Track loop entry
            if re.match(r'for\s+\w+\s+in\s+', stripped) or re.match(r'while\s+', stripped):
                in_loop = True
                loop_start = i + 1
                indent_stack.append(indent)
            
            # Track loop exit (dedent)
            if indent_stack and indent <= indent_stack[-1] and i > loop_start:
                if not stripped.startswith(('for', 'while', 'if', 'elif', 'else', 'try', 'except', 'finally')):
                    in_loop = False
                    if indent_stack:
                        indent_stack.pop()
            
            # Check for database queries in loop
            if in_loop and any(pattern in stripped for pattern in ['.query(', '.get(', '.filter(', '.execute(']):
                findings.append(Finding(
                    severity=Severity.HIGH,
                    finding_type="N_PLUS_ONE_QUERY",
                    description="Database query inside loop detected. This can cause N+1 query problem.",
                    location=f"Line {i + 1}",
                    evidence=stripped,
                    recommendation="Move query outside loop or use bulk operations (e.g., .filter(id__in=ids))",
                    confidence=0.85
                ))
                in_loop = False  # Only report once per loop
        
        return findings
    
    def _check_inefficient_loops(self, code: str, lines: List[str]) -> List[Finding]:
        """Check for inefficient loop patterns."""
        findings = []
        
        for i, line in enumerate(lines):
            # Check for range(len()) pattern
            if re.search(r'for\s+\w+\s+in\s+range\(len\(', line):
                findings.append(Finding(
                    severity=Severity.LOW,
                    finding_type="INEFFICIENT_LOOP",
                    description="Using range(len()) pattern. Consider using enumerate() for better readability.",
                    location=f"Line {i + 1}",
                    evidence=line.strip(),
                    recommendation="Use: for index, item in enumerate(collection):",
                    confidence=0.90
                ))
            
            # Check for list.append() in loop (could be list comprehension)
            if i < len(lines) - 1:
                if re.search(r'for\s+\w+\s+in\s+', line):
                    next_line = lines[i + 1].strip()
                    if '.append(' in next_line and 'if' not in next_line:
                        findings.append(Finding(
                            severity=Severity.LOW,
                            finding_type="LIST_COMPREHENSION_OPPORTUNITY",
                            description="Loop with append could be replaced with list comprehension for better performance.",
                            location=f"Line {i + 1}",
                            evidence=f"{line.strip()} ... {next_line}",
                            recommendation="Consider list comprehension: result = [item for item in collection]",
                            confidence=0.75
                        ))
        
        return findings
    
    def _check_data_structures(self, code: str, lines: List[str]) -> List[Finding]:
        """Check for inefficient data structure usage."""
        findings = []
        
        # Check for list membership testing in loops
        for i, line in enumerate(lines):
            # Pattern: if item in list
            if re.search(r'if\s+\w+\s+in\s+\w+:', line) and '[' in code[:code.index(line) if line in code else 0]:
                # Check if the container was defined as a list
                # This is a simplified check
                findings.append(Finding(
                    severity=Severity.MEDIUM,
                    finding_type="INEFFICIENT_MEMBERSHIP_TEST",
                    description="Membership testing with list is O(n). Consider using set for O(1) lookup.",
                    location=f"Line {i + 1}",
                    evidence=line.strip(),
                    recommendation="Convert list to set for frequent membership testing: my_set = set(my_list)",
                    confidence=0.65
                ))
        
        # Check for repeated list concatenation
        for i, line in enumerate(lines):
            if '+=' in line and re.search(r'\w+\s*\+=\s*\[', line):
                findings.append(Finding(
                    severity=Severity.LOW,
                    finding_type="INEFFICIENT_LIST_CONCAT",
                    description="Repeated list concatenation with += is inefficient.",
                    location=f"Line {i + 1}",
                    evidence=line.strip(),
                    recommendation="Use list.extend() or collect items and create list once",
                    confidence=0.80
                ))
        
        return findings
    
    def _check_repeated_calculations(self, code: str, lines: List[str]) -> List[Finding]:
        """Check for repeated calculations that could be cached."""
        findings = []
        
        # Look for same function call appearing multiple times
        function_calls = {}
        for i, line in enumerate(lines):
            # Find function calls
            calls = re.findall(r'(\w+)\([^)]*\)', line)
            for call in calls:
                if call not in ['print', 'len', 'str', 'int', 'float', 'bool', 'list', 'dict', 'set']:
                    key = call
                    if key in function_calls:
                        function_calls[key].append(i + 1)
                    else:
                        function_calls[key] = [i + 1]
        
        # Report functions called multiple times
        for func_name, line_nums in function_calls.items():
            if len(line_nums) >= 3:  # Called 3 or more times
                findings.append(Finding(
                    severity=Severity.LOW,
                    finding_type="REPEATED_CALCULATION",
                    description=f"Function '{func_name}()' called {len(line_nums)} times. Consider caching result if deterministic.",
                    location=f"Lines {', '.join(map(str, line_nums[:3]))}...",
                    evidence=f"{func_name}() called multiple times",
                    recommendation="Cache result if function is pure: result = func(); # reuse result",
                    confidence=0.60
                ))
        
        return findings
    
    def _check_string_operations(self, code: str, lines: List[str]) -> List[Finding]:
        """Check for inefficient string operations."""
        findings = []
        
        # Check for string concatenation in loops
        in_loop = False
        loop_start = 0
        
        for i, line in enumerate(lines):
            if re.match(r'\s*for\s+\w+\s+in\s+', line):
                in_loop = True
                loop_start = i + 1
            elif in_loop and not line.startswith(' ' * 4) and line.strip():
                in_loop = False
            
            # Check for += string concatenation in loop
            if in_loop and '+=' in line and ('"' in line or "'" in line):
                findings.append(Finding(
                    severity=Severity.MEDIUM,
                    finding_type="INEFFICIENT_STRING_CONCAT",
                    description="String concatenation with += in loop is inefficient in Python.",
                    location=f"Line {i + 1}",
                    evidence=line.strip(),
                    recommendation="Use list and ''.join(): items = []; items.append(s); result = ''.join(items)",
                    confidence=0.85
                ))
        
        return findings
    
    def _make_recommendation(self, findings: List[Finding]) -> str:
        """Override to provide performance-specific recommendations."""
        has_critical = any(f.severity == Severity.CRITICAL for f in findings)
        has_high = any(f.severity == Severity.HIGH for f in findings)
        
        # Performance issues are rarely blocking unless critical
        if has_critical:
            return "BLOCK"
        elif has_high:
            return "APPROVE_WITH_CHANGES"  # High-impact performance issues
        elif findings:
            return "APPROVE"  # Other performance improvements are optional
        else:
            return "APPROVE"


# Plugin factory function
def create_agent(message_bus: MessageBus) -> PerformanceAgent:
    """
    Factory function to create agent instance.
    Called by framework when loading plugin.
    """
    return PerformanceAgent(message_bus)
