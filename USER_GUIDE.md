# 🎯 AgentMesh User Guide - How to Use Each Feature

## How to Run the Project

```bash
$env:PYTHONPATH="d:\AgentMesh\AgentMesh"
python main.py
```

---

## 📋 Menu Options Explained

### **Option 1: Run Single Demo Scenario**

**What it does:** Tests the framework with pre-built code examples

**How to use:**
1. Select option `1`
2. Choose a demo scenario (1-5)
3. System analyzes the code
4. Shows findings and decision

**Example:**
```
Select option: 1
Select scenario: 1  (Authentication Service)

Output:
- CRITICAL: SQL Injection detected
- HIGH: Weak MD5 hashing
- HIGH: Hardcoded secrets
Decision: BLOCK
```

---

### **Option 2: Run All Demo Scenarios**

**What it does:** Batch tests all 5 demo scenarios at once

**How to use:**
1. Select option `2`
2. System runs all demos automatically
3. Shows summary with accuracy stats

**Output example:**
```
✓ Authentication Service: BLOCK
✓ Data Processor: APPROVE_WITH_CHANGES  
✓ API Handler: APPROVE_WITH_CHANGES
✓ Crypto Issues: BLOCK
✓ Good Code: APPROVE

Accuracy: 100%
Total Findings: 47
```

---

### **Option 3: Process Custom Code** ⭐ (Most Useful!)

**What it does:** Analyzes YOUR own Python code

**How to use:**

#### Step 1: Select option `3`

#### Step 2: Paste your code, then type `END`

**Example Session:**
```
Select option: 3

Enter your Python code to review.
Type 'END' on a new line when finished.
----------------------------------------------------------------------

def login(username, password):
    query = f"SELECT * FROM users WHERE name='{username}'"
    db.execute(query)
    return True
END

Task description (optional): Login function security review

Processing...

============================================================
           AGENTMESH CODE REVIEW REPORT
============================================================

Task ID: custom-1738678901
Timestamp: 2026-02-04 15:15:01

DECISION: BLOCK

CRITICAL FINDINGS (1):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • [SECURITY] SQL Injection vulnerability detected
    Confidence: 95%
    Line 2: query = f"SELECT * FROM users WHERE name='{username}'"
    Recommendation: Use parameterized queries

IMPORTANT FINDINGS (2):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • [CODE_QUALITY] Missing error handling
    Confidence: 80%
    
  • [SECURITY] No password hashing detected
    Confidence: 70%

Processing time: 0.03s
✓ Task saved to history
```

---

### **Option 4: View Task History**

**What it does:** Shows last 10 analyzed tasks

**How to use:**
1. Select option `4`
2. View previous analysis results

**Output:**
```
Recent Task History
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Task ID: custom-1738678901
Timestamp: 2026-02-04 15:15:01
Decision: BLOCK
Findings: 3
Conflicts: No
----------------------------------------------------------------------

Task ID: demo-auth-service
Timestamp: 2026-02-04 14:30:12
Decision: BLOCK
Findings: 5
Conflicts: Yes
```

---

### **Option 5: View System Statistics**

**What it does:** Shows overall performance metrics

**How to use:**
1. Select option `5`
2. View analytics

**Output:**
```
System Statistics
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total Tasks Processed: 25
Average Findings per Task: 6.4
Conflict Rate: 32%
Average Confidence: 87%

Decision Distribution:
  APPROVE: 40%
  APPROVE_WITH_CHANGES: 35%
  BLOCK: 25%

Agent Performance:
  Security Agent: 25 tasks, 95% avg confidence
  Code Quality Agent: 25 tasks, 82% avg confidence
  Performance Agent: 20 tasks, 78% avg confidence
  Documentation Agent: 15 tasks, 85% avg confidence
```

---

## 📝 Real-World Usage Examples

### Example 1: Review Your Own Code

**Scenario:** You wrote a login function and want to check for security issues

```python
# Start the program
python main.py

# Select option 3
Select option: 3

# Paste your code
def authenticate(user, pwd):
    conn = get_db()
    result = conn.execute(f"SELECT * FROM users WHERE username='{user}'")
    return result
END

# Enter description
Task description: Check login security

# Get instant feedback!
# Output: BLOCK - SQL Injection detected!
```

---

### Example 2: Compare Different Approaches

**Session 1 - Bad approach:**
```python
Select option: 3

# Paste bad code
password_hash = hashlib.md5(password.encode()).hexdigest()
END

Result: BLOCK - Weak hashing (MD5)
```

