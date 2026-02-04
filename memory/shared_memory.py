"""
Shared Memory System for AgentMesh
===================================

Enables stateful agentic reasoning by providing:
- Persistent memory across iterations
- Agent output history
- Conflict tracking
- Confidence progression
- Intermediate insights storage
- Context retrieval for informed decision-making

Thread-safe with multiple storage backend support.
"""

import threading
import json
import pickle
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
from dataclasses import dataclass, field, asdict
from pathlib import Path
from collections import defaultdict


@dataclass
class MemoryEntry:
    """Single memory entry for a goal iteration."""
    goal_id: str
    iteration: int
    timestamp: datetime
    agent_outputs: List[Dict[str, Any]] = field(default_factory=list)
    conflicts: List[Dict[str, Any]] = field(default_factory=list)
    confidence_score: float = 0.0
    refinements: List[str] = field(default_factory=list)
    insights: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryEntry':
        """Create from dictionary."""
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)


@dataclass
class MemoryQuery:
    """Query parameters for memory retrieval."""
    goal_id: Optional[str] = None
    min_confidence: Optional[float] = None
    max_conflicts: Optional[int] = None
    agent_types: Optional[List[str]] = None
    keywords: Optional[List[str]] = None
    limit: int = 10
    
    def matches(self, entry: MemoryEntry) -> bool:
        """Check if entry matches query criteria."""
        if self.goal_id and entry.goal_id != self.goal_id:
            return False
        
        if self.min_confidence and entry.confidence_score < self.min_confidence:
            return False
        
        if self.max_conflicts is not None and len(entry.conflicts) > self.max_conflicts:
            return False
        
        if self.agent_types:
            entry_agent_types = {
                output.get('agent_type', '') 
                for output in entry.agent_outputs
            }
            if not any(atype in entry_agent_types for atype in self.agent_types):
                return False
        
        if self.keywords:
            entry_text = json.dumps(entry.to_dict()).lower()
            if not any(kw.lower() in entry_text for kw in self.keywords):
                return False
        
        return True


