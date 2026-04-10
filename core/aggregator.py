"""
Report Aggregator for AgentMesh.
Combines agent responses into comprehensive final report.
"""

from typing import List, Optional
from datetime import datetime

from core.models import (
    AgentResponse, FinalReport, Finding, Severity, 
    ConflictRecord
)


class ReportAggregator:
    """
    Aggregates agent responses into a comprehensive final report.
    Organizes findings by severity and generates recommendations.
    """
    
    def __init__(self, logger=None):
        """
        Initialize report aggregator.
        
        Args:
            logger: Optional logger for tracking aggregation
        """
        self.logger = logger
    
    def aggregate(self, 
                  task_id: str,
                  agent_responses: List[AgentResponse],
                  conflicts_resolved: Optional[List[ConflictRecord]] = None,
                  processing_time: float = 0.0) -> FinalReport:
        """
        Aggregate agent responses into final report.
        
        Args:
            task_id: Task identifier
            agent_responses: List of agent responses
            conflicts_resolved: Optional list of resolved conflicts
            processing_time: Total processing time
            
        Returns:
            FinalReport with aggregated findings
        """
        # Collect all findings from all agents
        all_findings = []
        for response in agent_responses:
            all_findings.extend(response.findings)
        
        # Organize by severity
        critical_findings = [f for f in all_findings if f.severity == Severity.CRITICAL]
        high_findings = [f for f in all_findings if f.severity == Severity.HIGH]
        medium_findings = [f for f in all_findings if f.severity == Severity.MEDIUM]
        low_findings = [f for f in all_findings if f.severity == Severity.LOW]
        
        # Combine important findings
        important_findings = high_findings + medium_findings
        minor_findings = low_findings
        
        # Make final decision
        decision = self._make_final_decision(agent_responses, conflicts_resolved)
        
        # Calculate overall confidence
        overall_confidence = self._calculate_overall_confidence(
            agent_responses, 
            conflicts_resolved
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            critical_findings,
            important_findings,
            minor_findings
        )
        
        # Generate positive notes
        positive_notes = self._generate_positive_notes(agent_responses, all_findings)
        
        # Generate summary
        summary = self._generate_summary(decision, all_findings, agent_responses)
        
        # Create final report
        report = FinalReport(
            task_id=task_id,
            timestamp=datetime.now(),
            decision=decision,
            confidence=overall_confidence,
            critical_findings=critical_findings,
            important_findings=important_findings,
            minor_findings=minor_findings,
            positive_notes=positive_notes,
            recommendations=recommendations,
            agent_responses=agent_responses,
            conflicts_resolved=conflicts_resolved or [],
            processing_time=processing_time,
            summary=summary
        )
        
        if self.logger:
            self.logger.log_report_generated(task_id, decision, processing_time)
        
        return report
    
    def _make_final_decision(self, 
                            agent_responses: List[AgentResponse],
                            conflicts_resolved: Optional[List[ConflictRecord]]) -> str:
        """
        Make final deployment decision based on agent responses.
        
        Args:
            agent_responses: List of agent responses
            conflicts_resolved: Resolved conflicts (if any)
            
        Returns:
            Decision: "APPROVE", "BLOCK", or "APPROVE_WITH_CHANGES"
        """
        # If conflicts were resolved, use winner's recommendation
        if conflicts_resolved:
            # Get the winning agent's response
            latest_conflict = conflicts_resolved[-1]
            winner_response = next(
                r for r in agent_responses 
                if r.agent_id == latest_conflict.winner_agent_id
            )
            return winner_response.recommendation
        
        # Otherwise, use majority voting with priority to BLOCK
        recommendations = [r.recommendation for r in agent_responses]
        
        # If any agent says BLOCK, we block (conservative approach)
        if "BLOCK" in recommendations:
            return "BLOCK"
        
        # If any agent says APPROVE_WITH_CHANGES
        if "APPROVE_WITH_CHANGES" in recommendations:
            return "APPROVE_WITH_CHANGES"
        
        # All approve
        return "APPROVE"
    
    def _calculate_overall_confidence(self,
                                     agent_responses: List[AgentResponse],
                                     conflicts_resolved: Optional[List[ConflictRecord]]) -> float:
        """
        Calculate overall confidence in the final decision.
        
        Args:
            agent_responses: List of agent responses
            conflicts_resolved: Resolved conflicts
            
        Returns:
            Confidence score between 0 and 1
        """
        # If conflicts exist, use resolution confidence
        if conflicts_resolved:
            # Average resolution confidences
            resolution_confidences = [c.confidence for c in conflicts_resolved]
            return sum(resolution_confidences) / len(resolution_confidences)
        
        # Otherwise, average agent confidences
        agent_confidences = [r.confidence for r in agent_responses]
        if not agent_confidences:
            return 0.5
        
        return sum(agent_confidences) / len(agent_confidences)
    
    def _generate_recommendations(self,
                                 critical_findings: List[Finding],
                                 important_findings: List[Finding],
                                 minor_findings: List[Finding]) -> List[str]:
        """
        Generate prioritized recommendations.
        
        Args:
            critical_findings: Critical severity findings
            important_findings: High/Medium severity findings
            minor_findings: Low severity findings
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        # Phase 1: Critical issues
        if critical_findings:
            recommendations.append(
                f"PHASE 1 (CRITICAL - Must fix before deployment):"
            )
            for i, finding in enumerate(critical_findings[:3], 1):  # Top 3
                recommendations.append(
                    f"  {i}. {finding.finding_type}: {finding.recommendation}"
                )
            if len(critical_findings) > 3:
                recommendations.append(f"  ... and {len(critical_findings) - 3} more critical issues")
        
        # Phase 2: Important issues
        if important_findings:
            recommendations.append(
                f"PHASE 2 (IMPORTANT - Should fix before production):"
            )
            for i, finding in enumerate(important_findings[:5], 1):  # Top 5
                recommendations.append(
                    f"  {i}. {finding.finding_type}: {finding.recommendation}"
                )
            if len(important_findings) > 5:
                recommendations.append(f"  ... and {len(important_findings) - 5} more issues")
        
        # Phase 3: Improvements
        if minor_findings:
            recommendations.append(
                f"PHASE 3 (IMPROVEMENTS - Nice to have):"
            )
            recommendations.append(
                f"  Address {len(minor_findings)} minor code quality improvements"
            )
        
        return recommendations
    
    def _generate_positive_notes(self, 
                                agent_responses: List[AgentResponse],
                                all_findings: List[Finding]) -> List[str]:
        """
        Generate positive notes about what went well.
        
        Args:
            agent_responses: List of agent responses
            all_findings: All findings
            
        Returns:
            List of positive note strings
        """
        positive_notes = []
        
        # Check what wasn't found
        finding_types = {f.finding_type for f in all_findings}
        
        # Security positives
        if "SQL_INJECTION" not in finding_types:
            positive_notes.append("No SQL injection vulnerabilities detected")
        
        if "HARDCODED_SECRET" not in finding_types:
            positive_notes.append("No hardcoded secrets found")
        
        # Code quality positives
        if "BARE_EXCEPT" not in finding_types:
            positive_notes.append("Proper exception handling used")
        
        # Performance positives
        if "N_PLUS_ONE_QUERY" not in finding_types:
            positive_notes.append("No N+1 query problems detected")
        
        # If very few findings overall
        if len(all_findings) <= 3:
            positive_notes.append("Code is generally well-written with minimal issues")
        
        # Check for explicit positive patterns
        for response in agent_responses:
            if response.confidence > 0.85 and len(response.findings) == 0:
                positive_notes.append(
                    f"{response.agent_id} found no issues (high confidence review)"
                )
        
        return positive_notes if positive_notes else ["Code has been reviewed by multiple specialist agents"]
    
    def _generate_summary(self,
                         decision: str,
                         all_findings: List[Finding],
                         agent_responses: List[AgentResponse]) -> str:
        """
        Generate executive summary.
        
        Args:
            decision: Final decision
            all_findings: All findings
            agent_responses: Agent responses
            
        Returns:
            Summary string
        """
        # Count by severity
        critical_count = sum(1 for f in all_findings if f.severity == Severity.CRITICAL)
        high_count = sum(1 for f in all_findings if f.severity == Severity.HIGH)
        medium_count = sum(1 for f in all_findings if f.severity == Severity.MEDIUM)
        low_count = sum(1 for f in all_findings if f.severity == Severity.LOW)
        
        # Build summary
        parts = []
        
        if decision == "BLOCK":
            parts.append("⛔ DEPLOYMENT BLOCKED.")
        elif decision == "APPROVE_WITH_CHANGES":
            parts.append("⚠️  APPROVED WITH CHANGES REQUIRED.")
        else:
            parts.append("✅ APPROVED FOR DEPLOYMENT.")
        
        # Add finding counts
        if critical_count > 0:
            parts.append(f"{critical_count} CRITICAL issue(s) found.")
        if high_count > 0:
            parts.append(f"{high_count} HIGH severity issue(s) found.")
        if medium_count > 0:
            parts.append(f"{medium_count} MEDIUM issue(s) found.")
        if low_count > 0:
            parts.append(f"{low_count} LOW priority improvement(s) suggested.")
        
        if not all_findings:
            parts.append("No issues found.")
        
        # Add agent participation
        parts.append(f"Reviewed by {len(agent_responses)} specialist agent(s).")
        
        return " ".join(parts)
    
    def get_findings_by_agent(self, 
                             report: FinalReport,
                             agent_id: str) -> List[Finding]:
        """
        Get all findings from a specific agent.
        
        Args:
            report: Final report
            agent_id: Agent identifier
            
        Returns:
            List of findings from that agent
        """
        for response in report.agent_responses:
            if response.agent_id == agent_id:
                return response.findings
        return []
    
    def get_statistics(self, report: FinalReport) -> dict:
        """
        Get statistics about the report.
        
        Args:
            report: Final report
            
        Returns:
            Dictionary of statistics
        """
        all_findings = (
            report.critical_findings + 
            report.important_findings + 
            report.minor_findings
        )
        
        return {
            "total_findings": len(all_findings),
            "critical_count": len(report.critical_findings),
            "high_count": len([f for f in report.important_findings if f.severity == Severity.HIGH]),
            "medium_count": len([f for f in report.important_findings if f.severity == Severity.MEDIUM]),
            "low_count": len(report.minor_findings),
            "agents_participated": len(report.agent_responses),
            "conflicts_resolved": len(report.conflicts_resolved),
            "processing_time": report.processing_time,
            "decision": report.decision,
            "confidence": report.confidence
        }
