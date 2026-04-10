"""
Data models for AgentMesh multi-agent system.
Defines message structures and response formats.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum


class MessageType(Enum):
    """Types of messages exchanged between agents."""
    TASK_ASSIGN = "TASK_ASSIGN"
    TASK_RESULT = "TASK_RESULT"
    INFO_REQUEST = "INFO_REQUEST"
    INFO_RESPONSE = "INFO_RESPONSE"
    CONFLICT_DETECTED = "CONFLICT_DETECTED"
    RESOLUTION_COMPLETE = "RESOLUTION_COMPLETE"


class Severity(Enum):
    """Severity levels for findings."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class AgentType(Enum):
    """Types of agents in the system."""
    COORDINATOR = "COORDINATOR"
    SECURITY = "SECURITY"
    CODE_QUALITY = "CODE_QUALITY"
    PERFORMANCE = "PERFORMANCE"
    DOCUMENTATION = "DOCUMENTATION"
    LLM_REASONING = "LLM_REASONING"  # Probabilistic reasoning plugin
    OTHER = "OTHER"


class GoalStatus(Enum):
    """Status of a goal in the agentic loop."""
    PENDING = "PENDING"              # Goal created but not started
    IN_PROGRESS = "IN_PROGRESS"      # Currently working towards goal
    ACHIEVED = "ACHIEVED"            # Goal successfully achieved
    FAILED = "FAILED"                # Goal failed to achieve
    ABANDONED = "ABANDONED"          # Goal abandoned before completion
    REFINED = "REFINED"              # Goal refined and re-attempted


@dataclass
class Finding:
    """Represents a single issue found by an agent."""
    severity: Severity
    finding_type: str
    description: str
    location: Optional[str] = None
    evidence: Optional[str] = None
    recommendation: Optional[str] = None
    confidence: float = 0.0
    
    def __post_init__(self):
        """Validate finding data."""
        if not isinstance(self.severity, Severity):
            self.severity = Severity[self.severity]