class SharedMemory:
    """
    Shared memory store for agentic reasoning.
    
    Enables agents to:
    - Read previous outputs from past iterations
    - Write reasoning and insights
    - Track task history
    - Build collaborative understanding
    
    Thread-safe with automatic locking.
    """
    
    def __init__(self, max_entries_per_goal: int = 100):
        """
        Initialize shared memory.
        
        Args:
            max_entries_per_goal: Maximum entries to keep per goal (LRU eviction)
        """
        self._memory: Dict[str, List[MemoryEntry]] = defaultdict(list)
        self._lock = threading.RLock()
        self._max_entries = max_entries_per_goal
        self._access_count = defaultdict(int)
        self._total_entries = 0
    
    def store(self, entry: MemoryEntry) -> None:
        """
        Store a memory entry.
        
        Args:
            entry: Memory entry to store
        """
        with self._lock:
            entries = self._memory[entry.goal_id]
            entries.append(entry)
            
            # LRU eviction if exceeds limit
            if len(entries) > self._max_entries:
                entries.pop(0)
            
            self._total_entries += 1
    
    def get(self, goal_id: str) -> List[MemoryEntry]:
        """
        Retrieve all memory entries for a goal.
        
        Args:
            goal_id: Goal identifier
            
        Returns:
            List of memory entries, ordered by iteration
        """
        with self._lock:
            self._access_count[goal_id] += 1
            return list(self._memory.get(goal_id, []))
    
    def get_latest(self, goal_id: str, count: int = 1) -> List[MemoryEntry]:
        """
        Get the most recent N entries for a goal.
        
        Args:
            goal_id: Goal identifier
            count: Number of recent entries to retrieve
            
        Returns:
            List of most recent entries
        """
        with self._lock:
            entries = self._memory.get(goal_id, [])
            return entries[-count:] if entries else []
    
    def get_context(self, goal_id: str) -> Dict[str, Any]:
        """
        Get summarized context for a goal.
        
        Provides:
        - All agent outputs from previous iterations
        - Conflict history
        - Confidence progression
        - All refinements applied
        - Accumulated insights
        
        Args:
            goal_id: Goal identifier
            
        Returns:
            Dictionary with contextualized information
        """
        with self._lock:
            entries = self._memory.get(goal_id, [])
            
            if not entries:
                return {
                    "iterations": 0,
                    "agent_outputs": [],
                    "conflicts": [],
                    "confidence_history": [],
                    "refinements": [],
                    "insights": {},
                    "last_iteration": None
                }
            
            # Aggregate information
            all_outputs = []
            all_conflicts = []
            confidence_history = []
            all_refinements = []
            merged_insights = {}
            
            for entry in entries:
                all_outputs.extend(entry.agent_outputs)
                all_conflicts.extend(entry.conflicts)
                confidence_history.append({
                    'iteration': entry.iteration,
                    'confidence': entry.confidence_score,
                    'timestamp': entry.timestamp.isoformat()
                })
                all_refinements.extend(entry.refinements)
                merged_insights.update(entry.insights)
            
            return {
                "iterations": len(entries),
                "agent_outputs": all_outputs,
                "conflicts": all_conflicts,
                "confidence_history": confidence_history,
                "refinements": all_refinements,
                "insights": merged_insights,
                "last_iteration": entries[-1].iteration,
                "last_confidence": entries[-1].confidence_score
            }
    
    def query(self, query: MemoryQuery) -> List[MemoryEntry]:
        """
        Query memory with filtering criteria.
        
        Args:
            query: Query parameters
            
        Returns:
            List of matching entries
        """
        with self._lock:
            results = []
            
            # Search through all goals or specific goal
            goals_to_search = (
                [query.goal_id] if query.goal_id 
                else list(self._memory.keys())
            )
            
            for goal_id in goals_to_search:
                entries = self._memory.get(goal_id, [])
                for entry in entries:
                    if query.matches(entry):
                        results.append(entry)
                        if len(results) >= query.limit:
                            return results
            
            return results
    
    def get_similar_goals(
        self, 
        current_goal_id: str, 
        min_confidence: float = 0.80,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find similar goals with high confidence for learning.
        
        Args:
            current_goal_id: Current goal identifier
            min_confidence: Minimum confidence threshold
            limit: Maximum results to return
            
        Returns:
            List of similar goal summaries
        """
        with self._lock:
            similar = []
            
            for goal_id, entries in self._memory.items():
                if goal_id == current_goal_id:
                    continue
                
                # Find entries with high confidence
                high_confidence_entries = [
                    e for e in entries 
                    if e.confidence_score >= min_confidence
                ]
                
                if high_confidence_entries:
                    # Get the best entry
                    best_entry = max(
                        high_confidence_entries,
                        key=lambda e: e.confidence_score
                    )
                    
                    similar.append({
                        'goal_id': goal_id,
                        'confidence': best_entry.confidence_score,
                        'iterations': len(entries),
                        'refinements': best_entry.refinements,
                        'insights': best_entry.insights,
                        'agent_outputs': best_entry.agent_outputs
                    })
                    
                    if len(similar) >= limit:
                        break
            
            # Sort by confidence
            similar.sort(key=lambda x: x['confidence'], reverse=True)
            return similar
    
    def add_insight(self, goal_id: str, key: str, value: Any) -> None:
        """
        Add an insight to the most recent entry for a goal.
        
        Args:
            goal_id: Goal identifier
            key: Insight key
            value: Insight value
        """
        with self._lock:
            entries = self._memory.get(goal_id, [])
            if entries:
                entries[-1].insights[key] = value
    
    def get_insight(self, goal_id: str, key: str) -> Optional[Any]:
        """
        Retrieve a specific insight from the most recent entry.
        
        Args:
            goal_id: Goal identifier
            key: Insight key
            
        Returns:
            Insight value or None
        """
        with self._lock:
            entries = self._memory.get(goal_id, [])
            if entries:
                return entries[-1].insights.get(key)
            return None
    
    def get_confidence_trend(self, goal_id: str) -> List[float]:
        """
        Get confidence score progression for a goal.
        
        Args:
            goal_id: Goal identifier
            
        Returns:
            List of confidence scores in order
        """
        with self._lock:
            entries = self._memory.get(goal_id, [])
            return [e.confidence_score for e in entries]
    
    def has_repeated_conflicts(
        self, 
        goal_id: str, 
        threshold: int = 2
    ) -> bool:
        """
        Check if conflicts are repeating across iterations.
        
        Args:
            goal_id: Goal identifier
            threshold: Number of occurrences to consider repeated
            
        Returns:
            True if conflicts are repeating
        """
        with self._lock:
            entries = self._memory.get(goal_id, [])
            if len(entries) < threshold:
                return False
            
            # Count conflict patterns
            conflict_signatures = defaultdict(int)
            for entry in entries[-threshold:]:
                for conflict in entry.conflicts:
                    # Create signature from conflict type and agents
                    sig = f"{conflict.get('type', '')}:{','.join(sorted(conflict.get('agents', [])))}"
                    conflict_signatures[sig] += 1
            
            # Check if any conflict pattern repeats
            return any(count >= threshold for count in conflict_signatures.values())
    
    def get_successful_refinements(
        self, 
        goal_id: str,
        confidence_improvement: float = 0.05
    ) -> List[str]:
        """
        Identify refinements that led to confidence improvements.
        
        Args:
            goal_id: Goal identifier
            confidence_improvement: Minimum improvement threshold
            
        Returns:
            List of successful refinement descriptions
        """
        with self._lock:
            entries = self._memory.get(goal_id, [])
            if len(entries) < 2:
                return []
            
            successful = []
            for i in range(1, len(entries)):
                prev_conf = entries[i-1].confidence_score
                curr_conf = entries[i].confidence_score
                
                if curr_conf - prev_conf >= confidence_improvement:
                    successful.extend(entries[i-1].refinements)
            
            return successful
    
    def clear(self, goal_id: Optional[str] = None) -> None:
        """
        Clear memory entries.
        
        Args:
            goal_id: Specific goal to clear, or None to clear all
        """
        with self._lock:
            if goal_id:
                if goal_id in self._memory:
                    del self._memory[goal_id]
                    if goal_id in self._access_count:
                        del self._access_count[goal_id]
            else:
                self._memory.clear()
                self._access_count.clear()
                self._total_entries = 0
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get memory statistics.
        
        Returns:
            Dictionary with memory stats
        """
        with self._lock:
            return {
                'total_goals': len(self._memory),
                'total_entries': sum(len(entries) for entries in self._memory.values()),
                'total_stored': self._total_entries,
                'avg_entries_per_goal': (
                    sum(len(e) for e in self._memory.values()) / len(self._memory)
                    if self._memory else 0
                ),
                'most_accessed_goal': (
                    max(self._access_count.items(), key=lambda x: x[1])[0]
                    if self._access_count else None
                ),
                'memory_size_bytes': sum(
                    len(json.dumps(e.to_dict())) 
                    for entries in self._memory.values() 
                    for e in entries
                )
            }
    
    def save(self, filepath: str) -> None:
        """
        Save memory to file.
        
        Args:
            filepath: Path to save file
        """
        with self._lock:
            path = Path(filepath)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert to serializable format
            data = {
                'memory': {
                    goal_id: [entry.to_dict() for entry in entries]
                    for goal_id, entries in self._memory.items()
                },
                'access_count': dict(self._access_count),
                'total_entries': self._total_entries,
                'saved_at': datetime.now().isoformat()
            }
            
            # Save as JSON
            if filepath.endswith('.json'):
                with open(filepath, 'w') as f:
                    json.dump(data, f, indent=2)
            # Save as pickle for faster loading
            else:
                with open(filepath, 'wb') as f:
                    pickle.dump(data, f)
    
    def load(self, filepath: str) -> None:
        """
        Load memory from file.
        
        Args:
            filepath: Path to load file
        """
        with self._lock:
            path = Path(filepath)
            if not path.exists():
                raise FileNotFoundError(f"Memory file not found: {filepath}")
            
            # Load based on file type
            if filepath.endswith('.json'):
                with open(filepath, 'r') as f:
                    data = json.load(f)
            else:
                with open(filepath, 'rb') as f:
                    data = pickle.load(f)
            
            # Restore memory
            self._memory.clear()
            for goal_id, entries_data in data['memory'].items():
                self._memory[goal_id] = [
                    MemoryEntry.from_dict(entry_data)
                    for entry_data in entries_data
                ]
            
            self._access_count = defaultdict(int, data.get('access_count', {}))
            self._total_entries = data.get('total_entries', 0)
    
    def __len__(self) -> int:
        """Return total number of entries."""
        with self._lock:
            return sum(len(entries) for entries in self._memory.values())
    
    def __contains__(self, goal_id: str) -> bool:
        """Check if goal has memory entries."""
        with self._lock:
            return goal_id in self._memory and len(self._memory[goal_id]) > 0
