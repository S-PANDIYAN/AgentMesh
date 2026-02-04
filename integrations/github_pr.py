"""
GitHub Pull Request Integration for AgentMesh
Automatically reviews PRs using multi-agent framework.
"""
import os
import sys
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

from github import Github, GithubException
from github.PullRequest import PullRequest
from github.Repository import Repository

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from framework_init import initialize_framework
from core.models import Task


class GitHubPRReviewer:
    """GitHub Pull Request reviewer using AgentMesh framework."""
    
    def __init__(self, github_token: Optional[str] = None):
        """
        Initialize GitHub PR reviewer.
        
        Args:
            github_token: GitHub personal access token (or use GITHUB_TOKEN env var)
        """
        # Initialize framework
        print("Initializing AgentMesh framework...")
        self.registry, self.loader, self.coordinator, self.logger = initialize_framework()
        print(f"✓ Loaded {len(self.registry.list_agents())} agents\n")
        
        # Initialize GitHub client
        token = github_token or os.getenv('GITHUB_TOKEN')
        if not token:
            raise ValueError("GitHub token required. Set GITHUB_TOKEN env var or pass github_token parameter.")
        
        self.github = Github(token)
        self.logger.info("GitHub client initialized")
    
    def review_pr(self, repo_name: str, pr_number: int, 
                  post_comments: bool = True, 
                  review_event: str = "COMMENT") -> Dict[str, Any]:
        """
        Review a GitHub pull request.
        
        Args:
            repo_name: Repository name in format "owner/repo"
            pr_number: Pull request number
            post_comments: Whether to post review comments to GitHub
            review_event: Review event type: COMMENT, APPROVE, or REQUEST_CHANGES
        
        Returns:
            Review results dictionary
        """
        try:
            # Get repository and PR
            repo = self.github.get_repo(repo_name)
            pr = repo.get_pull(pr_number)
            
            self.logger.info(f"Reviewing PR #{pr_number}: {pr.title}")
            print(f"\n{'='*70}")
            print(f"Reviewing PR #{pr_number}: {pr.title}")
            print(f"Repository: {repo_name}")
            print(f"Author: {pr.user.login}")
            print(f"{'='*70}\n")
            
            # Get PR diff
            files_changed = self._get_pr_files(pr)
            
            if not files_changed:
                self.logger.warning("No files to review")
                return {
                    'status': 'skipped',
                    'message': 'No files to review',
                    'pr_number': pr_number
                }
            
            print(f"Files changed: {len(files_changed)}")
            for file_info in files_changed:
                print(f"  - {file_info['filename']} ({file_info['status']}, +{file_info['additions']}/-{file_info['deletions']})")
            print()
            
            # Review each file
            all_findings = []
            file_reviews = []
            
            for file_info in files_changed:
                if file_info['status'] == 'removed':
                    continue
                
                print(f"Reviewing: {file_info['filename']}...")
                
                # Create review task
                task = Task(
                    task_id=f"pr-{pr_number}-{file_info['filename']}",
                    description=f"Review PR #{pr_number} file: {file_info['filename']}",
                    priority="HIGH",
                    task_type="code_review",
                    payload={
                        'code': file_info['content'],
                        'filename': file_info['filename'],
                        'patch': file_info.get('patch', ''),
                        'pr_number': pr_number,
                        'repo': repo_name
                    }
                )
                
                # Process review
                start_time = time.time()
                report = self.coordinator.process_task(task)
                processing_time = time.time() - start_time
                
                # Collect findings
                file_findings = []
                for agent_report in report.agent_reports:
                    for finding in agent_report.findings:
                        file_findings.append({
                            'agent': agent_report.agent_id,
                            'file': file_info['filename'],
                            'finding': finding,
                            'severity': self._get_severity(agent_report.agent_id, finding)
                        })
                
                file_reviews.append({
                    'filename': file_info['filename'],
                    'decision': report.final_decision,
                    'confidence': report.confidence_score,
                    'findings': file_findings,
                    'processing_time_ms': round(processing_time * 1000, 2)
                })
                
                all_findings.extend(file_findings)
                
                print(f"  Decision: {report.final_decision} ({report.confidence_score:.1f}% confidence)")
                print(f"  Findings: {len(file_findings)}")
                print(f"  Time: {processing_time*1000:.2f}ms\n")
            
            # Generate overall decision
            approve_count = sum(1 for r in file_reviews if r['decision'] == 'APPROVE')
            block_count = sum(1 for r in file_reviews if r['decision'] == 'BLOCK')
            
            if block_count > 0:
                overall_decision = "REQUEST_CHANGES"
                summary = f"Found {len(all_findings)} issues across {len(files_changed)} files. {block_count} files require changes."
            elif len(all_findings) > 0:
                overall_decision = review_event if review_event == "COMMENT" else "COMMENT"
                summary = f"Found {len(all_findings)} suggestions across {len(files_changed)} files."
            else:
                overall_decision = "APPROVE"
                summary = f"No issues found. All {len(files_changed)} files look good!"
            
            # Prepare result
            result = {
                'status': 'completed',
                'pr_number': pr_number,
                'repo': repo_name,
                'title': pr.title,
                'author': pr.user.login,
                'files_reviewed': len(files_changed),
                'overall_decision': overall_decision,
                'summary': summary,
                'total_findings': len(all_findings),
                'file_reviews': file_reviews,
                'findings': all_findings
            }
            
            # Post review to GitHub if requested
            if post_comments:
                self._post_review(pr, result, overall_decision)
            
            # Print summary
            print(f"\n{'='*70}")
            print("REVIEW SUMMARY")
            print(f"{'='*70}")
            print(f"Overall Decision: {overall_decision}")
            print(f"Total Findings: {len(all_findings)}")
            print(f"Files Reviewed: {len(files_changed)}")
            print(f"Summary: {summary}")
            print(f"{'='*70}\n")
            
            return result
            
        except GithubException as e:
            self.logger.error(f"GitHub API error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error reviewing PR: {e}")
            raise
    
    def _get_pr_files(self, pr: PullRequest) -> List[Dict[str, Any]]:
        """Get all files changed in PR with their content."""
        files = []
        
        for file in pr.get_files():
            # Skip non-code files
            if not self._is_code_file(file.filename):
                continue
            
            file_info = {
                'filename': file.filename,
                'status': file.status,  # added, modified, removed
                'additions': file.additions,
                'deletions': file.deletions,
                'patch': file.patch if hasattr(file, 'patch') else '',
                'content': ''
            }
            
            # Get file content (for non-removed files)
            if file.status != 'removed':
                try:
                    # Get content from PR head
                    content = pr.head.repo.get_contents(file.filename, ref=pr.head.sha)
                    if hasattr(content, 'decoded_content'):
                        file_info['content'] = content.decoded_content.decode('utf-8')
                except:
                    # If file not accessible, use patch
                    file_info['content'] = file.patch if hasattr(file, 'patch') else ''
            
            files.append(file_info)
        
        return files
    
    def _is_code_file(self, filename: str) -> bool:
        """Check if file is a code file worth reviewing."""
        code_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h',
            '.cs', '.go', '.rs', '.php', '.rb', '.swift', '.kt', '.scala',
            '.sql', '.sh', '.bash', '.yaml', '.yml', '.json', '.xml'
        }
        
        # Skip common non-code files
        skip_patterns = [
            'package-lock.json', 'yarn.lock', '.min.js', '.bundle.js',
            '.gitignore', 'LICENSE', 'README'
        ]
        
        if any(pattern in filename for pattern in skip_patterns):
            return False
        
        ext = Path(filename).suffix.lower()
        return ext in code_extensions
    
    def _get_severity(self, agent_id: str, finding: str) -> str:
        """Determine severity level based on agent and finding content."""
        finding_lower = finding.lower()
        
        # Security issues are high severity
        if 'security' in agent_id.lower():
            if any(word in finding_lower for word in ['critical', 'injection', 'vulnerability', 'exploit']):
                return 'HIGH'
            return 'MEDIUM'
        
        # Performance issues
        if 'performance' in agent_id.lower():
            if any(word in finding_lower for word in ['slow', 'inefficient', 'bottleneck']):
                return 'MEDIUM'
            return 'LOW'
        
        # Code quality issues
        return 'LOW'
    
    def _post_review(self, pr: PullRequest, result: Dict[str, Any], event: str):
        """Post review comments to GitHub PR."""
        try:
            # Build review body
            body_parts = [
                "## 🤖 AgentMesh Automated Review\n",
                f"**Decision:** {result['overall_decision']}",
                f"**Summary:** {result['summary']}\n",
                f"**Files Reviewed:** {result['files_reviewed']}",
                f"**Total Findings:** {result['total_findings']}\n"
            ]
            
            # Add findings by severity
            high_findings = [f for f in result['findings'] if f['severity'] == 'HIGH']
            medium_findings = [f for f in result['findings'] if f['severity'] == 'MEDIUM']
            low_findings = [f for f in result['findings'] if f['severity'] == 'LOW']
            
            if high_findings:
                body_parts.append(f"### 🔴 High Severity Issues ({len(high_findings)})\n")
                for finding in high_findings[:10]:  # Limit to 10
                    body_parts.append(f"- **{finding['file']}**: {finding['finding']} _{finding['agent']}_")
                if len(high_findings) > 10:
                    body_parts.append(f"_...and {len(high_findings)-10} more_\n")
            
            if medium_findings:
                body_parts.append(f"\n### 🟡 Medium Severity Issues ({len(medium_findings)})\n")
                for finding in medium_findings[:5]:  # Limit to 5
                    body_parts.append(f"- **{finding['file']}**: {finding['finding']} _{finding['agent']}_")
                if len(medium_findings) > 5:
                    body_parts.append(f"_...and {len(medium_findings)-5} more_\n")
            
            if low_findings:
                body_parts.append(f"\n### 🔵 Low Severity Issues ({len(low_findings)})\n")
                for finding in low_findings[:3]:  # Limit to 3
                    body_parts.append(f"- **{finding['file']}**: {finding['finding']} _{finding['agent']}_")
                if len(low_findings) > 3:
                    body_parts.append(f"_...and {len(low_findings)-3} more_\n")
            
            # Add agents consulted
            agents_used = set(f['agent'] for f in result['findings'])
            if agents_used:
                body_parts.append(f"\n**Agents Consulted:** {', '.join(agents_used)}")
            
            body = "\n".join(body_parts)
            
            # Post review
            pr.create_review(
                body=body,
                event=event  # COMMENT, APPROVE, or REQUEST_CHANGES
            )
            
            print(f"✓ Posted review to GitHub PR #{result['pr_number']}")
            
        except Exception as e:
            self.logger.error(f"Error posting review: {e}")
            print(f"✗ Failed to post review: {e}")
    
    def watch_repository(self, repo_name: str, auto_review: bool = True):
        """
        Watch a repository for new PRs and automatically review them.
        
        Args:
            repo_name: Repository name in format "owner/repo"
            auto_review: Automatically review new PRs
        """
        print(f"Watching repository: {repo_name}")
        print("Press Ctrl+C to stop\n")
        
        try:
            repo = self.github.get_repo(repo_name)
            reviewed_prs = set()
            
            while True:
                # Get open PRs
                prs = repo.get_pulls(state='open', sort='created', direction='desc')
                
                for pr in prs[:10]:  # Check last 10 open PRs
                    if pr.number not in reviewed_prs:
                        print(f"\n🔔 New PR detected: #{pr.number} - {pr.title}")
                        
                        if auto_review:
                            try:
                                self.review_pr(repo_name, pr.number, post_comments=True)
                                reviewed_prs.add(pr.number)
                            except Exception as e:
                                print(f"✗ Error reviewing PR #{pr.number}: {e}")
                
                # Wait before checking again
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            print("\n\nStopped watching repository.")
        except Exception as e:
            self.logger.error(f"Error watching repository: {e}")
            raise


def main():
    """CLI for GitHub PR reviewer."""
    import argparse
    
    parser = argparse.ArgumentParser(description='AgentMesh GitHub PR Reviewer')
    parser.add_argument('repo', help='Repository name (owner/repo)')
    parser.add_argument('pr_number', type=int, help='Pull request number')
    parser.add_argument('--token', help='GitHub token (or use GITHUB_TOKEN env var)')
    parser.add_argument('--no-post', action='store_true', help='Do not post comments to GitHub')
    parser.add_argument('--event', choices=['COMMENT', 'APPROVE', 'REQUEST_CHANGES'],
                       default='COMMENT', help='Review event type')
    
    args = parser.parse_args()
    
    # Create reviewer
    reviewer = GitHubPRReviewer(github_token=args.token)
    
    # Review PR
    result = reviewer.review_pr(
        args.repo,
        args.pr_number,
        post_comments=not args.no_post,
        review_event=args.event
    )
    
    # Exit with appropriate code
    if result['overall_decision'] == 'REQUEST_CHANGES':
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
