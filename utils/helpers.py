"""
Helper utilities for AgentMesh.
Shared utility functions used across the system.
"""

import re
from typing import List, Dict, Any
from datetime import datetime
import hashlib


def generate_task_id(description: str) -> str:
    """
    Generate a unique task ID based on description and timestamp.
    
    Args:
        description: Task description
        
    Returns:
        Unique task ID
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    desc_hash = hashlib.md5(description.encode()).hexdigest()[:6]
    return f"task-{timestamp}-{desc_hash}"


def extract_functions(code: str) -> List[Dict[str, Any]]:
    """
    Extract function definitions from Python code.
    
    Args:
        code: Python source code
        
    Returns:
        List of function info dictionaries
    """
    functions = []
    lines = code.split('\n')
    
    for i, line in enumerate(lines, 1):
        match = re.match(r'^\s*def\s+(\w+)\s*\((.*?)\)', line)
        if match:
            func_name = match.group(1)
            params = match.group(2)
            functions.append({
                'name': func_name,
                'line': i,
                'params': params,
                'definition': line.strip()
            })
    
    return functions


def count_lines_of_code(code: str, exclude_blank: bool = True, 
                        exclude_comments: bool = True) -> int:
    """
    Count lines of code.
    
    Args:
        code: Source code
        exclude_blank: Whether to exclude blank lines
        exclude_comments: Whether to exclude comment lines
        
    Returns:
        Line count
    """
    lines = code.split('\n')
    count = 0
    
    for line in lines:
        stripped = line.strip()
        
        # Skip blank lines
        if exclude_blank and not stripped:
            continue
        
        # Skip comment lines
        if exclude_comments and stripped.startswith('#'):
            continue
        
        count += 1
    
    return count


def sanitize_code(code: str) -> str:
    """
    Basic code sanitization for display.
    
    Args:
        code: Source code
        
    Returns:
        Sanitized code
    """
    # Remove any potentially dangerous patterns for display
    # This is just basic sanitization for demo
    code = code.replace('\r\n', '\n')
    code = code.replace('\r', '\n')
    return code


def format_duration(seconds: float) -> str:
    """
    Format duration in human-readable format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted string
    """
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def format_percentage(value: float) -> str:
    """
    Format float as percentage.
    
    Args:
        value: Float value between 0 and 1
        
    Returns:
        Formatted percentage string
    """
    return f"{value*100:.1f}%"


def truncate_string(text: str, max_length: int = 100, 
                   suffix: str = "...") -> str:
    """
    Truncate string to maximum length.
    
    Args:
        text: String to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def parse_severity_from_string(severity_str: str) -> str:
    """
    Parse severity from various string formats.
    
    Args:
        severity_str: Severity string
        
    Returns:
        Normalized severity string
    """
    severity_str = severity_str.upper().strip()
    
    valid_severities = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']
    
    if severity_str in valid_severities:
        return severity_str
    
    # Map common alternatives
    mappings = {
        'CRIT': 'CRITICAL',
        'ERROR': 'HIGH',
        'WARN': 'MEDIUM',
        'WARNING': 'MEDIUM',
        'MINOR': 'LOW',
        'TRIVIAL': 'LOW'
    }
    
    return mappings.get(severity_str, 'MEDIUM')


def colorize_severity(severity: str, text: str) -> str:
    """
    Add ANSI color codes to text based on severity.
    
    Args:
        severity: Severity level
        text: Text to colorize
        
    Returns:
        Colorized text
    """
    colors = {
        'CRITICAL': '\033[91m',  # Red
        'HIGH': '\033[93m',      # Yellow
        'MEDIUM': '\033[94m',    # Blue
        'LOW': '\033[92m',       # Green
        'INFO': '\033[96m'       # Cyan
    }
    
    reset = '\033[0m'
    color = colors.get(severity.upper(), '')
    
    return f"{color}{text}{reset}"


def extract_imports(code: str) -> List[str]:
    """
    Extract import statements from Python code.
    
    Args:
        code: Python source code
        
    Returns:
        List of imported modules
    """
    imports = []
    lines = code.split('\n')
    
    for line in lines:
        # Match "import module"
        match1 = re.match(r'^\s*import\s+([\w.]+)', line)
        if match1:
            imports.append(match1.group(1))
        
        # Match "from module import ..."
        match2 = re.match(r'^\s*from\s+([\w.]+)\s+import', line)
        if match2:
            imports.append(match2.group(1))
    
    return list(set(imports))  # Remove duplicates


def calculate_code_complexity(code: str) -> int:
    """
    Calculate basic code complexity (simplified cyclomatic complexity).
    
    Args:
        code: Python source code
        
    Returns:
        Complexity score
    """
    complexity = 1  # Base complexity
    
    # Count decision points
    keywords = ['if', 'elif', 'for', 'while', 'except', 'and', 'or']
    
    for keyword in keywords:
        # Count occurrences of keywords
        pattern = r'\b' + keyword + r'\b'
        matches = re.findall(pattern, code)
        complexity += len(matches)
    
    return complexity


def indent_text(text: str, spaces: int = 2) -> str:
    """
    Indent all lines in text.
    
    Args:
        text: Text to indent
        spaces: Number of spaces to indent
        
    Returns:
        Indented text
    """
    indent = ' ' * spaces
    lines = text.split('\n')
    return '\n'.join(indent + line if line.strip() else line for line in lines)


def create_separator(char: str = "=", length: int = 70) -> str:
    """
    Create a separator line.
    
    Args:
        char: Character to use
        length: Length of separator
        
    Returns:
        Separator string
    """
    return char * length


def dict_to_table(data: Dict[str, Any], headers: List[str] = None) -> str:
    """
    Convert dictionary to simple table format.
    
    Args:
        data: Dictionary to display
        headers: Optional column headers
        
    Returns:
        Formatted table string
    """
    if headers is None:
        headers = ["Key", "Value"]
    
    lines = []
    lines.append(f"{headers[0]:30} {headers[1]}")
    lines.append("-" * 50)
    
    for key, value in data.items():
        key_str = str(key)[:30]
        value_str = str(value)[:50]
        lines.append(f"{key_str:30} {value_str}")
    
    return '\n'.join(lines)
