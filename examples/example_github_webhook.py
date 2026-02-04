"""
Example: GitHub Pull Request Auto-Review
Demonstrates how to automatically review GitHub PRs using AgentMesh.
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from integrations.github_pr import GitHubPRReviewer


def example_1_review_specific_pr():
    """Example 1: Review a specific PR."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Review Specific Pull Request")
    print("="*70 + "\n")
    
    # Set your GitHub token
    # Get token from: https://github.com/settings/tokens
    # Required permissions: repo (for private repos) or public_repo (for public repos)
    github_token = os.getenv('GITHUB_TOKEN')
    
    if not github_token:
        print("ERROR: GITHUB_TOKEN environment variable not set")
        print("Please set it with: export GITHUB_TOKEN='your_token_here'")
        return
    
    # Initialize reviewer
    reviewer = GitHubPRReviewer(github_token=github_token)
    
    # Review a PR (replace with actual repo and PR number)
    repo_name = "owner/repository"  # e.g., "microsoft/vscode"
    pr_number = 1234
    
    print(f"Reviewing PR #{pr_number} in {repo_name}...")
    print("(Replace with actual repo and PR number)\n")
    
    try:
        result = reviewer.review_pr(
            repo_name=repo_name,
            pr_number=pr_number,
            post_comments=False,  # Set to True to post review to GitHub
            review_event="COMMENT"  # COMMENT, APPROVE, or REQUEST_CHANGES
        )
        
        # Print summary
        print("\n" + "-"*70)
        print("REVIEW SUMMARY")
        print("-"*70)
        print(f"PR: #{result['pr_number']} - {result['title']}")
        print(f"Author: {result['author']}")
        print(f"Files Reviewed: {result['files_reviewed']}")
        print(f"Total Findings: {result['total_findings']}")
        print(f"Decision: {result['overall_decision']}")
        print(f"Summary: {result['summary']}")
        
        # Print findings by file
        if result['file_reviews']:
            print("\nFindings by File:")
            for file_review in result['file_reviews']:
                print(f"\n  {file_review['filename']}:")
                print(f"    Decision: {file_review['decision']}")
                print(f"    Confidence: {file_review['confidence']:.1f}%")
                print(f"    Findings: {len(file_review['findings'])}")
                print(f"    Time: {file_review['processing_time_ms']}ms")
        
    except Exception as e:
        print(f"Error: {e}")


def example_2_review_without_posting():
    """Example 2: Review PR without posting comments."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Review Without Posting Comments")
    print("="*70 + "\n")
    
    github_token = os.getenv('GITHUB_TOKEN')
    
    if not github_token:
        print("ERROR: GITHUB_TOKEN not set")
        return
    
    reviewer = GitHubPRReviewer(github_token=github_token)
    
    # Review PR without posting
    print("Reviewing PR locally (no comments posted to GitHub)...\n")
    
    result = reviewer.review_pr(
        repo_name="owner/repo",
        pr_number=1,
        post_comments=False  # Only analyze, don't post
    )
    
    print(f"Analysis complete: {result['total_findings']} findings")


def example_3_auto_approve_or_request_changes():
    """Example 3: Automatically approve or request changes."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Auto-Approve or Request Changes")
    print("="*70 + "\n")
    
    github_token = os.getenv('GITHUB_TOKEN')
    
    if not github_token:
        print("ERROR: GITHUB_TOKEN not set")
        return
    
    reviewer = GitHubPRReviewer(github_token=github_token)
    
    # Review and post with appropriate event
    print("Reviewing PR and posting review...\n")
    
    result = reviewer.review_pr(
        repo_name="owner/repo",
        pr_number=1,
        post_comments=True,
        review_event="COMMENT"  # Will auto-change to REQUEST_CHANGES if issues found
    )
    
    if result['overall_decision'] == 'REQUEST_CHANGES':
        print("❌ PR requires changes before merge")
    elif result['overall_decision'] == 'APPROVE':
        print("✅ PR approved - looks good to merge")
    else:
        print("💬 PR reviewed - comments posted")


def example_4_watch_repository():
    """Example 4: Watch repository for new PRs."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Watch Repository for New PRs")
    print("="*70 + "\n")
    
    github_token = os.getenv('GITHUB_TOKEN')
    
    if not github_token:
        print("ERROR: GITHUB_TOKEN not set")
        return
    
    reviewer = GitHubPRReviewer(github_token=github_token)
    
    # Watch repository
    print("Starting repository watch...")
    print("Will automatically review new PRs as they are created")
    print("Press Ctrl+C to stop\n")
    
    try:
        reviewer.watch_repository(
            repo_name="owner/repo",
            auto_review=True  # Automatically review new PRs
        )
    except KeyboardInterrupt:
        print("\nStopped watching repository")


def example_5_batch_review_open_prs():
    """Example 5: Review all open PRs in a repository."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Batch Review All Open PRs")
    print("="*70 + "\n")
    
    github_token = os.getenv('GITHUB_TOKEN')
    
    if not github_token:
        print("ERROR: GITHUB_TOKEN not set")
        return
    
    from github import Github
    
    reviewer = GitHubPRReviewer(github_token=github_token)
    github = Github(github_token)
    
    repo_name = "owner/repo"
    repo = github.get_repo(repo_name)
    
    # Get all open PRs
    open_prs = repo.get_pulls(state='open')
    
    print(f"Found {open_prs.totalCount} open PRs\n")
    
    for pr in open_prs:
        print(f"Reviewing PR #{pr.number}: {pr.title}")
        
        try:
            result = reviewer.review_pr(
                repo_name=repo_name,
                pr_number=pr.number,
                post_comments=False  # Set to True to post reviews
            )
            
            print(f"  Decision: {result['overall_decision']}")
            print(f"  Findings: {result['total_findings']}")
            print()
            
        except Exception as e:
            print(f"  Error: {e}\n")


