"""
LLM Reasoning Agent - Probabilistic Reasoning Plugin
=====================================================

NOT A REPLACEMENT for deterministic agents.
ONE specialist plugin among many in the orchestrated system.

This agent uses Groq's Llama3 for probabilistic reasoning tasks:
- Abstract reasoning
- Natural language analysis
- Edge case exploration
- Hypothesis generation

Key Design Principles:
1. Low temperature (0.1-0.3) - reasoning, not creativity
2. Conservative confidence - never blindly trust LLM output
3. Graceful error handling - API failures don't crash system
4. Controlled influence - one voice among many agents
5. Performance monitoring - track latency impact

The LLM agent is invoked by the Coordinator alongside deterministic
agents. The system remains hybrid: deterministic + probabilistic.
"""

import os
import time
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

from agents.base_agent import BaseAgent
from core.models import Task, AgentResponse, Finding, Severity, AgentType
from core.message_bus import MessageBus


@dataclass
class LLMReasoningConfig:
    """Configuration for LLM reasoning behavior."""
    model: str = "llama3-70b-8192"
    temperature: float = 0.2  # Low temp = reasoning, not creativity
    max_tokens: int = 2048
    timeout: int = 30  # seconds
    retry_attempts: int = 2
    base_confidence: float = 0.65  # Conservative base confidence
    confidence_boost_per_iteration: float = 0.05
    max_confidence: float = 0.85  # Never too confident
    fallback_on_error: bool = True


