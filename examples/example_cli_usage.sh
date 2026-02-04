#!/bin/bash

# AgentMesh CLI Usage Examples
# Run with: bash examples/example_cli_usage.sh

echo "========================================================================"
echo "AGENTMESH CLI EXAMPLES"
echo "========================================================================"
echo ""

# Example 1: Get help
echo "Example 1: CLI Help"
echo "------------------------------------------------------------------------"
python cli/agentmesh_cli.py --help
echo ""

# Example 2: List available agents
echo ""
echo "Example 2: List Available Agents"
echo "------------------------------------------------------------------------"
python cli/agentmesh_cli.py agents
echo ""

# Example 3: List agents in JSON format
echo ""
echo "Example 3: List Agents (JSON format)"
echo "------------------------------------------------------------------------"
python cli/agentmesh_cli.py agents --format json
echo ""

# Example 4: Create a test file and review it
echo ""
echo "Example 4: Review a Code File"
echo "------------------------------------------------------------------------"

# Create test file
cat > /tmp/test_review.py << 'EOF'
def process_payment(card_number, cvv, amount):
    # Store card details
    db.save("cards", {
        "number": card_number,
        "cvv": cvv,
        "amount": amount
    })
    
    # Process payment
    query = "SELECT * FROM accounts WHERE card='" + card_number + "'"
    result = db.execute(query)
    return result
EOF

echo "Created test file: /tmp/test_review.py"
echo ""

# Review the file
python cli/agentmesh_cli.py review /tmp/test_review.py
echo ""

# Example 5: Review with high priority
echo ""
echo "Example 5: Review with HIGH Priority"
echo "------------------------------------------------------------------------"
python cli/agentmesh_cli.py review /tmp/test_review.py --priority HIGH
echo ""

# Example 6: Review and save report
echo ""
echo "Example 6: Review and Save Report"
echo "------------------------------------------------------------------------"
python cli/agentmesh_cli.py review /tmp/test_review.py --save
echo ""
echo "Report saved to: /tmp/test_review.py.agentmesh-report.json"
if [ -f /tmp/test_review.py.agentmesh-report.json ]; then
    echo "Report contents:"
    cat /tmp/test_review.py.agentmesh-report.json | python -m json.tool
fi
echo ""

# Example 7: Review in JSON format
echo ""
echo "Example 7: Review Output in JSON"
echo "------------------------------------------------------------------------"
python cli/agentmesh_cli.py review /tmp/test_review.py --format json
echo ""

# Example 8: Select agents for a task
echo ""
echo "Example 8: Select Agents for Task"
echo "------------------------------------------------------------------------"
python cli/agentmesh_cli.py select "Check for SQL injection and security issues"
echo ""

# Example 9: Weighted agent selection
echo ""
echo "Example 9: Weighted Agent Selection"
echo "------------------------------------------------------------------------"
python cli/agentmesh_cli.py select "CRITICAL: Authentication bypass vulnerability" --weighted
echo ""

# Example 10: Reload plugins
echo ""
echo "Example 10: Hot-Reload Plugins"
echo "------------------------------------------------------------------------"
python cli/agentmesh_cli.py reload
echo ""

# Example 11: Run benchmark
echo ""
echo "Example 11: Performance Benchmark (50 tasks)"
echo "------------------------------------------------------------------------"
python cli/agentmesh_cli.py benchmark --tasks 50
echo ""

# Example 12: Pipeline - Review multiple files
echo ""
echo "Example 12: Review Multiple Files"
echo "------------------------------------------------------------------------"

# Create multiple test files
cat > /tmp/auth.py << 'EOF'
def login(username, password):
    return username == "admin" and password == "admin123"
EOF

cat > /tmp/api.py << 'EOF'
def get_user(user_id):
    return db.query(f"SELECT * FROM users WHERE id={user_id}")
EOF

cat > /tmp/utils.py << 'EOF'
def hash_password(password):
    return password  # No hashing!
EOF

echo "Reviewing multiple files..."
for file in /tmp/auth.py /tmp/api.py /tmp/utils.py; do
    echo ""
    echo "Reviewing: $file"
    python cli/agentmesh_cli.py review $file --format json | python -c "
import sys, json
data = json.load(sys.stdin)
print(f\"  Decision: {data['decision']}\")
print(f\"  Confidence: {data['confidence']:.1f}%\")
print(f\"  Findings: {data['agents_consulted']} agents, {sum(len(f['issues']) for f in data['findings'])} issues\")
"
done
echo ""

# Example 13: Batch review with summary
echo ""
echo "Example 13: Batch Review Summary"
echo "------------------------------------------------------------------------"

total_files=0
approve_count=0
block_count=0

for file in /tmp/test_review.py /tmp/auth.py /tmp/api.py /tmp/utils.py; do
    result=$(python cli/agentmesh_cli.py review $file --format json 2>/dev/null)
    decision=$(echo $result | python -c "import sys, json; print(json.load(sys.stdin)['decision'])" 2>/dev/null)
    
    total_files=$((total_files + 1))
    
    if [ "$decision" = "APPROVE" ]; then
        approve_count=$((approve_count + 1))
    elif [ "$decision" = "BLOCK" ]; then
        block_count=$((block_count + 1))
    fi
done

echo "Batch Review Summary:"
echo "  Total Files: $total_files"
echo "  Approved: $approve_count"
echo "  Blocked: $block_count"
echo ""

# Cleanup
echo "Cleaning up test files..."
rm -f /tmp/test_review.py /tmp/auth.py /tmp/api.py /tmp/utils.py
rm -f /tmp/test_review.py.agentmesh-report.json
echo ""

echo "========================================================================"
echo "ALL CLI EXAMPLES COMPLETED"
echo "========================================================================"
echo ""
echo "Available commands:"
echo "  python cli/agentmesh_cli.py review <file>    # Review a code file"
echo "  python cli/agentmesh_cli.py agents           # List available agents"
echo "  python cli/agentmesh_cli.py reload           # Hot-reload plugins"
echo "  python cli/agentmesh_cli.py benchmark        # Run performance test"
echo "  python cli/agentmesh_cli.py select <desc>    # Select agents for task"
echo ""
