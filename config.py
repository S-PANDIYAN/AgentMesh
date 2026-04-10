"""
Configuration file for AgentMesh.
Contains all configurable parameters and thresholds.
"""
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Agent Configuration
AGENT_CONFIG = {
    "security_agent": {
        "enabled": True,
        "timeout_seconds": 60,
        "min_confidence_threshold": 0.70
    },
    "code_quality_agent": {
        "enabled": True,
        "timeout_seconds": 60,
        "min_confidence_threshold": 0.65
    },
    "performance_agent": {
        "enabled": True,
        "timeout_seconds": 60,
        "min_confidence_threshold": 0.65
    },
    "llm_reasoning_agent": {
        "enabled": True,
        "model": "llama3-70b-8192",
        "temperature": 0.2,  # Low temp for reasoning
        "max_tokens": 2048,
        "timeout_seconds": 30,
        "retry_attempts": 2,
        "base_confidence": 0.65,
        "confidence_boost_per_iteration": 0.05,
        "max_confidence": 0.85,  # Never too confident
        "fallback_on_error": True
    }
}

# Conflict Resolution Configuration
CONFLICT_RESOLUTION = {
    "score_weights": {
        "confidence": 0.4,
        "domain_expertise": 0.4,
        "evidence_quality": 0.2
    },
    "min_resolution_confidence": 0.60,
    "enable_meta_rules": True
}

# Decision Thresholds
DECISION_THRESHOLDS = {
    "block_on_critical": True,  # Always block if critical findings
    "block_on_high_security": True,  # Block on high security issues
    "approve_confidence_threshold": 0.70,  # Min confidence to approve
    "changes_required_on_medium": False  # Require changes for medium issues
}

# Severity Weights (for scoring)
SEVERITY_WEIGHTS = {
    "CRITICAL": 1.0,
    "HIGH": 0.8,
    "MEDIUM": 0.6,
    "LOW": 0.4,
    "INFO": 0.2
}

# Agent Selection Keywords
AGENT_SELECTION_KEYWORDS = {
    "security": [
        'security', 'auth', 'login', 'password', 'token',
        'session', 'encrypt', 'hash', 'sql', 'injection',
        'vulnerability', 'attack', 'breach'
    ],
    "code_quality": [
        'review', 'quality', 'bug', 'error', 'exception',
        'refactor', 'clean', 'maintain', 'structure',
        'naming', 'documentation'
    ],
    "performance": [
        'performance', 'slow', 'optimize', 'efficient',
        'query', 'loop', 'database', 'cache', 'speed',
        'memory', 'cpu'
    ]
}

# Logging Configuration
LOGGING_CONFIG = {
    "log_level": "INFO",  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    "log_dir": "logs",
    "console_output": True,
    "file_output": True,
    "save_events": True
}

# Task Configuration
TASK_CONFIG = {
    "default_priority": "NORMAL",
    "default_deadline_seconds": 60,
    "max_code_length": 10000,  # Max lines of code
    "enable_parallel_execution": True  # Future: true parallel
}

# Report Configuration
REPORT_CONFIG = {
    "max_findings_per_severity": 10,  # Limit findings shown
    "show_positive_notes": True,
    "show_conflict_details": True,
    "show_agent_stats": False,  # Don't clutter main report
    "include_evidence": True
}

# System Configuration
SYSTEM_CONFIG = {
    "max_agents": 3,
    "enable_conflict_resolution": True,
    "enable_aggregation": True,
    "save_task_history": True
}

# Demo Configuration
DEMO_CONFIG = {
    "use_sample_code": True,
    "verbose_output": True,
    "show_communication_log": False,
    "pause_between_steps": False
}

# File Paths
PATHS = {
    "logs": "logs",
    "history": "memory/history",
    "demo_scenarios": "demo/scenarios",
    "LOG_FILE": "./logs/agentmesh.log",
    "HISTORY_FILE": "./data/task_history.json"
}

# LLM Configuration
LLM_CONFIG = {
    "groq": {
        "api_key_env": "GROQ_API_KEY",  # Environment variable name
        "default_model": "llama-3.3-70b-versatile",
        "reasoning_temperature": 0.2,  # Low for reasoning
        "creative_temperature": 0.7,   # Higher for creative tasks
        "max_tokens": 2048,
        "timeout": 30,
        "retry_attempts": 2
    },
    "confidence": {
        "base": 0.65,  # Conservative starting point
        "boost_per_iteration": 0.05,
        "max": 0.85,  # Never too confident in LLM
        "min": 0.45   # Floor for fallback scenarios
    },
    "performance": {
        "max_latency_warning": 15.0,  # Warn if LLM takes > 15s
        "track_metrics": True
    }
}

# Color codes for console output (optional)
COLORS = {
    "CRITICAL": "\033[91m",  # Red
    "HIGH": "\033[93m",      # Yellow
    "MEDIUM": "\033[94m",    # Blue
    "LOW": "\033[92m",       # Green
    "RESET": "\033[0m",      # Reset
    "HEADER": "\033[95m",    # Purple
    "OKBLUE": "\033[94m",    # Blue
    "OKGREEN": "\033[92m",   # Green
    "WARNING": "\033[93m",   # Yellow
    "FAIL": "\033[91m",      # Red
    "ENDC": "\033[0m",       # Reset
    "BOLD": "\033[1m",       # Bold
    "UNDERLINE": "\033[4m"   # Underline
}
