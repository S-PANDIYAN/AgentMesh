"""
Example: Using AgentMesh REST API Client
Demonstrates how to submit tasks and check status via HTTP API.
"""
import requests
import time
import json


class AgentMeshClient:
    """Simple client for AgentMesh REST API."""
    
    def __init__(self, base_url='http://localhost:5000'):
        """Initialize client with API base URL."""
        self.base_url = base_url
    
    def health_check(self):
        """Check API health."""
        response = requests.get(f'{self.base_url}/health')
        return response.json()
    
    def list_agents(self):
        """List all available agents."""
        response = requests.get(f'{self.base_url}/agents')
        return response.json()
    
    def submit_review(self, code, description, priority='MEDIUM'):
        """Submit a code review task."""
        data = {
            'description': description,
            'priority': priority,
            'task_type': 'code_review',
            'payload': {
                'code': code
            }
        }
        
        response = requests.post(f'{self.base_url}/review', json=data)
        return response.json()
    
    def get_status(self, task_id):
        """Get task status."""
        response = requests.get(f'{self.base_url}/status/{task_id}')
        return response.json()
    
    def wait_for_completion(self, task_id, timeout=30, poll_interval=0.5):
        """Wait for task to complete."""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self.get_status(task_id)
            
            if status['status'] in ['completed', 'failed']:
                return status
            
            time.sleep(poll_interval)
        
        raise TimeoutError(f"Task {task_id} did not complete within {timeout}s")
    
    def select_agents(self, description, use_weighted=False):
        """Select agents for a task."""
        data = {
            'description': description,
            'use_weighted': use_weighted
        }
        
        response = requests.post(f'{self.base_url}/select', json=data)
        return response.json()
    
    def reload_plugins(self):
        """Hot-reload all plugins."""
        response = requests.post(f'{self.base_url}/reload')
        return response.json()


def example_1_basic_review():
    """Example 1: Basic code review."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Code Review")
    print("="*70 + "\n")
    
    client = AgentMeshClient()
    
    # Check API health
    health = client.health_check()
    print(f"API Status: {health['status']}")
    print(f"Agents Loaded: {health['agents_loaded']}\n")
    
    # Code to review
    code = """
def login(username, password):
    query = "SELECT * FROM users WHERE username='" + username + "'"
    result = db.execute(query)
    return result
"""
    
    # Submit review
    print("Submitting code for review...")
    result = client.submit_review(
        code=code,
        description="Review login function for security issues",
        priority="HIGH"
    )
    
    task_id = result['task_id']
    print(f"Task ID: {task_id}")
    print(f"Status: {result['status']}\n")
    
    # Wait for completion
    print("Waiting for review to complete...")
    final_result = client.wait_for_completion(task_id)
    
    # Print results
    print("\n" + "-"*70)
    print("REVIEW RESULTS")
    print("-"*70)
    
    if final_result['status'] == 'completed':
        result_data = final_result['result']
        print(f"Decision: {result_data['decision']}")
        print(f"Confidence: {result_data['confidence']:.1f}%")
        print(f"Agents Consulted: {result_data['agents_consulted']}")
        print(f"Processing Time: {result_data['processing_time_ms']}ms\n")
        
        print("Findings by Agent:")
        for finding in result_data['findings']:
            print(f"\n  {finding['agent']}:")
            print(f"    Decision: {finding['decision']}")
            print(f"    Confidence: {finding['confidence']:.1f}%")
            if finding['findings']:
                print(f"    Issues:")
                for issue in finding['findings']:
                    print(f"      - {issue}")
    else:
        print(f"Task failed: {final_result.get('error', 'Unknown error')}")


def example_2_list_agents():
    """Example 2: List available agents."""
    print("\n" + "="*70)
    print("EXAMPLE 2: List Available Agents")
    print("="*70 + "\n")
    
    client = AgentMeshClient()
    
    result = client.list_agents()
    
    print(f"Total Agents: {result['total']}\n")
    
    for agent in result['agents']:
        print(f"ID: {agent['id']}")
        print(f"  Type: {agent['type']}")
        print(f"  Priority: {agent['priority']}")
        print(f"  Capabilities: {', '.join(agent['capabilities'][:5])}")
        if len(agent['capabilities']) > 5:
            print(f"    ...and {len(agent['capabilities'])-5} more")
        print()


def example_3_agent_selection():
    """Example 3: Agent selection for different tasks."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Intelligent Agent Selection")
    print("="*70 + "\n")
    
    client = AgentMeshClient()
    
    # Test different task descriptions
    tasks = [
        "Check for SQL injection vulnerabilities",
        "Review code quality and style",
        "Analyze performance bottlenecks",
        "Generate API documentation"
    ]
    
    for task_desc in tasks:
        print(f"Task: {task_desc}")
        
        # Standard selection
        result = client.select_agents(task_desc, use_weighted=False)
        print(f"  Standard: {len(result['agents_selected'])} agents")
        for agent in result['agents_selected']:
            print(f"    - {agent['id']}")
        
        # Weighted selection
        result = client.select_agents(task_desc, use_weighted=True)
        print(f"  Weighted: {len(result['agents_selected'])} agents")
        for agent in result['agents_selected']:
            print(f"    - {agent['id']}")
        
        print()


