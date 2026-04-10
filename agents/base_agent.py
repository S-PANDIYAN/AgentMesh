"""
Base Agent class for all specialist agents.
Provides common interface and functionality.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from datetime import datetime
import time

from core.models import AgentResponse, Task, Finding, Severity, AgentType, MessageType
from core.message_bus import MessageBus


class BaseAgent(ABC):
    """
    Abstract base class for all specialist agents.
    Defines common interface and shared functionality.
    """
    
    def __init__(self, agent_id: str, agent_type: AgentType, message_bus: MessageBus):
        """
        Initialize base agent.
        
        Args:
            agent_id: Unique identifier for this agent
            agent_type: Type of agent (SECURITY, CODE_QUALITY, PERFORMANCE)
            message_bus: Message bus for communication logging
        """
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.message_bus = message_bus
        
        # Register with message bus
        self.message_bus.register_agent(self.agent_id, self)
        
        # Track agent state
        self.tasks_completed = 0
        self.tasks_failed = 0
        self.total_processing_time = 0.0
    
    def process(self, task: Task) -> AgentResponse:
        """
        Process a task and return response.
        
        Args:
            task: Task to process
            
        Returns:
            AgentResponse with findings and recommendations
        """
        start_time = time.time()
        
        try:
            # Log task received
            self.message_bus.log_task_assignment(
                coordinator_id="coordinator",
                agent_id=self.agent_id,
                task_data={"task_id": task.task_id, "description": task.description}
            )
            
            # Call agent-specific analysis
            findings = self._analyze(task)
            
            # Calculate confidence based on findings
            confidence = self._calculate_confidence(findings)
            
            # Generate recommendation
            recommendation = self._make_recommendation(findings)
            
            # Generate summary
            summary = self._generate_summary(findings)
            
            processing_time = time.time() - start_time
            
            # Create response
            response = AgentResponse(
                agent_id=self.agent_id,
                agent_type=self.agent_type,
                task_id=task.task_id,
                status="COMPLETE",
                findings=findings,
                confidence=confidence,
                summary=summary,
                recommendation=recommendation,
                processing_time=processing_time,
                timestamp=datetime.now(),
                metadata={"tasks_completed": self.tasks_completed + 1}
            )
            
            # Log completion
            self.message_bus.log_task_result(
                agent_id=self.agent_id,
                coordinator_id="coordinator",
                result_data={
                    "task_id": task.task_id,
                    "status": "COMPLETE",
                    "findings_count": len(findings),
                    "confidence": confidence
                }
            )
            
            # Update stats
            self.tasks_completed += 1
            self.total_processing_time += processing_time
            
            return response
            
        except Exception as e:
            # Handle failure
            processing_time = time.time() - start_time
            self.tasks_failed += 1
            
            return AgentResponse(
                agent_id=self.agent_id,
                agent_type=self.agent_type,
                task_id=task.task_id,
                status="FAILED",
                findings=[],
                confidence=0.0,
                summary=f"Agent failed: {str(e)}",
                recommendation="BLOCK",
                processing_time=processing_time,
                timestamp=datetime.now(),
                metadata={"error": str(e)}
            )
    
    @abstractmethod
    def _analyze(self, task: Task) -> List[Finding]:
        """
        Agent-specific analysis logic.
        Must be implemented by each specialist agent.
        
        Args:
            task: Task to analyze
            
        Returns:
            List of findings
        """
        pass
    
    def _calculate_confidence(self, findings: List[Finding]) -> float:
        """
        Calculate overall confidence based on findings.
        
        Args:
            findings: List of findings
            
        Returns:
            Confidence score between 0 and 1
        """
        if not findings:
            return 0.5  # Medium confidence when no issues found
        
        # Average confidence of all findings
        total_confidence = sum(f.confidence for f in findings if f.confidence > 0)
        count = sum(1 for f in findings if f.confidence > 0)
        
        if count == 0:
            return 0.7  # Default confidence
        
        return total_confidence / count
    
    def _make_recommendation(self, findings: List[Finding]) -> str:
        """
        Make deployment recommendation based on findings.
        
        Args:
            findings: List of findings
            
        Returns:
            Recommendation: "APPROVE", "BLOCK", "APPROVE_WITH_CHANGES"
        """
        has_critical = any(f.severity == Severity.CRITICAL for f in findings)
        has_high = any(f.severity == Severity.HIGH for f in findings)
        
        if has_critical:
            return "BLOCK"
        elif has_high:
            return "APPROVE_WITH_CHANGES"
        else:
            return "APPROVE"
    
    def _generate_summary(self, findings: List[Finding]) -> str:
        """
        Generate summary of findings.
        
        Args:
            findings: List of findings
            
        Returns:
            Summary string
        """
        if not findings:
            return f"{self.agent_id} found no issues."
        
        # Count by severity
        severity_counts = {}
        for finding in findings:
            sev = finding.severity.value
            severity_counts[sev] = severity_counts.get(sev, 0) + 1
        
        parts = []
        for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            count = severity_counts.get(sev, 0)
            if count > 0:
                parts.append(f"{count} {sev}")
        
        return f"{self.agent_id} found: {', '.join(parts)} issues"
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics."""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type.value,
            "tasks_completed": self.tasks_completed,
            "tasks_failed": self.tasks_failed,
            "total_processing_time": self.total_processing_time,
            "avg_processing_time": (
                self.total_processing_time / self.tasks_completed 
                if self.tasks_completed > 0 else 0
            )
        }
    
    def __str__(self) -> str:
        return f"{self.agent_type.value}({self.agent_id})"
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.agent_id}>"
