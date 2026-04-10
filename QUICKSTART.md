# 🚀 AgentMesh - Quick Start Guide

## How to Run This Project

### Prerequisites

- **Python 3.10+** (uses dataclasses and type hints)
- **No external dependencies required!** (Standard library only)
- **Optional:** Groq API key for LLM reasoning agent

---

## Option 1: Quick Start (Recommended)

### 1. Install Dependencies

```bash
# Navigate to project directory
cd d:\AgentMesh\AgentMesh

# Install required packages
pip install -r requirements.txt
```

**Current dependencies:**
- `groq` - For LLM reasoning agent (Step 9)
- `python-dotenv` - For environment variable management
- `pytest` - For running tests (optional)

### 2. Configure Environment (Optional - for LLM agent)

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your Groq API key
# Get free key from: https://console.groq.com/
```

Your `.env` should contain:
```
GROQ_API_KEY=your_actual_key_here
```

### 3. Run the Main Demo

```bash
# Set Python path and run
$env:PYTHONPATH="d:\AgentMesh\AgentMesh"
python main.py
```

**Menu Options:**
1. **Run Single Demo Scenario** - Test specific code samples
2. **Run All Demo Scenarios** - Batch test all scenarios  
3. **Process Custom Code** - Review your own code
4. **View Task History** - See past reviews
5. **View System Statistics** - Performance metrics
6. **Exit**

---

## Option 2: Run Specific Demos

### Demo 1: Complete Framework Demo

Shows all framework features including plugin architecture, multi-agent collaboration, and conflict resolution:

```bash
$env:PYTHONPATH="d:\AgentMesh\AgentMesh"
python demo_complete.py
```

**What it demonstrates:**
- Multi-agent code review (security, quality, performance)
- Plugin-based architecture
- Weighted agent selection
- Conflict resolution
- Performance benchmarking

### Demo 2: Goal Loop Demo (Step 7)

Shows autonomous iterative refinement with goal-driven execution:

```bash
$env:PYTHONPATH="d:\AgentMesh\AgentMesh"
python demo_step6_complete.py
```

**What it demonstrates:**
- Goal-driven autonomous reasoning
- Iterative refinement loops
- Success criteria evaluation
- Quality improvement tracking

### Demo 3: Memory System Demo (Step 8)

Shows stateful learning and shared memory:

```bash
$env:PYTHONPATH="d:\AgentMesh\AgentMesh"
python demo_memory_system.py
```

**What it demonstrates:**
- Shared memory across iterations
- Pattern storage and retrieval
- Stateful learning
- Context preservation

### Demo 4: Agentic Loop Example

```bash
$env:PYTHONPATH="d:\AgentMesh\AgentMesh"
python examples/demo_agentic_loop.py
```

---

## Option 3: Run Tests

### Test All Components

```bash
# Run all tests
$env:PYTHONPATH="d:\AgentMesh\AgentMesh"
pytest tests/ -v
```

### Test Specific Components

```bash
# Test LLM reasoning agent (Step 9)
pytest tests/test_llm_reasoning_agent.py -v

# Test goal loop
pytest tests/test_goal_lifecycle.py -v

# Test shared memory
pytest tests/test_shared_memory.py -v

# Test agent registry
pytest tests/test_agent_registry.py -v

# Test integration
pytest tests/test_integration.py -v
```

### Verify LLM API Key

```bash
python tests/verify_groq_api.py
```

**Expected output:**
```
✓ API key found: gsk_...
✓ Groq client initialized
✓ Testing API with a simple request...
✓ API Response: OK
✓✓✓ SUCCESS! Your Groq API key is VALID and working! ✓✓✓
```

### Test Step 9 Completion

```bash
python tests/test_step9_completion.py
```

**Expected output:**
```
============================================================
STEP 9 COMPLETION VERIFICATION
============================================================

✓ Deterministic agent registered: SecurityAgent
✓ LLM agent registered: LLMReasoningAgent
✓ Coordinator created (supports hybrid orchestration)