def example_4_batch_reviews():
    """Example 4: Batch review multiple files."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Batch Review")
    print("="*70 + "\n")
    
    client = AgentMeshClient()
    
    # Multiple code samples
    code_samples = [
        {
            'name': 'auth.py',
            'code': 'def authenticate(user, pwd): return user == "admin" and pwd == "12345"'
        },
        {
            'name': 'api.py',
            'code': 'def get_user(id): return db.query(f"SELECT * FROM users WHERE id={id}")'
        },
        {
            'name': 'utils.py',
            'code': 'def process_data(data): return [x*2 for x in data]'
        }
    ]
    
    # Submit all reviews
    task_ids = []
    for sample in code_samples:
        print(f"Submitting {sample['name']}...")
        result = client.submit_review(
            code=sample['code'],
            description=f"Review {sample['name']}"
        )
        task_ids.append((sample['name'], result['task_id']))
    
    print(f"\nSubmitted {len(task_ids)} tasks\n")
    
    # Wait for all to complete
    print("Waiting for all reviews to complete...\n")
    
    for filename, task_id in task_ids:
        result = client.wait_for_completion(task_id)
        
        if result['status'] == 'completed':
            data = result['result']
            print(f"{filename}: {data['decision']} ({data['confidence']:.0f}% confidence)")
        else:
            print(f"{filename}: FAILED")


def example_5_hot_reload():
    """Example 5: Hot-reload plugins."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Hot-Reload Plugins")
    print("="*70 + "\n")
    
    client = AgentMeshClient()
    
    # Check current agents
    before = client.list_agents()
    print(f"Agents before reload: {before['total']}")
    
    # Reload plugins
    print("\nReloading plugins...")
    result = client.reload_plugins()
    
    print(f"\nReload results:")
    for plugin, status in result['results'].items():
        status_text = "✓ Success" if status else "✗ Failed"
        print(f"  {plugin}: {status_text}")
    
    # Check agents after reload
    after = client.list_agents()
    print(f"\nAgents after reload: {after['total']}")
    print(f"Message: {result['message']}")


def example_6_error_handling():
    """Example 6: Error handling."""
    print("\n" + "="*70)
    print("EXAMPLE 6: Error Handling")
    print("="*70 + "\n")
    
    client = AgentMeshClient()
    
    # Test 1: Invalid task ID
    print("Test 1: Getting status of non-existent task")
    try:
        result = client.get_status('invalid-task-id')
        if 'error' in result:
            print(f"  Expected error: {result['error']}")
    except requests.exceptions.RequestException as e:
        print(f"  Request failed: {e}")
    
    # Test 2: Empty review submission
    print("\nTest 2: Submitting invalid review")
    try:
        response = requests.post(f'{client.base_url}/review', json={})
        result = response.json()
        if 'error' in result:
            print(f"  Expected error: {result['error']}")
    except Exception as e:
        print(f"  Error caught: {e}")
    
    # Test 3: API not running
    print("\nTest 3: Connecting to invalid endpoint")
    try:
        client_bad = AgentMeshClient('http://localhost:9999')
        result = client_bad.health_check()
    except requests.exceptions.ConnectionError:
        print("  Expected error: Connection refused (API not running)")


def main():
    """Run all examples."""
    print("\n" + "="*70)
    print("AGENTMESH REST API CLIENT EXAMPLES")
    print("="*70)
    print("\nMake sure the API server is running:")
    print("  python api/rest_api.py")
    print("\nOr use: python api/rest_api.py --port 5000")
    
    try:
        # Run examples
        example_1_basic_review()
        example_2_list_agents()
        example_3_agent_selection()
        example_4_batch_reviews()
        example_5_hot_reload()
        example_6_error_handling()
        
        print("\n" + "="*70)
        print("ALL EXAMPLES COMPLETED")
        print("="*70 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Could not connect to API server")
        print("Please start the server first:")
        print("  python api/rest_api.py\n")
    except Exception as e:
        print(f"\n✗ ERROR: {e}\n")


if __name__ == '__main__':
    main()
