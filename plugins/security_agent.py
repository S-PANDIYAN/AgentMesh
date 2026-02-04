"""
Security Analyzer Agent
Specializes in identifying security vulnerabilities in code.

PLUGIN for AgentMesh Framework
"""

from typing import List
import re

from agents.base_agent import BaseAgent
from core.models import Task, Finding, Severity, AgentType
from core.message_bus import MessageBus


# Plugin metadata
PLUGIN_NAME = "SecurityAgent"
PLUGIN_VERSION = "1.0.0"
PLUGIN_CAPABILITIES = [
    'security', 'auth', 'authentication', 'login', 'password', 
    'token', 'session', 'encrypt', 'encryption', 'hash', 'hashing',
    'sql', 'injection', 'vulnerability', 'crypto', 'secrets'
]


class SecurityAgent(BaseAgent):
    """
    Agent specialized in security analysis.
    Detects SQL injection, weak cryptography, authentication issues, etc.
    """
    
    def __init__(self, message_bus: MessageBus):
        super().__init__(
            agent_id="security-agent",
            agent_type=AgentType.SECURITY,
            message_bus=message_bus
        )
        
        # Security patterns to check
        self.vulnerability_patterns = {
            "SQL_INJECTION": {
                "patterns": [
                    r'\.query\s*\(\s*f["\'].*?\{.*?\}',  # f-string in query
                    r'\.query\s*\(\s*["\'].*?\%s',  # %s formatting
                    r'\.execute\s*\(\s*f["\'].*?\{.*?\}',  # f-string in execute
                    r'\+.*?["\']SELECT',  # String concatenation with SELECT
                ],
                "severity": Severity.CRITICAL,
                "confidence": 0.95
            },
            "WEAK_HASH": {
                "patterns": [
                    r'hashlib\.md5',
                    r'hashlib\.sha1',
                ],
                "severity": Severity.HIGH,
                "confidence": 0.90
            },
            "HARDCODED_SECRET": {
                "patterns": [
                    r'password\s*=\s*["\'][^"\']{3,}["\']',
                    r'api_key\s*=\s*["\'][^"\']{10,}["\']',
                    r'secret\s*=\s*["\'][^"\']{10,}["\']',
                ],
                "severity": Severity.HIGH,
                "confidence": 0.85
            },
            "PREDICTABLE_RANDOM": {
                "patterns": [
                    r'random\.random\(',
                    r'random\.randint\(',
                    r'time\.time\(\)',
                ],
                "severity": Severity.MEDIUM,
                "confidence": 0.75
            },
            "UNSAFE_DESERIALIZATION": {
                "patterns": [
                    r'pickle\.loads?\(',
                    r'yaml\.load\(',
                ],
                "severity": Severity.HIGH,
                "confidence": 0.88
            },
        }
    
    def _analyze(self, task: Task) -> List[Finding]:
        """
        Perform security analysis on the code.
        
        Args:
            task: Task containing code to analyze
            
        Returns:
            List of security findings
        """
        findings = []
        code = task.payload.get('code', '')
        lines = code.split('\n')
        
        # Check for vulnerability patterns
        for vuln_type, vuln_info in self.vulnerability_patterns.items():
            for pattern in vuln_info["patterns"]:
                for line_num, line in enumerate(lines, 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        findings.append(self._create_finding(
                            vuln_type=vuln_type,
                            line_num=line_num,
                            line_content=line.strip(),
                            severity=vuln_info["severity"],
                            confidence=vuln_info["confidence"]
                        ))
        
        # Check for missing security features
        findings.extend(self._check_missing_security_features(code, lines))
        
        # Check authentication/session security
        findings.extend(self._check_auth_security(code, lines))
        
        return findings
    
    def _create_finding(self, vuln_type: str, line_num: int, line_content: str, 
                       severity: Severity, confidence: float) -> Finding:
        """Create a security finding with appropriate details."""
        
        descriptions = {
            "SQL_INJECTION": "SQL injection vulnerability detected. User input appears to be directly interpolated into SQL query.",
            "WEAK_HASH": "Weak cryptographic hash function detected (MD5/SHA1). Use SHA-256 or better.",
            "HARDCODED_SECRET": "Hardcoded secret detected. Secrets should be stored in environment variables or secure vaults.",
            "PREDICTABLE_RANDOM": "Predictable randomness used for security-sensitive operation. Use secrets module instead.",
            "UNSAFE_DESERIALIZATION": "Unsafe deserialization detected. Can lead to remote code execution.",
        }
        
        recommendations = {
            "SQL_INJECTION": "Use parameterized queries: db.query('SELECT * FROM users WHERE id=?', [user_id])",
            "WEAK_HASH": "Use hashlib.sha256() or better yet, use bcrypt for password hashing",
            "HARDCODED_SECRET": "Store secrets in environment variables: os.getenv('API_KEY')",
            "PREDICTABLE_RANDOM": "Use secrets.token_urlsafe() or secrets.token_hex() for cryptographic randomness",
            "UNSAFE_DESERIALIZATION": "Use json.loads() for untrusted data, or implement signature verification",
        }
        
        return Finding(
            severity=severity,
            finding_type=vuln_type,
            description=descriptions.get(vuln_type, f"{vuln_type} detected"),
            location=f"Line {line_num}",
            evidence=line_content,
            recommendation=recommendations.get(vuln_type, "Review and fix this security issue"),
            confidence=confidence
        )
    
    def _check_missing_security_features(self, code: str, lines: List[str]) -> List[Finding]:
        """Check for missing security features."""
        findings = []
        
        # Check for authentication without rate limiting
        has_auth_function = any(re.search(r'def\s+(auth|login|authenticate)', line, re.IGNORECASE) 
                               for line in lines)
        has_rate_limiting = any(re.search(r'rate.?limit|throttle|backoff', line, re.IGNORECASE) 
                               for line in lines)
        
        if has_auth_function and not has_rate_limiting:
            findings.append(Finding(
                severity=Severity.MEDIUM,
                finding_type="MISSING_RATE_LIMITING",
                description="Authentication function found without rate limiting. Vulnerable to brute force attacks.",
                location="Authentication function",
                evidence="No rate limiting mechanism detected",
                recommendation="Implement rate limiting (e.g., max 5 attempts per 15 minutes)",
                confidence=0.80
            ))
        
        # Check for password handling without proper hashing
        has_password = any(re.search(r'password', line, re.IGNORECASE) for line in lines)
        has_bcrypt = 'bcrypt' in code or 'argon2' in code or 'scrypt' in code
        
        if has_password and not has_bcrypt and not any('hash' in line.lower() for line in lines):
            findings.append(Finding(
                severity=Severity.HIGH,
                finding_type="MISSING_PASSWORD_HASHING",
                description="Password handling detected without proper hashing mechanism.",
                location="Password handling code",
                evidence="No bcrypt/argon2 usage detected",
                recommendation="Use bcrypt.hashpw() for password hashing",
                confidence=0.75
            ))
        
        return findings
    
    def _check_auth_security(self, code: str, lines: List[str]) -> List[Finding]:
        """Check authentication and session security."""
        findings = []
        
        # Check for session management issues
        has_session = any(re.search(r'session', line, re.IGNORECASE) for line in lines)
        has_expiration = any(re.search(r'expir|timeout|ttl', line, re.IGNORECASE) for line in lines)
        
        if has_session and not has_expiration:
            findings.append(Finding(
                severity=Severity.MEDIUM,
                finding_type="MISSING_SESSION_EXPIRATION",
                description="Session management found without expiration mechanism.",
                location="Session handling code",
                evidence="No session expiration detected",
                recommendation="Implement session timeout (e.g., 30 minutes of inactivity)",
                confidence=0.70
            ))
        
        # Check for input validation
        has_user_input = any(re.search(r'input\(|request\.|form\.|query\.|params', line) 
                            for line in lines)
        has_validation = any(re.search(r'validat|sanitiz|escape|clean', line, re.IGNORECASE) 
                            for line in lines)
        
        if has_user_input and not has_validation:
            findings.append(Finding(
                severity=Severity.MEDIUM,
                finding_type="MISSING_INPUT_VALIDATION",
                description="User input detected without validation. Can lead to various injection attacks.",
                location="Input handling code",
                evidence="No input validation detected",
                recommendation="Validate all user input: check type, length, format, and whitelist allowed characters",
                confidence=0.70
            ))
        
        return findings
    
    def _make_recommendation(self, findings: List[Finding]) -> str:
        """Override to provide security-specific recommendations."""
        has_critical = any(f.severity == Severity.CRITICAL for f in findings)
        has_high = any(f.severity == Severity.HIGH for f in findings)
        
        if has_critical:
            return "BLOCK"  # Critical security issues must be fixed
        elif has_high:
            return "BLOCK"  # High security issues should also block for security agent
        elif findings:
            return "APPROVE_WITH_CHANGES"
        else:
            return "APPROVE"


# Plugin factory function
def create_agent(message_bus: MessageBus) -> SecurityAgent:
    """
    Factory function to create agent instance.
    Called by framework when loading plugin.
    """
    return SecurityAgent(message_bus)