@dataclass
class AgentResponse:
    """Response from a specialist agent after processing a task."""
    agent_id: str
    agent_type: AgentType
    task_id: str
    status: str  # "COMPLETE", "FAILED", "PARTIAL"
    findings: List[Finding] = field(default_factory=list)
    confidence: float = 0.0
    summary: str = ""
    recommendation: str = ""  # "APPROVE", "BLOCK", "APPROVE_WITH_CHANGES"
    processing_time: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Ensure agent_type is enum."""
        if not isinstance(self.agent_type, AgentType):
            self.agent_type = AgentType[self.agent_type]


@dataclass
class Message:
    """Message structure for agent communication."""
    message_id: str
    sender_id: str
    receiver_id: str
    message_type: MessageType
    timestamp: datetime
    payload: Dict[str, Any]
    priority: str = "NORMAL"  # "CRITICAL", "HIGH", "NORMAL", "LOW"
    
    def __post_init__(self):
        """Ensure message_type is enum."""
        if not isinstance(self.message_type, MessageType):
            self.message_type = MessageType[self.message_type]


@dataclass
class Task:
    """Task definition sent to agents - now domain-agnostic."""
    task_id: str
    description: str
    task_type: str = "code_review"  # Type of task: code_review, config_audit, log_analysis, etc.
    payload: Dict[str, Any] = field(default_factory=dict)  # Generic payload (code, config, logs, etc.)
    context: Optional[str] = None
    priority: str = "NORMAL"
    deadline_seconds: int = 60
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConflictRecord:
    """Record of a conflict and its resolution."""
    conflict_id: str
    timestamp: datetime
    agents_involved: List[str]
    conflict_type: str
    agent_responses: List[AgentResponse]
    resolution_strategy: str
    winner_agent_id: str
    reasoning: List[str]
    confidence: float
    scores: Dict[str, float] = field(default_factory=dict)


@dataclass
class FinalReport:
    """Final aggregated report returned to user."""
    task_id: str
    timestamp: datetime
    decision: str  # "APPROVE", "BLOCK", "APPROVE_WITH_CHANGES"
    confidence: float
    critical_findings: List[Finding]
    important_findings: List[Finding]
    minor_findings: List[Finding]
    positive_notes: List[str]
    recommendations: List[str]
    agent_responses: List[AgentResponse]
    conflicts_resolved: List[ConflictRecord]
    processing_time: float
    summary: str
    
    def to_formatted_string(self) -> str:
        """Format report as readable string."""
        lines = []
        lines.append("=" * 70)
        lines.append("           AGENTMESH CODE REVIEW REPORT")
        lines.append("=" * 70)
        lines.append(f"\nTask ID: {self.task_id}")
        lines.append(f"Timestamp: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"\nDECISION: {self.decision}")
        lines.append(f"Confidence: {self.confidence:.2%}")
        lines.append(f"Processing Time: {self.processing_time:.2f}s")
        lines.append("\n" + "=" * 70)
        
        # Critical findings
        if self.critical_findings:
            lines.append("\n🔴 CRITICAL FINDINGS (Must Fix)")
            lines.append("-" * 70)
            for finding in self.critical_findings:
                lines.append(f"\n• {finding.finding_type}")
                lines.append(f"  Location: {finding.location}")
                lines.append(f"  Issue: {finding.description}")
                if finding.recommendation:
                    lines.append(f"  Fix: {finding.recommendation}")
        
        # Important findings
        if self.important_findings:
            lines.append("\n\n🟡 IMPORTANT FINDINGS (Should Fix)")
            lines.append("-" * 70)
            for finding in self.important_findings:
                lines.append(f"\n• {finding.finding_type}")
                lines.append(f"  Issue: {finding.description}")
                if finding.recommendation:
                    lines.append(f"  Recommendation: {finding.recommendation}")
        
        # Minor findings
        if self.minor_findings:
            lines.append("\n\n🔵 MINOR IMPROVEMENTS (Nice to Have)")
            lines.append("-" * 70)
            for finding in self.minor_findings:
                lines.append(f"• {finding.description}")
        
        # Positive notes
        if self.positive_notes:
            lines.append("\n\n✅ WHAT WENT WELL")
            lines.append("-" * 70)
            for note in self.positive_notes:
                lines.append(f"• {note}")
        
        # Recommendations
        if self.recommendations:
            lines.append("\n\n📋 RECOMMENDATIONS")
            lines.append("-" * 70)
            for i, rec in enumerate(self.recommendations, 1):
                lines.append(f"{i}. {rec}")
        
        # Conflicts
        if self.conflicts_resolved:
            lines.append("\n\n⚖️  CONFLICTS RESOLVED")
            lines.append("-" * 70)
            for conflict in self.conflicts_resolved:
                lines.append(f"\nConflict: {conflict.conflict_type}")
                lines.append(f"Winner: {conflict.winner_agent_id}")
                lines.append(f"Reasoning: {', '.join(conflict.reasoning)}")
        
        lines.append("\n" + "=" * 70)
        lines.append(f"Review completed by {len(self.agent_responses)} specialist agents")
        lines.append("=" * 70)
        
        return "\n".join(lines)


@dataclass
class SuccessCriteria:
    """Defines success criteria for a goal."""
    min_confidence: float = 0.85          # Minimum confidence threshold
    max_conflicts: int = 0                # Maximum acceptable conflicts
    require_consensus: bool = False       # Require all agents to agree
    required_agent_types: List[str] = field(default_factory=list)  # Required agent types
    custom_checks: Dict[str, Any] = field(default_factory=dict)    # Custom validation


@dataclass
class GoalEvaluation:
    """Evaluation result for a goal iteration."""
    iteration: int
    timestamp: datetime
    goal_achieved: bool
    confidence_score: float
    conflicts_detected: int
    consensus_reached: bool
    findings_count: int
    agent_agreement_score: float  # 0.0-1.0: how much agents agree
    refinement_suggestions: List[str] = field(default_factory=list)
    stopping_reason: Optional[str] = None  # Why the loop stopped
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Goal:
    """
    Goal-driven task specification for autonomous agentic reasoning.
    Represents a high-level objective that may require multiple iterations.
    """
    goal_id: str
    description: str                              # High-level goal description
    success_criteria: SuccessCriteria             # How to determine success
    max_iterations: int = 5                       # Maximum refinement iterations
    current_iteration: int = 0                    # Current iteration count
    status: GoalStatus = GoalStatus.PENDING       # Current goal status
    
    # Task specification (what to analyze)
    task_type: str = "code_review"
    payload: Dict[str, Any] = field(default_factory=dict)
    context: Optional[str] = None
    priority: str = "NORMAL"
    
    # Execution tracking
    evaluation_history: List[GoalEvaluation] = field(default_factory=list)
    agent_responses_history: List[List[AgentResponse]] = field(default_factory=list)
    refinement_history: List[str] = field(default_factory=list)  # Tracking refinements
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def start(self):
        """Mark goal as started."""
        self.status = GoalStatus.IN_PROGRESS
        self.started_at = datetime.now()
        self.current_iteration = 0
    
    def complete(self, success: bool = True):
        """Mark goal as completed."""
        self.status = GoalStatus.ACHIEVED if success else GoalStatus.FAILED
        self.completed_at = datetime.now()
    
    def refine(self, refinement_note: str):
        """Mark goal for refinement."""
        self.refinement_history.append(f"[Iter {self.current_iteration}] {refinement_note}")
        self.status = GoalStatus.REFINED
    
    def abandon(self, reason: str):
        """Abandon goal."""
        self.status = GoalStatus.ABANDONED
        self.completed_at = datetime.now()
        self.metadata['abandonment_reason'] = reason
    
    def add_evaluation(self, evaluation: GoalEvaluation):
        """Add evaluation result from iteration."""
        self.evaluation_history.append(evaluation)
        self.current_iteration += 1
    
    def should_continue(self) -> bool:
        """Check if goal execution should continue."""
        if self.status in [GoalStatus.ACHIEVED, GoalStatus.FAILED, GoalStatus.ABANDONED]:
            return False
        if self.current_iteration >= self.max_iterations:
            return False
        return True
    
    def get_latest_evaluation(self) -> Optional[GoalEvaluation]:
        """Get the most recent evaluation."""
        return self.evaluation_history[-1] if self.evaluation_history else None


@dataclass
class AgentReport:
    """Simplified report from an agent (for backward compatibility)."""
    agent_id: str
    agent_type: AgentType
    decision: str  # "APPROVE", "BLOCK", "APPROVE_WITH_CHANGES"
    confidence: float
    findings: List[str] = field(default_factory=list)
    reasoning: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Ensure agent_type is enum."""
        if not isinstance(self.agent_type, AgentType):
            self.agent_type = AgentType[self.agent_type]


@dataclass
class GoalReport:
    """
    Final report from goal-driven execution.
    Extends FinalReport with goal-specific information.
    """
    goal_id: str
    goal_description: str
    goal_status: GoalStatus
    
    # Standard report fields
    task_id: str
    timestamp: datetime
    final_decision: str  # "APPROVE", "BLOCK", "APPROVE_WITH_CHANGES"
    confidence_score: float
    
    # Goal-specific fields
    iterations_completed: int
    goal_achieved: bool
    success_criteria_met: Dict[str, bool] = field(default_factory=dict)
    
    # Results
    agent_reports: List[AgentReport] = field(default_factory=list)
    evaluation_history: List[GoalEvaluation] = field(default_factory=list)
    refinement_history: List[str] = field(default_factory=list)
    
    # Conflict resolution
    conflicts_resolved: int = 0
    consensus_reached: bool = False
    
    # Performance
    total_processing_time: float = 0.0
    average_iteration_time: float = 0.0
    
    # Summary
    summary: str = ""
    recommendations: List[str] = field(default_factory=list)
    stopping_reason: str = ""
    
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Ensure goal_status is enum."""
        if not isinstance(self.goal_status, GoalStatus):
            self.goal_status = GoalStatus[self.goal_status]