class LLMReasoningAgent(BaseAgent):
    """
    Probabilistic reasoning agent using Groq LLM.
    
    This is ONE plugin in the multi-agent orchestration system.
    It provides probabilistic reasoning capabilities but does NOT
    replace deterministic agents.
    
    Design Philosophy:
    - Conservative confidence estimation
    - Graceful error handling with fallbacks
    - Performance monitoring
    - Controlled temperature for reasoning
    - Integration with existing agent framework
    """
    
    def __init__(
        self,
        agent_id: str,
        message_bus: MessageBus,
        api_key: Optional[str] = None,
        config: Optional[LLMReasoningConfig] = None
    ):
        """
        Initialize LLM reasoning agent.
        
        Args:
            agent_id: Unique agent identifier
            message_bus: Message bus for communication
            api_key: Groq API key (or set GROQ_API_KEY env var)
            config: Configuration for LLM behavior
        """
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.LLM_REASONING,
            message_bus=message_bus
        )
        
        self.config = config or LLMReasoningConfig()
        self.logger = logging.getLogger(f"{__name__}.{agent_id}")
        
        # Check Groq availability
        if not GROQ_AVAILABLE:
            self.logger.error(
                "Groq SDK not installed. Install with: pip install groq"
            )
            self.client = None
            self.available = False
            return
        
        # Get API key
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        if not self.api_key:
            self.logger.error(
                "Groq API key not found. Set GROQ_API_KEY environment variable "
                "or pass api_key parameter."
            )
            self.client = None
            self.available = False
            return
        
        # Initialize Groq client
        try:
            self.client = Groq(api_key=self.api_key)
            self.available = True
            self.logger.info(
                f"LLM reasoning agent initialized with model: {self.config.model}"
            )
        except Exception as e:
            self.logger.error(f"Failed to initialize Groq client: {e}")
            self.client = None
            self.available = False
        
        # Performance tracking
        self.call_count = 0
        self.total_latency = 0.0
        self.error_count = 0
        self.fallback_count = 0
    
    def _analyze(self, task: Task) -> List[Finding]:
        """
        Analyze task and return findings.
        
        This is the abstract method required by BaseAgent.
        We delegate to process_task for full LLM reasoning.
        
        Args:
            task: Task to analyze
            
        Returns:
            List of Finding objects
        """
        response = self.process_task(task, context={})
        return response.findings
    
    def process_task(self, task: Task, context: Dict[str, Any] = None) -> AgentResponse:
        """
        Process task using LLM reasoning.
        
        Args:
            task: Task to analyze
            context: Additional context (goal_id, iteration, etc.)
            
        Returns:
            AgentResponse with LLM-based findings
        """
        context = context or {}
        iteration = context.get('iteration', 1)
        
        self.logger.info(
            f"LLM reasoning agent processing task: {task.description[:50]}..."
        )
        
        # Check availability
        if not self.available or not self.client:
            return self._create_fallback_report(
                task,
                "LLM agent not available (API key or SDK missing)"
            )
        
        # Perform LLM reasoning with error handling
        start_time = time.time()
        
        try:
            findings = self._perform_reasoning(task, context)
            latency = time.time() - start_time
            
            # Convert findings to Finding objects
            finding_objects = [
                Finding(
                    severity=Severity.INFO,
                    finding_type="llm_analysis",
                    description=f,
                    confidence=confidence
                )
                for f in findings
            ]
            
            # Determine recommendation
            recommendation = self._determine_recommendation(findings, confidence)
            
            # Track performance
            self.call_count += 1
            self.total_latency += latency
            
            self.logger.info(
                f"LLM reasoning completed in {latency:.2f}s, "
                f"confidence: {confidence:.2f}"
            )
            
            return AgentResponse(
                agent_id=self.agent_id,
                agent_type=self.agent_type,
                task_id=task.task_id,
                status="COMPLETE",
                findings=finding_objects,
                confidence=confidence,
                summary=f"LLM-based probabilistic reasoning analysis",
                recommendation=recommendation,
                processing_time=latency
            )
            
        except Exception as e:
            latency = time.time() - start_time
            self.error_count += 1
            
            self.logger.error(
                f"LLM reasoning failed after {latency:.2f}s: {e}",
                exc_info=True
            )
            
            if self.config.fallback_on_error:
                self.fallback_count += 1
                return self._create_fallback_report(task, str(e))
            else:
                raise
    
    def _perform_reasoning(
        self,
        task: Task,
        context: Dict[str, Any]
    ) -> List[str]:
        """
        Perform LLM reasoning with retry logic.
        
        Args:
            task: Task to analyze
            context: Additional context
            
        Returns:
            List of findings from LLM
        """
        prompt = self._build_prompt(task, context)
        
        for attempt in range(self.config.retry_attempts):
            try:
                completion = self.client.chat.completions.create(
                    model=self.config.model,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a reasoning agent in a multi-agent system. "
                                "Provide clear, structured analysis. Be concise and specific. "
                                "Focus on reasoning, not creativity."
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens,
                    timeout=self.config.timeout
                )
                
                output = completion.choices[0].message.content.strip()
                
                # Parse output into structured findings
                findings = self._parse_llm_output(output)
                
                if not findings:
                    self.logger.warning("LLM returned empty findings")
                    findings = [
                        f"LLM analysis: {output[:200]}..."
                    ]
                
                return findings
                
            except Exception as e:
                self.logger.warning(
                    f"LLM API call failed (attempt {attempt + 1}/{self.config.retry_attempts}): {e}"
                )
                
                if attempt < self.config.retry_attempts - 1:
                    time.sleep(1)  # Brief delay before retry
                else:
                    raise
    
    def _build_prompt(self, task: Task, context: Dict[str, Any]) -> str:
        """
        Build prompt for LLM reasoning.
        
        Args:
            task: Task to analyze
            context: Additional context
            
        Returns:
            Formatted prompt string
        """
        goal_id = context.get('goal_id', 'unknown')
        iteration = context.get('iteration', 1)
        
        prompt = f"""Task Analysis Request

Goal: {goal_id}
Iteration: {iteration}

Task Description:
{task.description}

Your Role:
You are a reasoning agent in a multi-agent system. Other agents provide deterministic analysis. Your role is to provide probabilistic reasoning and explore edge cases.

Instructions:
1. Analyze the task from a reasoning perspective
2. Identify key challenges and considerations
3. Suggest potential approaches or solutions
4. Highlight edge cases or risks
5. Be concise and structured

Provide your analysis in the following format:
- Key Challenge: [main challenge]
- Approach: [suggested approach]
- Edge Cases: [potential issues]
- Recommendation: [your recommendation]
"""
        
        return prompt
    
    def _parse_llm_output(self, output: str) -> List[str]:
        """
        Parse LLM output into structured findings.
        
        Args:
            output: Raw LLM output
            
        Returns:
            List of structured findings
        """
        findings = []
        
        # Split by lines and extract structured information
        lines = output.strip().split('\n')
        current_finding = []
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_finding:
                    findings.append(' '.join(current_finding))
                    current_finding = []
            else:
                current_finding.append(line)
        
        # Add final finding
        if current_finding:
            findings.append(' '.join(current_finding))
        
        # Fallback to full output if parsing failed
        if not findings:
            findings = [output]
        
        return findings
    
    def _estimate_confidence(
        self,
        findings: List[str],
        iteration: int,
        latency: float
    ) -> float:
        """
        Estimate confidence in LLM reasoning.
        
        CRITICAL: Never blindly trust LLM output.
        Confidence is conservatively estimated based on:
        - Base confidence (conservative)
        - Iteration number (improves with context)
        - Output structure (well-formed = higher confidence)
        - Latency (too fast = suspicious, too slow = uncertain)
        
        Args:
            findings: LLM findings
            iteration: Current iteration number
            latency: API call latency
            
        Returns:
            Confidence score [0.0-1.0]
        """
        # Start with conservative base
        confidence = self.config.base_confidence
        
        # Boost confidence with iterations (more context)
        iteration_boost = min(
            iteration * self.config.confidence_boost_per_iteration,
            0.15  # Cap iteration boost at 15%
        )
        confidence += iteration_boost
        
        # Adjust based on output quality
        if findings:
            # Well-structured output (multiple findings)
            if len(findings) > 2:
                confidence += 0.05
            
            # Check for structured format (Key Challenge, Approach, etc.)
            output_text = ' '.join(findings).lower()
            structured_keywords = ['challenge', 'approach', 'edge case', 'recommendation']
            structure_score = sum(1 for kw in structured_keywords if kw in output_text)
            
            if structure_score >= 3:
                confidence += 0.05  # Well-structured response
            elif structure_score < 2:
                confidence -= 0.05  # Poorly structured
        else:
            # No findings = low confidence
            confidence -= 0.15
        
        # Adjust based on latency
        if latency < 1.0:
            # Too fast might indicate cached/generic response
            confidence -= 0.05
        elif latency > 20.0:
            # Very slow might indicate uncertainty or API issues
            confidence -= 0.05
        
        # Cap confidence at maximum
        confidence = min(confidence, self.config.max_confidence)
        
        # Floor confidence at reasonable minimum
        confidence = max(confidence, 0.45)
        
        return round(confidence, 2)
    
    def _determine_recommendation(
        self,
        findings: List[str],
        confidence: float
    ) -> str:
        """
        Determine recommendation based on findings and confidence.
        
        Args:
            findings: LLM findings
            confidence: Estimated confidence
            
        Returns:
            Recommendation string: "APPROVE", "APPROVE_WITH_CHANGES", or "BLOCK"
        """
        # LLM reasoning agent is cautious
        # It suggests improvements unless confidence is very high
        
        if confidence >= 0.80:
            return "APPROVE"
        elif confidence >= 0.65:
            return "APPROVE_WITH_CHANGES"
        else:
            return "BLOCK"
    
    def _create_fallback_report(
        self,
        task: Task,
        error_message: str
    ) -> AgentResponse:
        """
        Create fallback report when LLM reasoning fails.
        
        Args:
            task: Task that was being processed
            error_message: Error that occurred
            
        Returns:
            Neutral fallback AgentResponse
        """
        self.logger.warning(f"Creating fallback report due to: {error_message}")
        
        fallback_findings = [
            Finding(
                severity=Severity.INFO,
                finding_type="llm_unavailable",
                description=f"LLM reasoning unavailable: {error_message}",
                recommendation="Recommend review by other agents",
                confidence=0.50
            )
        ]
        
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type=self.agent_type,
            task_id=task.task_id,
            status="PARTIAL",
            findings=fallback_findings,
            confidence=0.50,  # Neutral confidence
            summary="Fallback due to LLM unavailability",
            recommendation="APPROVE_WITH_CHANGES",  # Neutral recommendation
            processing_time=0.0
        )
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """
        Get performance statistics for LLM agent.
        
        Returns:
            Dictionary with performance metrics
        """
        avg_latency = (
            self.total_latency / self.call_count
            if self.call_count > 0 else 0.0
        )
        
        error_rate = (
            self.error_count / self.call_count
            if self.call_count > 0 else 0.0
        )
        
        fallback_rate = (
            self.fallback_count / self.call_count
            if self.call_count > 0 else 0.0
        )
        
        return {
            'available': self.available,
            'call_count': self.call_count,
            'total_latency': round(self.total_latency, 2),
            'avg_latency': round(avg_latency, 2),
            'error_count': self.error_count,
            'error_rate': round(error_rate, 2),
            'fallback_count': self.fallback_count,
            'fallback_rate': round(fallback_rate, 2),
            'model': self.config.model,
            'temperature': self.config.temperature
        }
    
    def __repr__(self) -> str:
        status = "available" if self.available else "unavailable"
        return (
            f"LLMReasoningAgent(id={self.agent_id}, "
            f"model={self.config.model}, status={status})"
        )
