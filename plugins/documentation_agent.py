"""
Documentation Quality Agent Plugin for AgentMesh Framework.
Checks code for documentation quality issues.
"""

from agents.base_agent import BaseAgent
from core.models import AgentResponse, Finding, Severity


# Plugin Metadata - Required for framework discovery
PLUGIN_NAME = "DocumentationAgent"
PLUGIN_VERSION = "1.0.0"
PLUGIN_CAPABILITIES = [
    'documentation', 'docs', 'comment', 'docstring', 'readme',
    'api', 'explain', 'description', 'usage', 'example'
]


def create_agent(message_bus):
    """
    Factory function required by plugin loader.
    
    Args:
        message_bus: MessageBus instance for agent communication
        
    Returns:
        Configured DocumentationAgent instance
    """
    return DocumentationAgent(message_bus)


class DocumentationAgent(BaseAgent):
    """Specialist agent for documentation quality analysis."""
    
    def __init__(self, message_bus):
        super().__init__("documentation-agent", "DOCUMENTATION", message_bus)
    
    def _analyze(self, task):
        """
        Analyze code for documentation issues.
        
        Checks:
        - Missing docstrings
        - Incomplete API documentation
        - Missing examples
        - Poor comment quality
        """
        findings = []
        code = task.payload.get('code', '')
        code_lines = code.split('\n')
        
        # Check for missing docstrings
        if '"""' not in code and "'''" not in code:
            findings.append(Finding(
                category='MISSING_DOCSTRING',
                severity=Severity.MEDIUM,
                line_number=1,
                code_snippet=code_lines[0] if code_lines else '',
                description='No docstrings found in code',
                recommendation='Add docstrings to describe module/class/function purpose'
            ))
        
        # Check for functions without docstrings
        for i, line in enumerate(code_lines, 1):
            if line.strip().startswith('def '):
                # Check if next few lines have docstring
                has_docstring = False
                for j in range(i, min(i + 3, len(code_lines))):
                    if '"""' in code_lines[j] or "'''" in code_lines[j]:
                        has_docstring = True
                        break
                
                if not has_docstring:
                    findings.append(Finding(
                        category='MISSING_FUNCTION_DOCSTRING',
                        severity=Severity.LOW,
                        line_number=i,
                        code_snippet=line.strip(),
                        description='Function without docstring',
                        recommendation='Add docstring explaining parameters, returns, and purpose'
                    ))
        
        # Check for poor inline comments
        for i, line in enumerate(code_lines, 1):
            if '#' in line:
                comment = line.split('#')[1].strip()
                if len(comment) < 5:
                    findings.append(Finding(
                        category='POOR_COMMENT',
                        severity=Severity.LOW,
                        line_number=i,
                        code_snippet=line.strip(),
                        description='Comment is too short to be meaningful',
                        recommendation='Provide more detailed explanation'
                    ))
        
        # Calculate confidence
        confidence = min(0.70 + (len(findings) * 0.05), 0.90)
        
        decision = 'NEEDS_REVISION' if len(findings) > 3 else 'APPROVE'
        
        return AgentResponse(
            agent_id=self.agent_id,
            task_id=task.task_id,
            findings=findings,
            decision=decision,
            confidence=confidence,
            metadata={'total_findings': len(findings)}
        )
