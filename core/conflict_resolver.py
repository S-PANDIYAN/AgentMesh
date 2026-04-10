"""
Conflict Resolver for AgentMesh.
Resolves disagreements between agents using confidence-based scoring.
"""

from typing import List, Dict, Optional
from datetime import datetime
import uuid

from core.models import AgentResponse, ConflictRecord, AgentType, Severity


class ConflictResolver:
    """
    Resolves conflicts when agents provide contradictory recommendations.
    Uses multi-factor scoring: confidence + domain expertise + evidence quality.
    """
    
    def __init__(self, logger=None):
        """
        Initialize conflict resolver.
        
        Args:
            logger: Optional logger for tracking resolution decisions
        """
        self.logger = logger
        
        # Domain expertise weights for different conflict types
        self.domain_expertise = {
            AgentType.SECURITY: {
                "security": 1.0,
                "authentication": 1.0,
                "deployment": 0.8,
                "performance": 0.3,
                "code_quality": 0.5
            },
            AgentType.CODE_QUALITY: {
                "security": 0.5,
                "authentication": 0.4,
                "deployment": 0.6,
                "performance": 0.6,
                "code_quality": 1.0
            },
            AgentType.PERFORMANCE: {
                "security": 0.3,
                "authentication": 0.3,
                "deployment": 0.7,
                "performance": 1.0,
                "code_quality": 0.6
            }
        }
        
        # Weight configuration for scoring
        self.score_weights = {
            "confidence": 0.4,
            "domain_expertise": 0.4,
            "evidence_quality": 0.2
        }
    
    def detect_conflicts(self, agent_responses: List[AgentResponse]) -> bool:
        """
        Detect if agents have conflicting recommendations.
        
        Args:
            agent_responses: List of agent responses
            
        Returns:
            True if conflicts detected, False otherwise
        """
        if len(agent_responses) < 2:
            return False
        
        recommendations = [r.recommendation for r in agent_responses]
        
        # Conflict exists if we have both APPROVE and BLOCK
        has_approve = any(r in ["APPROVE", "APPROVE_WITH_CHANGES"] for r in recommendations)
        has_block = any(r == "BLOCK" for r in recommendations)
        
        return has_approve and has_block
    
    def resolve(self, agent_responses: List[AgentResponse], 
                conflict_domain: str = "deployment") -> ConflictRecord:
        """
        Resolve conflict between agents using multi-factor scoring.
        
        Args:
            agent_responses: List of conflicting agent responses
            conflict_domain: Domain of conflict (security, performance, etc.)
            
        Returns:
            ConflictRecord with resolution details
        """
        if self.logger:
            agent_ids = [r.agent_id for r in agent_responses]
            self.logger.log_conflict_detected(agent_ids, conflict_domain)
        
        # Calculate scores for each agent
        scores = {}
        for response in agent_responses:
            score = self._calculate_agent_score(response, conflict_domain)
            scores[response.agent_id] = score
        
        # Find winner (highest score)
        winner_id = max(scores, key=scores.get)
        winner_response = next(r for r in agent_responses if r.agent_id == winner_id)
        
        # Generate reasoning
        reasoning = self._generate_reasoning(
            winner_response, 
            agent_responses, 
            scores, 
            conflict_domain
        )
        
        # Calculate overall confidence in resolution
        resolution_confidence = self._calculate_resolution_confidence(scores)
        
        # Create conflict record
        conflict_record = ConflictRecord(
            conflict_id=str(uuid.uuid4())[:8],
            timestamp=datetime.now(),
            agents_involved=[r.agent_id for r in agent_responses],
            conflict_type=f"{conflict_domain.upper()}_RECOMMENDATION",
            agent_responses=agent_responses,
            resolution_strategy="MULTI_FACTOR_SCORING",
            winner_agent_id=winner_id,
            reasoning=reasoning,
            confidence=resolution_confidence,
            scores=scores
        )
        
        if self.logger:
            self.logger.log_conflict_resolved(winner_id, "; ".join(reasoning))
        
        return conflict_record
    
    def _calculate_agent_score(self, response: AgentResponse, 
                               conflict_domain: str) -> float:
        """
        Calculate score for an agent's response.
        
        Args:
            response: Agent response
            conflict_domain: Domain of conflict
            
        Returns:
            Score between 0 and 1
        """
        # Factor 1: Agent's confidence
        confidence_score = response.confidence
        
        # Factor 2: Domain expertise
        expertise_score = self.domain_expertise.get(
            response.agent_type, {}
        ).get(conflict_domain, 0.5)
        
        # Factor 3: Evidence quality (based on findings)
        evidence_score = self._calculate_evidence_quality(response)
        
        # Weighted combination
        total_score = (
            confidence_score * self.score_weights["confidence"] +
            expertise_score * self.score_weights["domain_expertise"] +
            evidence_score * self.score_weights["evidence_quality"]
        )
        
        return total_score
    
    def _calculate_evidence_quality(self, response: AgentResponse) -> float:
        """
        Calculate evidence quality based on findings.
        
        Args:
            response: Agent response
            
        Returns:
            Evidence quality score between 0 and 1
        """
        if not response.findings:
            return 0.5  # Neutral score when no findings
        
        # Weight by severity
        severity_weights = {
            Severity.CRITICAL: 1.0,
            Severity.HIGH: 0.8,
            Severity.MEDIUM: 0.6,
            Severity.LOW: 0.4,
            Severity.INFO: 0.2
        }
        
        total_weight = 0
        total_confidence = 0
        
        for finding in response.findings:
            weight = severity_weights.get(finding.severity, 0.5)
            total_weight += weight
            total_confidence += finding.confidence * weight
        
        if total_weight == 0:
            return 0.5
        
        return min(total_confidence / total_weight, 1.0)
    
    def _generate_reasoning(self, winner: AgentResponse, 
                           all_responses: List[AgentResponse],
                           scores: Dict[str, float],
                           conflict_domain: str) -> List[str]:
        """
        Generate human-readable reasoning for the resolution.
        
        Args:
            winner: Winning agent response
            all_responses: All agent responses
            scores: Calculated scores
            conflict_domain: Domain of conflict
            
        Returns:
            List of reasoning statements
        """
        reasoning = []
        
        # Winner and score
        winner_score = scores[winner.agent_id]
        reasoning.append(f"{winner.agent_id} has highest score: {winner_score:.3f}")
        
        # Score comparison
        other_scores = [s for aid, s in scores.items() if aid != winner.agent_id]
        if other_scores:
            max_other = max(other_scores)
            score_diff = winner_score - max_other
            if score_diff > 0.2:
                reasoning.append(f"Significant score advantage: {score_diff:.3f}")
            else:
                reasoning.append(f"Close decision: margin of {score_diff:.3f}")
        
        # Domain expertise
        expertise = self.domain_expertise.get(winner.agent_type, {}).get(conflict_domain, 0.5)
        if expertise >= 0.8:
            reasoning.append(f"High domain expertise in {conflict_domain}: {expertise:.2f}")
        
        # Severity of findings
        critical_findings = [f for f in winner.findings if f.severity == Severity.CRITICAL]
        high_findings = [f for f in winner.findings if f.severity == Severity.HIGH]
        
        if critical_findings:
            reasoning.append(f"Found {len(critical_findings)} CRITICAL issue(s)")
        if high_findings:
            reasoning.append(f"Found {len(high_findings)} HIGH severity issue(s)")
        
        # Meta-rule application
        if winner.agent_type == AgentType.SECURITY and (critical_findings or high_findings):
            reasoning.append("Meta-rule: Security concerns override other considerations")
        
        return reasoning
    
    def _calculate_resolution_confidence(self, scores: Dict[str, float]) -> float:
        """
        Calculate confidence in the resolution decision.
        
        Args:
            scores: Agent scores
            
        Returns:
            Confidence score between 0 and 1
        """
        if len(scores) < 2:
            return 0.5
        
        sorted_scores = sorted(scores.values(), reverse=True)
        winner_score = sorted_scores[0]
        runner_up_score = sorted_scores[1]
        
        # Large gap = high confidence
        gap = winner_score - runner_up_score
        
        # Convert gap to confidence
        # Gap of 0.3 or more = 0.95 confidence
        # Gap of 0.0 = 0.50 confidence (toss-up)
        confidence = 0.5 + min(gap / 0.3, 1.0) * 0.45
        
        return confidence
    
    def get_resolution_summary(self, conflict_record: ConflictRecord) -> str:
        """
        Generate a summary of the conflict resolution.
        
        Args:
            conflict_record: Conflict record
            
        Returns:
            Formatted summary string
        """
        lines = []
        lines.append(f"Conflict: {conflict_record.conflict_type}")
        lines.append(f"Agents involved: {', '.join(conflict_record.agents_involved)}")
        lines.append(f"Winner: {conflict_record.winner_agent_id}")
        lines.append(f"Confidence: {conflict_record.confidence:.2%}")
        lines.append(f"Reasoning:")
        for reason in conflict_record.reasoning:
            lines.append(f"  - {reason}")
        
        return "\n".join(lines)
