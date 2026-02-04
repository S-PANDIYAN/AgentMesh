"""
Logging infrastructure for AgentMesh.
Centralized logging for all agent communications and events.
"""

import logging
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path
import json


class AgentMeshLogger:
    """Central logging system for all agent activities."""
    
    def __init__(self, log_dir: str = "logs", log_level: str = "INFO"):
        """
        Initialize the logger.
        
        Args:
            log_dir: Directory to store log files
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Setup main logger
        self.logger = logging.getLogger("AgentMesh")
        self.logger.setLevel(getattr(logging, log_level))
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        
        # File handler
        log_file = self.log_dir / f"agentmesh_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_format)
        
        # Add handlers
        if not self.logger.handlers:
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)
        
        # Event log for structured data
        self.events = []
    
    def log_task_received(self, task_id: str, description: str):
        """Log when a new task is received."""
        self.logger.info(f"📥 Task received: {task_id}")
        self.logger.debug(f"Description: {description}")
        self._add_event("TASK_RECEIVED", {"task_id": task_id, "description": description})
    
    def log_task_decomposed(self, task_id: str, subtasks: int):
        """Log task decomposition."""
        self.logger.info(f"📋 Task decomposed into {subtasks} subtasks")
        self._add_event("TASK_DECOMPOSED", {"task_id": task_id, "subtasks": subtasks})
    
    def log_agent_assigned(self, agent_id: str, task_id: str):
        """Log agent assignment."""
        self.logger.info(f"👤 {agent_id} assigned to task {task_id}")
        self._add_event("AGENT_ASSIGNED", {"agent_id": agent_id, "task_id": task_id})
    
    def log_agent_started(self, agent_id: str):
        """Log when agent starts processing."""
        self.logger.debug(f"▶️  {agent_id} started processing")
        self._add_event("AGENT_STARTED", {"agent_id": agent_id})
    
    def log_agent_completed(self, agent_id: str, findings_count: int, confidence: float):
        """Log agent completion."""
        self.logger.info(f"✅ {agent_id} completed: {findings_count} findings (confidence: {confidence:.2%})")
        self._add_event("AGENT_COMPLETED", {
            "agent_id": agent_id,
            "findings_count": findings_count,
            "confidence": confidence
        })
    
    def log_agent_failed(self, agent_id: str, error: str):
        """Log agent failure."""
        self.logger.error(f"❌ {agent_id} failed: {error}")
        self._add_event("AGENT_FAILED", {"agent_id": agent_id, "error": error})
    
    def log_conflict_detected(self, agents: list, conflict_type: str):
        """Log conflict detection."""
        self.logger.warning(f"⚠️  Conflict detected: {conflict_type} between {', '.join(agents)}")
        self._add_event("CONFLICT_DETECTED", {
            "agents": agents,
            "conflict_type": conflict_type
        })
    
    def log_conflict_resolved(self, winner_agent: str, reasoning: str):
        """Log conflict resolution."""
        self.logger.info(f"⚖️  Conflict resolved: {winner_agent} won")
        self.logger.debug(f"Reasoning: {reasoning}")
        self._add_event("CONFLICT_RESOLVED", {
            "winner_agent": winner_agent,
            "reasoning": reasoning
        })
    
    def log_report_generated(self, task_id: str, decision: str, processing_time: float):
        """Log final report generation."""
        self.logger.info(f"📊 Report generated: {decision} (took {processing_time:.2f}s)")
        self._add_event("REPORT_GENERATED", {
            "task_id": task_id,
            "decision": decision,
            "processing_time": processing_time
        })
    
    def log_message(self, sender: str, receiver: str, message_type: str):
        """Log message passing between agents."""
        self.logger.debug(f"💬 {sender} → {receiver}: {message_type}")
        self._add_event("MESSAGE_SENT", {
            "sender": sender,
            "receiver": receiver,
            "message_type": message_type
        })
    
    def log_custom(self, level: str, message: str, data: Optional[Dict[str, Any]] = None):
        """Log custom message with optional structured data."""
        log_func = getattr(self.logger, level.lower())
        log_func(message)
        if data:
            self._add_event("CUSTOM", {"message": message, "data": data})
    
    def _add_event(self, event_type: str, data: Dict[str, Any]):
        """Add structured event to event log."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "data": data
        }
        self.events.append(event)
    
    def get_events(self) -> list:
        """Get all logged events."""
        return self.events
    
    def save_events(self, filename: Optional[str] = None):
        """Save events to JSON file."""
        if filename is None:
            filename = f"events_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = self.log_dir / filename
        with open(filepath, 'w') as f:
            json.dump(self.events, f, indent=2)
        
        self.logger.info(f"Events saved to {filepath}")
    
    def print_summary(self):
        """Print summary of logged events."""
        event_counts = {}
        for event in self.events:
            event_type = event["event_type"]
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        print("\n" + "=" * 50)
        print("EVENT SUMMARY")
        print("=" * 50)
        for event_type, count in sorted(event_counts.items()):
            print(f"{event_type:25} : {count:3}")
        print("=" * 50)