🎉 STEP 9 COMPLETE - All requirements met!
```

---

## Option 4: Interactive Python Shell

### Quick Test

```python
# Start Python in project directory
cd d:\AgentMesh\AgentMesh
python

# In Python shell:
from framework_init import initialize_framework
from core.models import Task

# Initialize
coordinator, registry, history, logger = initialize_framework()

# Create a task
task = Task(
    task_id="test-001",
    task_type="code_review",
    description="Review authentication code for security issues"
)

# Process
report = coordinator.process_task(task)

# View results
print(f"Decision: {report.decision}")
print(f"Confidence: {report.confidence:.2f}")
print(f"Findings: {len(report.critical_findings)} critical")
```

### Goal-Driven Example

```python
from core.models import Goal, SuccessCriteria

# Define quality requirements
goal = Goal(
    goal_id="goal-001",
    description="Comprehensive security review",
    success_criteria=SuccessCriteria(
        min_confidence=0.90,
        max_conflicts=0,
        require_consensus=True
    ),
    max_iterations=5
)

# Execute (autonomous iteration)
report = coordinator.process_goal(goal)

# Track refinement
print(f"Iterations: {report.iterations_completed}")
print(f"Goal achieved: {report.goal_achieved}")
for eval in report.evaluation_history:
    print(f"  Iter {eval.iteration}: {eval.confidence_score:.2%}")
```

### Hybrid Reasoning Example

```python
from plugins.security_agent import SecurityAgent
from plugins.llm_reasoning_agent import LLMReasoningAgent

# Register both deterministic and LLM agents
bus = coordinator.message_bus
registry.register(
    SecurityAgent(bus),
    capabilities=['security', 'vulnerability'],
    priority=9
)

registry.register(
    LLMReasoningAgent("llm-agent", bus),
    capabilities=['reasoning', 'edge-cases'],
    priority=6
)

# Process task - both agents contribute
task = Task(
    task_id="hybrid-001",
    task_type="code_review",
    description="Analyze payment processing for vulnerabilities and edge cases"
)
report = coordinator.process_task(task)

# View hybrid results
for response in report.agent_responses:
    print(f"{response.agent_type}: {response.status}")
```

---

## Option 5: REST API (If Implemented)

```bash
# Start API server
python api/rest_api.py

# In another terminal, test endpoints:
curl http://localhost:5000/health
curl -X POST http://localhost:5000/analyze -d '{"code": "..."}'
```

---

## Option 6: CLI Interface (If Implemented)

```bash
# Run CLI
python cli/cli.py review --file mycode.py

# Help
python cli/cli.py --help
```

---

## Common Issues & Solutions

### Issue 1: "Module not found" error

**Solution:**
```bash
# Always set PYTHONPATH before running
$env:PYTHONPATH="d:\AgentMesh\AgentMesh"

# Or add to your PowerShell profile permanently:
[System.Environment]::SetEnvironmentVariable('PYTHONPATH', 'd:\AgentMesh\AgentMesh', 'User')
```

### Issue 2: Groq API key not working

**Solution:**
```bash
# Verify .env file exists
ls .env

# Check API key is set (without quotes)
cat .env
# Should show: GROQ_API_KEY=gsk_your_key_here

# Test API key
python tests/verify_groq_api.py
```

### Issue 3: Tests failing

**Solution:**
```bash
# Install test dependencies
pip install pytest

# Run with verbose output
pytest tests/ -v -s

# Run specific failing test
pytest tests/test_specific.py::test_function_name -v
```

### Issue 4: Import errors in demos

**Solution:**
```bash
# Ensure you're in the project root
cd d:\AgentMesh\AgentMesh

# Set PYTHONPATH
$env:PYTHONPATH="d:\AgentMesh\AgentMesh"

