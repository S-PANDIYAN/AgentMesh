"""
Code Quality Analyzer Agent
Specializes in code quality, maintainability, and best practices.

PLUGIN for AgentMesh Framework
"""

from typing import List
import re

from agents.base_agent import BaseAgent
from core.models import Task, Finding, Severity, AgentType
from core.message_bus import MessageBus


# Plugin metadata
PLUGIN_NAME = "CodeQualityAgent"
PLUGIN_VERSION = "1.0.0"
PLUGIN_CAPABILITIES = [
    'quality', 'code', 'structure', 'naming', 'style', 'maintainability',
    'review', 'bug', 'error', 'exception', 'refactor', 'clean', 'maintain',
    'documentation', 'docstring', 'type hints', 'conventions', 'best practices'
]


class CodeQualityAgent(BaseAgent):
    """
    Agent specialized in code quality analysis.
    Checks for bugs, code smells, best practices, and maintainability issues.
    """
    
    def __init__(self, message_bus: MessageBus):
        super().__init__(
            agent_id="code-quality-agent",
            agent_type=AgentType.CODE_QUALITY,
            message_bus=message_bus
        )
        
        # Code quality patterns
        self.quality_patterns = {
            "MISSING_ERROR_HANDLING": {
                "positive": [r'def\s+\w+\s*\([^)]*\):'],
                "negative": [r'try:', r'except', r'raise'],
                "severity": Severity.MEDIUM,
                "confidence": 0.70
            },
            "BARE_EXCEPT": {
                "patterns": [r'except\s*:'],
                "severity": Severity.MEDIUM,
                "confidence": 0.90
            },
            "PRINT_STATEMENT": {
                "patterns": [r'print\s*\('],
                "severity": Severity.LOW,
                "confidence": 0.95
            },
            "TODO_COMMENT": {
                "patterns": [r'#\s*TODO', r'#\s*FIXME', r'#\s*HACK'],
                "severity": Severity.LOW,
                "confidence": 1.0
            },
            "MUTABLE_DEFAULT_ARG": {
                "patterns": [r'def\s+\w+\s*\([^)]*=\s*\[', r'def\s+\w+\s*\([^)]*=\s*\{'],
                "severity": Severity.MEDIUM,
                "confidence": 0.85
            },
        }
    
    def _analyze(self, task: Task) -> List[Finding]:
        """
        Perform code quality analysis.
        
        Args:
            task: Task containing code to analyze
            
        Returns:
            List of code quality findings
        """
        findings = []
        code = task.payload.get('code', '')
        lines = code.split('\n')
        
        # Check for quality patterns
        for issue_type, pattern_info in self.quality_patterns.items():
            if "patterns" in pattern_info:
                for pattern in pattern_info["patterns"]:
                    for line_num, line in enumerate(lines, 1):
                        if re.search(pattern, line):
                            findings.append(self._create_finding(
                                issue_type=issue_type,
                                line_num=line_num,
                                line_content=line.strip(),
                                severity=pattern_info["severity"],
                                confidence=pattern_info["confidence"]
                            ))
        
        # Check for missing error handling
        findings.extend(self._check_error_handling(code, lines))
        
        # Check code structure
        findings.extend(self._check_code_structure(code, lines))
        
        # Check naming conventions
        findings.extend(self._check_naming_conventions(code, lines))
        
        # Check for type hints
        findings.extend(self._check_type_hints(code, lines))
        
        return findings
    
    def _create_finding(self, issue_type: str, line_num: int, line_content: str,
                       severity: Severity, confidence: float) -> Finding:
        """Create a code quality finding."""
        
        descriptions = {
            "BARE_EXCEPT": "Bare except clause catches all exceptions including system exits. Specify exception types.",
            "PRINT_STATEMENT": "Print statement found. Use proper logging instead of print() for production code.",
            "TODO_COMMENT": "TODO/FIXME comment found. Should be addressed before production.",
            "MUTABLE_DEFAULT_ARG": "Mutable default argument (list/dict). This can cause unexpected behavior across function calls.",
            "MISSING_TYPE_HINTS": "Function lacks type hints. Type hints improve code readability and enable better IDE support.",
            "NAMING_CONVENTION": "Variable/function name doesn't follow Python naming conventions (snake_case).",
            "COMPLEX_FUNCTION": "Function is complex and should be split into smaller functions for better maintainability.",
            "MISSING_DOCSTRING": "Function lacks docstring. Docstrings improve code documentation.",
            "DEAD_CODE": "Unreachable code detected after return statement.",
        }
        
        recommendations = {
            "BARE_EXCEPT": "Specify exception types: except (ValueError, TypeError):",
            "PRINT_STATEMENT": "Replace with logging: logger.info() or logger.debug()",
            "TODO_COMMENT": "Create a ticket for this TODO and complete it",
            "MUTABLE_DEFAULT_ARG": "Use None as default: def func(items=None): items = items or []",
            "MISSING_TYPE_HINTS": "Add type hints: def function(param: str) -> int:",
            "NAMING_CONVENTION": "Use snake_case for functions/variables: my_variable, my_function",
            "COMPLEX_FUNCTION": "Break into smaller functions, each doing one thing",
            "MISSING_DOCSTRING": "Add docstring explaining what the function does",
            "DEAD_CODE": "Remove unreachable code or fix control flow",
        }
        
        return Finding(
            severity=severity,
            finding_type=issue_type,
            description=descriptions.get(issue_type, f"{issue_type} detected"),
            location=f"Line {line_num}",
            evidence=line_content,
            recommendation=recommendations.get(issue_type, "Review and improve code quality"),
            confidence=confidence
        )
    
    def _check_error_handling(self, code: str, lines: List[str]) -> List[Finding]:
        """Check for proper error handling."""
        findings = []
        
        # Check if functions have try-except blocks
        function_lines = []
        for i, line in enumerate(lines):
            if re.match(r'^\s*def\s+\w+', line):
                function_lines.append((i + 1, line))
        
        for func_line_num, func_line in function_lines:
            # Check if function body has error handling
            # Look ahead 10 lines
            has_error_handling = False
            for j in range(func_line_num, min(func_line_num + 10, len(lines))):
                if 'try:' in lines[j] or 'except' in lines[j]:
                    has_error_handling = True
                    break
            
            # If function does database/network operations without error handling
            has_risky_ops = False
            for j in range(func_line_num, min(func_line_num + 10, len(lines))):
                if any(keyword in lines[j].lower() for keyword in ['query', 'request', 'open', 'read']):
                    has_risky_ops = True
                    break
            
            if has_risky_ops and not has_error_handling:
                findings.append(Finding(
                    severity=Severity.MEDIUM,
                    finding_type="MISSING_ERROR_HANDLING",
                    description="Function performs risky operations without error handling.",
                    location=f"Line {func_line_num}",
                    evidence=func_line.strip(),
                    recommendation="Wrap risky operations in try-except blocks",
                    confidence=0.75
                ))
        
        return findings
    
    def _check_code_structure(self, code: str, lines: List[str]) -> List[Finding]:
        """Check code structure and organization."""
        findings = []
        
        # Check function length
        current_function = None
        function_start = 0
        
        for i, line in enumerate(lines):
            # Detect function definition
            func_match = re.match(r'^(\s*)def\s+(\w+)', line)
            if func_match:
                # If we were tracking a previous function
                if current_function is not None:
                    func_length = i - function_start
                    if func_length > 30:  # Functions longer than 30 lines
                        findings.append(Finding(
                            severity=Severity.LOW,
                            finding_type="LONG_FUNCTION",
                            description=f"Function '{current_function}' is {func_length} lines long. Consider breaking it down.",
                            location=f"Line {function_start + 1}",
                            evidence=f"def {current_function}(...)",
                            recommendation="Split into smaller, single-responsibility functions",
                            confidence=0.80
                        ))
                
                current_function = func_match.group(2)
                function_start = i
        
        # Check for dead code (code after return in same block)
        for i, line in enumerate(lines[:-1]):  # Exclude last line
            if re.search(r'^\s*return\s', line):
                next_line = lines[i + 1].strip()
                # Check if next line is code (not empty, not comment, not new function/class)
                if next_line and not next_line.startswith('#') and not next_line.startswith('def ') and not next_line.startswith('class '):
                    # Check indentation - if same level, it's dead code
                    curr_indent = len(line) - len(line.lstrip())
                    next_indent = len(lines[i + 1]) - len(lines[i + 1].lstrip())
                    if next_indent == curr_indent:
                        findings.append(Finding(
                            severity=Severity.MEDIUM,
                            finding_type="DEAD_CODE",
                            description="Unreachable code found after return statement.",
                            location=f"Line {i + 2}",
                            evidence=next_line,
                            recommendation="Remove dead code or fix control flow",
                            confidence=0.85
                        ))
        
        return findings
    
    def _check_naming_conventions(self, code: str, lines: List[str]) -> List[Finding]:
        """Check Python naming conventions."""
        findings = []
        
        # Check function names (should be snake_case)
        for i, line in enumerate(lines):
            func_match = re.search(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)', line)
            if func_match:
                func_name = func_match.group(1)
                # Check if camelCase (not snake_case)
                if re.search(r'[a-z][A-Z]', func_name) and not func_name.startswith('_'):
                    findings.append(Finding(
                        severity=Severity.LOW,
                        finding_type="NAMING_CONVENTION",
                        description=f"Function name '{func_name}' uses camelCase. Python convention is snake_case.",
                        location=f"Line {i + 1}",
                        evidence=line.strip(),
                        recommendation=f"Rename to: {self._to_snake_case(func_name)}",
                        confidence=0.95
                    ))
        
        return findings
    
    def _check_type_hints(self, code: str, lines: List[str]) -> List[Finding]:
        """Check for type hints in function signatures."""
        findings = []
        
        for i, line in enumerate(lines):
            # Find function definitions
            if re.match(r'^\s*def\s+\w+', line):
                # Check if it has type hints (: or ->)
                if ':' not in line and '->' not in line:
                    # Skip __init__ and magic methods
                    if not re.search(r'def\s+__\w+__', line):
                        findings.append(Finding(
                            severity=Severity.LOW,
                            finding_type="MISSING_TYPE_HINTS",
                            description="Function lacks type hints for better code documentation.",
                            location=f"Line {i + 1}",
                            evidence=line.strip(),
                            recommendation="Add type hints: def function(param: str) -> int:",
                            confidence=0.80
                        ))
        
        return findings
    
    def _to_snake_case(self, name: str) -> str:
        """Convert camelCase to snake_case."""
        return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
    
    def _make_recommendation(self, findings: List[Finding]) -> str:
        """Override to provide code-quality-specific recommendations."""
        has_critical = any(f.severity == Severity.CRITICAL for f in findings)
        has_high = any(f.severity == Severity.HIGH for f in findings)
        has_medium = any(f.severity == Severity.MEDIUM for f in findings)
        
        if has_critical:
            return "BLOCK"
        elif has_high:
            return "APPROVE_WITH_CHANGES"
        elif has_medium:
            return "APPROVE_WITH_CHANGES"
        else:
            return "APPROVE"


# Plugin factory function
def create_agent(message_bus: MessageBus) -> CodeQualityAgent:
    """
    Factory function to create agent instance.
    Called by framework when loading plugin.
    """
    return CodeQualityAgent(message_bus)
