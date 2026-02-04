"""
Message Bus for AgentMesh.
Invisible infrastructure that logs and tracks agent communication.
"""

from typing import Dict, Optional, Any
from datetime import datetime
from core.models import Message, MessageType
import uuid


class MessageBus:
    """
    Lightweight message bus for agent communication.
    Provides logging and tracking without complex routing.
    """
    
    def __init__(self, logger=None):
        """
        Initialize the message bus.
        
        Args:
            logger: Optional logger instance for tracking messages
        """
        self.logger = logger
        self.agents = {}  # agent_id -> agent_instance
        self.message_log = []
        self.metrics = {
            "messages_sent": 0,
            "messages_received": 0,
            "total_agents": 0
        }
    
    def register_agent(self, agent_id: str, agent_instance: Any):
        """
        Register an agent with the message bus.
        
        Args:
            agent_id: Unique identifier for the agent
            agent_instance: The agent object
        """
        self.agents[agent_id] = agent_instance
        self.metrics["total_agents"] = len(self.agents)
        
        if self.logger:
            self.logger.log_custom("debug", f"Agent registered: {agent_id}")
    
    def unregister_agent(self, agent_id: str):
        """Remove an agent from the message bus."""
        if agent_id in self.agents:
            del self.agents[agent_id]
            self.metrics["total_agents"] = len(self.agents)
    
    def send_message(self, sender_id: str, receiver_id: str, 
                    message_type: MessageType, payload: Dict[str, Any],
                    priority: str = "NORMAL") -> str:
        """
        Log a message being sent between agents.
        
        Args:
            sender_id: ID of sending agent
            receiver_id: ID of receiving agent
            message_type: Type of message
            payload: Message data
            priority: Message priority
            
        Returns:
            message_id: Unique identifier for this message
        """
        message_id = str(uuid.uuid4())[:8]
        
        message = Message(
            message_id=message_id,
            sender_id=sender_id,
            receiver_id=receiver_id,
            message_type=message_type,
            timestamp=datetime.now(),
            payload=payload,
            priority=priority
        )
        
        self.message_log.append(message)
        self.metrics["messages_sent"] += 1
        
        if self.logger:
            self.logger.log_message(sender_id, receiver_id, message_type.value)
        
        return message_id
    
    def log_task_assignment(self, coordinator_id: str, agent_id: str, task_data: Dict[str, Any]):
        """Log a task being assigned to an agent."""
        return self.send_message(
            sender_id=coordinator_id,
            receiver_id=agent_id,
            message_type=MessageType.TASK_ASSIGN,
            payload=task_data,
            priority="HIGH"
        )
    
    def log_task_result(self, agent_id: str, coordinator_id: str, result_data: Dict[str, Any]):
        """Log a task result being returned."""
        return self.send_message(
            sender_id=agent_id,
            receiver_id=coordinator_id,
            message_type=MessageType.TASK_RESULT,
            payload=result_data,
            priority="NORMAL"
        )
    
    def get_message_log(self) -> list:
        """Get all logged messages."""
        return self.message_log
    
    def get_messages_by_agent(self, agent_id: str, direction: str = "both") -> list:
        """
        Get messages involving a specific agent.
        
        Args:
            agent_id: Agent to filter by
            direction: "sent", "received", or "both"
            
        Returns:
            List of messages
        """
        messages = []
        for msg in self.message_log:
            if direction in ["sent", "both"] and msg.sender_id == agent_id:
                messages.append(msg)
            elif direction in ["received", "both"] and msg.receiver_id == agent_id:
                messages.append(msg)
        return messages
    
    def get_metrics(self) -> Dict[str, int]:
        """Get message bus metrics."""
        return self.metrics.copy()
    
    def clear_logs(self):
        """Clear message log (useful for testing)."""
        self.message_log = []
        self.metrics["messages_sent"] = 0
        self.metrics["messages_received"] = 0
    
    def print_communication_log(self):
        """Print formatted communication log for debugging."""
        print("\n" + "=" * 70)
        print("COMMUNICATION LOG")
        print("=" * 70)
        
        for msg in self.message_log:
            timestamp = msg.timestamp.strftime("%H:%M:%S.%f")[:-3]
            print(f"[{timestamp}] {msg.sender_id} → {msg.receiver_id}")
            print(f"  Type: {msg.message_type.value}")
            print(f"  Priority: {msg.priority}")
            if "task_id" in msg.payload:
                print(f"  Task: {msg.payload['task_id']}")
            print()
        
        print("=" * 70)
        print(f"Total messages: {len(self.message_log)}")
        print(f"Registered agents: {len(self.agents)}")
        print("=" * 70)