# Run demo
python demo_complete.py
```

---

## Project Structure

```
AgentMesh/
├── main.py                    # Main entry point (interactive menu)
├── demo_complete.py           # Complete framework demo
├── demo_step6_complete.py     # Goal loop demo
├── demo_memory_system.py      # Memory system demo
├── framework_init.py          # Framework initialization
├── config.py                  # Configuration
├── .env                       # Environment variables (API keys)
│
├── agents/                    # Core agents
│   ├── base_agent.py          # Abstract base class
│   └── coordinator_new.py     # Orchestrator
│
├── plugins/                   # Specialist agents (plugins)
│   ├── security_agent.py      # Security specialist
│   ├── code_quality_agent.py  # Quality specialist
│   ├── performance_agent.py   # Performance specialist
│   ├── documentation_agent.py # Documentation specialist
│   └── llm_reasoning_agent.py # LLM reasoning (Step 9)
│
├── core/                      # Core framework
│   ├── models.py              # Data structures
│   ├── agent_registry.py      # Plugin management
│   ├── conflict_resolver.py   # Conflict resolution
│   ├── aggregator.py          # Report aggregation
│   ├── goal_evaluator.py      # Goal evaluation
│   └── message_bus.py         # Communication
│
├── memory/                    # Shared memory
│   └── shared_memory.py       # Stateful learning
│
├── tests/                     # Test suite
│   ├── test_*.py              # Various tests
│   ├── verify_groq_api.py     # API verification
│   └── test_step9_completion.py # Step 9 verification
│
├── demo/                      # Demo scenarios
│   └── demo_scenarios.py      # Sample code for testing
│
└── docs/                      # Documentation
    ├── ARCHITECTURE.md        # Architecture details
    ├── STEP7_GOAL_LOOP.md     # Goal loop docs
    ├── STEP8_SHARED_MEMORY.md # Memory docs
    └── STEP10_DOCUMENTATION.md # Step 10 summary
```

---

## Quick Command Reference

```bash
# Setup
cd d:\AgentMesh\AgentMesh
pip install -r requirements.txt
cp .env.example .env  # Then edit with your API key

# Run demos
$env:PYTHONPATH="d:\AgentMesh\AgentMesh"
python main.py                    # Interactive menu
python demo_complete.py           # Full framework demo
python demo_step6_complete.py     # Goal loop demo
python demo_memory_system.py      # Memory demo

# Run tests
pytest tests/ -v                           # All tests
pytest tests/test_llm_reasoning_agent.py  # LLM agent tests
python tests/verify_groq_api.py           # API verification
python tests/test_step9_completion.py     # Step 9 check

# Documentation
cat README.md                     # Main README
cat docs/ARCHITECTURE.md          # Full architecture
cat docs/STEP7_GOAL_LOOP.md       # Goal loop details
cat docs/STEP8_SHARED_MEMORY.md   # Memory details
```

---

## Next Steps

### For Learning:
1. Read [README.md](../README.md) - Project overview
2. Read [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - Complete architecture
3. Run `main.py` - Interactive demo
4. Run tests - Verify everything works

### For Development:
1. Create custom agent in `plugins/`
2. Register in `framework_init.py`
3. Run tests to verify
4. Submit PR!

### For Interviews:
1. Read architecture documentation
2. Understand technical contributions
3. Practice explaining design decisions
4. Review talking points in docs

---

## Support

**Documentation:**
- [README.md](../README.md) - Main documentation
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Complete architecture
- [STEP7_GOAL_LOOP.md](docs/STEP7_GOAL_LOOP.md) - Goal loop
- [STEP8_SHARED_MEMORY.md](docs/STEP8_SHARED_MEMORY.md) - Memory
- [STEP10_DOCUMENTATION.md](docs/STEP10_DOCUMENTATION.md) - Summary

**Issues?**
- Check environment setup (PYTHONPATH, .env)
- Verify Python version (3.10+)
- Test API key if using LLM agent
- Review error messages carefully

---

**Happy coding! 🚀**