def example_6_webhook_handler():
    """Example 6: GitHub Webhook handler for PR events."""
    print("\n" + "="*70)
    print("EXAMPLE 6: GitHub Webhook Handler")
    print("="*70 + "\n")
    
    print("Example webhook handler code:\n")
    
    webhook_code = '''
from flask import Flask, request, jsonify
from integrations.github_pr import GitHubPRReviewer

app = Flask(__name__)
reviewer = GitHubPRReviewer()

@app.route('/webhook', methods=['POST'])
def github_webhook():
    """Handle GitHub PR webhook events."""
    event = request.headers.get('X-GitHub-Event')
    payload = request.json
    
    # Only handle PR events
    if event not in ['pull_request', 'pull_request_review']:
        return jsonify({'status': 'ignored'}), 200
    
    # Check if PR was opened or synchronized
    action = payload.get('action')
    if action not in ['opened', 'synchronize', 'reopened']:
        return jsonify({'status': 'ignored'}), 200
    
    # Get PR details
    pr_number = payload['pull_request']['number']
    repo_name = payload['repository']['full_name']
    
    print(f"Processing PR #{pr_number} in {repo_name}")
    
    try:
        # Review the PR
        result = reviewer.review_pr(
            repo_name=repo_name,
            pr_number=pr_number,
            post_comments=True,
            review_event="COMMENT"
        )
        
        return jsonify({
            'status': 'success',
            'pr_number': pr_number,
            'decision': result['overall_decision'],
            'findings': result['total_findings']
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
'''
    
    print(webhook_code)
    
    print("\nTo use this webhook:")
    print("1. Deploy the webhook handler to a server")
    print("2. Go to your GitHub repo → Settings → Webhooks")
    print("3. Add webhook with URL: https://yourserver.com/webhook")
    print("4. Select events: Pull requests")
    print("5. Save the webhook")
    print("\nNow PRs will be automatically reviewed when created or updated!")


def example_7_custom_review_rules():
    """Example 7: Custom review rules based on findings."""
    print("\n" + "="*70)
    print("EXAMPLE 7: Custom Review Rules")
    print("="*70 + "\n")
    
    github_token = os.getenv('GITHUB_TOKEN')
    
    if not github_token:
        print("ERROR: GITHUB_TOKEN not set")
        return
    
    reviewer = GitHubPRReviewer(github_token=github_token)
    
    # Review PR
    result = reviewer.review_pr(
        repo_name="owner/repo",
        pr_number=1,
        post_comments=False
    )
    
    # Custom rules
    print("Applying custom review rules...\n")
    
    # Count issues by severity
    high_severity = [f for f in result['findings'] if f['severity'] == 'HIGH']
    medium_severity = [f for f in result['findings'] if f['severity'] == 'MEDIUM']
    low_severity = [f for f in result['findings'] if f['severity'] == 'LOW']
    
    print(f"High Severity Issues: {len(high_severity)}")
    print(f"Medium Severity Issues: {len(medium_severity)}")
    print(f"Low Severity Issues: {len(low_severity)}\n")
    
    # Apply rules
    if len(high_severity) > 0:
        decision = "BLOCK - High severity issues must be fixed"
    elif len(medium_severity) > 3:
        decision = "REQUEST_CHANGES - Too many medium severity issues"
    elif len(low_severity) > 10:
        decision = "COMMENT - Consider addressing low severity issues"
    else:
        decision = "APPROVE - No significant issues found"
    
    print(f"Final Decision: {decision}")


def main():
    """Run all examples."""
    print("\n" + "="*70)
    print("GITHUB PR INTEGRATION EXAMPLES")
    print("="*70)
    print("\nPrerequisites:")
    print("1. Set GITHUB_TOKEN environment variable:")
    print("   export GITHUB_TOKEN='your_github_token'")
    print("\n2. Get token from: https://github.com/settings/tokens")
    print("   Required scopes: repo (or public_repo for public repos)")
    print("\n3. Replace 'owner/repo' and PR numbers with real values")
    
    # Check if token is set
    if not os.getenv('GITHUB_TOKEN'):
        print("\n⚠️  WARNING: GITHUB_TOKEN not set")
        print("Examples will show structure but won't connect to GitHub\n")
    
    # Run examples (most will fail without real repo/PR, but show structure)
    print("\nRunning examples...\n")
    
    # Example 6 doesn't require token
    example_6_webhook_handler()
    
    print("\n" + "="*70)
    print("EXAMPLES COMPLETE")
    print("="*70)
    print("\nTo use these examples:")
    print("1. Set GITHUB_TOKEN environment variable")
    print("2. Replace 'owner/repo' with actual repository")
    print("3. Replace PR numbers with actual PR numbers")
    print("4. Run: python examples/example_github_webhook.py")
    print("\nFor webhook integration:")
    print("  python examples/example_github_webhook.py example_6\n")


if __name__ == '__main__':
    main()