**Session 2 - Good approach:**
```python
Select option: 3

# Paste improved code
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
END

Result: APPROVE - Secure hashing detected
```

---

### Example 3: Batch Test Your Project Files

**Option A:** Use Option 3 multiple times
- Copy/paste each file
- Type `END` after each
- Review results

**Option B:** Create a custom demo (advanced)
- Add your code to `demo/demo_scenarios.py`
- Run Option 2 to batch test

---

## 🔧 Customization Tips

### Add Your Own Test Scenarios

Edit `demo/demo_scenarios.py`:

```python
DEMO_SCENARIOS = {
    # ... existing scenarios ...
    
    'my_custom_test': {
        'name': 'My API Endpoint',
        'code': '''
def my_api_handler(request):
    user_id = request.GET['id']
    query = f"SELECT * FROM data WHERE id={user_id}"
    return execute(query)
        ''',
        'expected_decision': 'BLOCK',
        'description': 'Testing my API for SQL injection'
    }
}
```

Then use Option 1 to test it!

---

## 💡 Pro Tips

### Tip 1: Use Descriptive Task Names
```
Task description: Payment processing security audit
```
Better than:
```
Task description: code review
```

### Tip 2: Test Small Chunks
Instead of pasting 500 lines, paste one function at a time for clearer feedback.

### Tip 3: Review History Regularly
Use Option 4 to track improvements over time.

### Tip 4: Combine Options
1. Run Option 3 for your code
2. Run Option 1 to see how it compares to demos
3. Check Option 5 for overall patterns

---

## 🎯 Common Use Cases

### Use Case 1: Homework/Assignment Review
```bash
# Before submitting
1. Run main.py
2. Select option 3
3. Paste your assignment code
4. Fix any CRITICAL or HIGH findings
5. Resubmit until you get APPROVE
```

### Use Case 2: Interview Preparation
```bash
# Practice coding problems
1. Solve a problem
2. Paste into AgentMesh (option 3)
3. Check for code quality issues
4. Refactor based on feedback
5. Test again
```

### Use Case 3: Production Code Audit
```bash
# Weekly code review
1. Run option 2 to baseline
2. Add your new code as custom scenario
3. Run option 1 to compare quality
4. Track metrics with option 5
```

---

## 🚀 Quick Command Reference

```bash
# Start application
$env:PYTHONPATH="d:\AgentMesh\AgentMesh"; python main.py

# Menu shortcuts:
1 - Test with demo scenarios
2 - Batch test all demos  
3 - Analyze YOUR code ⭐
4 - View past results
5 - See statistics
6 - Exit
```

---

## ⚠️ Common Mistakes

### ❌ Mistake 1: Forgetting to type `END`
```
def my_code():
    return True
# ← Still waiting for END!
```
**Fix:** Always type `END` on a new line

### ❌ Mistake 2: Not setting PYTHONPATH
```
python main.py  # Error: Module not found
```
**Fix:** 
```bash
$env:PYTHONPATH="d:\AgentMesh\AgentMesh"; python main.py
```

### ❌ Mistake 3: Pasting formatted code with tabs
**Fix:** Paste plain text code, the system handles formatting

---

## 📊 Understanding Results

### Decision Types

| Decision | Meaning | Action |
|----------|---------|--------|
| **APPROVE** | ✅ No issues found | Safe to use |
| **APPROVE_WITH_CHANGES** | ⚠️ Minor issues | Fix recommendations before production |
| **BLOCK** | 🚫 Critical issues | Must fix before deployment |

### Severity Levels

| Level | Color | Urgency |
|-------|-------|---------|
| **CRITICAL** | 🔴 Red | Fix immediately |
| **HIGH** | 🟠 Orange | Fix before production |
| **MEDIUM** | 🟡 Yellow | Should fix |
| **LOW** | 🟢 Green | Nice to fix |

### Confidence Scores

- **90-100%:** Very certain
- **70-89%:** Highly confident
- **50-69%:** Moderate confidence
- **Below 50%:** Low confidence (review manually)

---

## 🎓 Learning Path

### Beginner (Day 1)
1. Run Option 1 (demo scenarios)
2. Understand what gets flagged
3. Try Option 3 with simple code

### Intermediate (Week 1)
1. Use Option 3 for all your code
2. Track improvements with Option 4
3. Understand patterns with Option 5

### Advanced (Month 1)
1. Add custom scenarios
2. Contribute new agent plugins
3. Customize detection rules

---

**Ready to analyze code? Run `python main.py` and select option 3!** 🚀
