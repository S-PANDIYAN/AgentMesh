"""
Agent Registry for AgentMesh Framework.
Generic plugin system for registering and managing specialist agents.
"""

from typing import Dict, List, Optional, Type, Any
from core.models import AgentType


class AgentRegistry:
    """
    Central registry for managing specialist agents.
    Enables plugin-based architecture where agents can be dynamically registered.
    """
    
    def __init__(self):
        """Initialize the agent registry."""
        self._agents: Dict[str, Any] = {}  # agent_id -> agent_instance
        self._agents_by_type: Dict[AgentType, List[Any]] = {}
        self._capabilities: Dict[str, List[str]] = {}  # agent_id -> capability keywords
        self._capability_weights: Dict[str, Dict[str, float]] = {}  # agent_id -> {keyword: weight}
        self._agent_priorities: Dict[str, int] = {}  # agent_id -> priority (higher = more important)
    
    def register(self, agent_instance: Any, capabilities: List[str] = None, 
                 capability_weights: Dict[str, float] = None, priority: int = 5) -> None:
        """
        Register a specialist agent with the framework.
        
        Args:
            agent_instance: The agent to register (must have agent_id and agent_type)
            capabilities: Optional list of capability keywords for agent selection
            capability_weights: Optional weights for keywords (0.0-1.0, default 1.0)
            priority: Agent priority level (1-10, default 5, higher = more important)
        """
        if not hasattr(agent_instance, 'agent_id'):
            raise ValueError("Agent must have 'agent_id' attribute")
        
        if not hasattr(agent_instance, 'agent_type'):
            raise ValueError("Agent must have 'agent_type' attribute")
        
        agent_id = agent_instance.agent_id
        agent_type = agent_instance.agent_type
        
        # Register agent
        self._agents[agent_id] = agent_instance
        
        # Register by type
        if agent_type not in self._agents_by_type:
            self._agents_by_type[agent_type] = []
        self._agents_by_type[agent_type].append(agent_instance)
        
        # Register capabilities
        if capabilities:
            self._capabilities[agent_id] = capabilities
            
            # Register weights (default 1.0 for all)
            if capability_weights:
                self._capability_weights[agent_id] = capability_weights
            else:
                self._capability_weights[agent_id] = {cap: 1.0 for cap in capabilities}
        
        # Register priority
        self._agent_priorities[agent_id] = max(1, min(10, priority))
    
    def unregister(self, agent_id: str) -> None:
        """
        Remove an agent from the registry.
        
        Args:
            agent_id: ID of agent to remove
        """
        if agent_id in self._agents:
            agent = self._agents[agent_id]
            agent_type = agent.agent_type
            
            # Remove from main registry
            del self._agents[agent_id]
            
            # Remove from type registry
            if agent_type in self._agents_by_type:
                self._agents_by_type[agent_type] = [
                    a for a in self._agents_by_type[agent_type] 
                    if a.agent_id != agent_id
                ]
            
            # Remove capabilities
            if agent_id in self._capabilities:
                del self._capabilities[agent_id]
    
    def get_agent(self, agent_id: str) -> Optional[Any]:
        """
        Get agent by ID.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            Agent instance or None
        """
        return self._agents.get(agent_id)
    
    def get_agents_by_type(self, agent_type: AgentType) -> List[Any]:
        """
        Get all agents of a specific type.
        
        Args:
            agent_type: Type of agents to retrieve
            
        Returns:
            List of agent instances
        """
        return self._agents_by_type.get(agent_type, [])
    
    def get_all_specialists(self) -> List[Any]:
        """
        Get all registered specialist agents.
        
        Returns:
            List of all registered agents
        """
        return list(self._agents.values())
    
    def select_agents_by_capabilities(self, keywords: List[str]) -> List[Any]:
        """
        Select agents based on capability keywords.
        
        Args:
            keywords: List of keywords to match against agent capabilities
            
        Returns:
            List of matching agents
        """
        selected = []
        keywords_lower = [k.lower() for k in keywords]
        
        for agent_id, capabilities in self._capabilities.items():
            capabilities_lower = [c.lower() for c in capabilities]
            
            # Check if any keyword matches any capability
            if any(keyword in capabilities_lower for keyword in keywords_lower):
                agent = self._agents.get(agent_id)
                if agent and agent not in selected:
                    selected.append(agent)
        
        return selected
    
    def auto_select_agents(self, task_text: str, use_weighted: bool = False, 
                          min_score: float = 0.0) -> List[Any]:
        """
        Automatically select agents based on task content.
        Uses keyword matching against registered capabilities.
        
        Args:
            task_text: Combined text from task description and content
            use_weighted: Use weighted matching (considers keyword importance)
            min_score: Minimum match score to include agent (0.0-1.0)
            
        Returns:
            List of selected agents, sorted by match score if weighted
        """
        if use_weighted:
            return self._weighted_select(task_text, min_score)
        
        text_lower = task_text.lower()
        selected = []
        
        for agent_id, capabilities in self._capabilities.items():
            # Check if any capability keyword appears in task text
            if any(cap.lower() in text_lower for cap in capabilities):
                agent = self._agents.get(agent_id)
                if agent and agent not in selected:
                    selected.append(agent)
        
        # If no agents matched, return all specialists
        return selected if selected else self.get_all_specialists()
    
    def _weighted_select(self, task_text: str, min_score: float = 0.0) -> List[Any]:
        """
        Select agents using weighted keyword matching.
        
        Args:
            task_text: Task content
            min_score: Minimum score threshold
            
        Returns:
            List of agents sorted by relevance score
        """
        text_lower = task_text.lower()
        agent_scores = []
        
        for agent_id, capabilities in self._capabilities.items():
            score = 0.0
            matches = 0
            weights = self._capability_weights.get(agent_id, {})
            
            for cap in capabilities:
                if cap.lower() in text_lower:
                    weight = weights.get(cap, 1.0)
                    score += weight
                    matches += 1
            
            if matches > 0:
                # Normalize by number of matches and apply priority boost
                priority = self._agent_priorities.get(agent_id, 5)
                priority_multiplier = priority / 5.0  # 5 is default
                normalized_score = (score / matches) * priority_multiplier
                
                if normalized_score >= min_score:
                    agent = self._agents.get(agent_id)
                    if agent:
                        agent_scores.append((agent, normalized_score))
        
        # Sort by score (highest first)
        agent_scores.sort(key=lambda x: x[1], reverse=True)
        selected = [agent for agent, score in agent_scores]
        
        # If no agents matched, return all specialists
        return selected if selected else self.get_all_specialists()
    
    def get_agent_count(self) -> int:
        """Get total number of registered agents."""
        return len(self._agents)
    
    def get_agent_types(self) -> List[AgentType]:
        """Get list of all registered agent types."""
        return list(self._agents_by_type.keys())
    
    def clear(self) -> None:
        """Clear all registered agents."""
        self._agents.clear()
        self._agents_by_type.clear()
        self._capabilities.clear()
    
    def get_registry_info(self) -> Dict[str, Any]:
        """
        Get information about registered agents.
        
        Returns:
            Dictionary with registry statistics
        """
        return {
            'total_agents': len(self._agents),
            'agent_types': [t.value if hasattr(t, 'value') else str(t) for t in self._agents_by_type.keys()],
            'agents': [
                {
                    'agent_id': agent.agent_id,
                    'agent_type': agent.agent_type.value if hasattr(agent.agent_type, 'value') else str(agent.agent_type),
                    'capabilities': self._capabilities.get(agent.agent_id, [])
                }
                for agent in self._agents.values()
            ]
        }
