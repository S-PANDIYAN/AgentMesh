# AgentMesh 🤖

**Production-Ready Multi-Agent Orchestration Framework**

A sophisticated autonomous multi-agent system featuring **goal-driven iterative refinement**, **plugin-based architecture**, **weighted conflict resolution**, and **hybrid reasoning** (deterministic + LLM). AgentMesh enables intelligent task delegation, autonomous quality improvement, and stateful learning across iterations.

---

## 🎯 Problem Statement

**AgentMesh addresses the lack of structured multi-agent orchestration frameworks capable of:**

1. **Dynamic Delegation**: Automatically routing tasks to appropriate specialist agents based on capability matching
2. **Conflict Resolution**: Systematically handling contradictions between multiple agent opinions with weighted arbitration
3. **Iterative Goal Refinement**: Autonomously improving analysis quality through goal-driven execution loops
4. **Hybrid Reasoning**: Combining deterministic rule-based agents with probabilistic LLM-powered reasoning
5. **Stateful Learning**: Maintaining context and patterns across iterations through shared memory
6. **Plugin Extensibility**: Adding new specialist agents without modifying core framework

📖 **[Read Full Architecture Documentation →](docs/ARCHITECTURE.md)**

---

## ✨ Key Technical Contributions

### 1. **Plugin-Based Architecture**
- True plugin system where agents are dynamically loaded
- Drop new agents into `plugins/` directory
- Framework automatically discovers capabilities
- Zero modification to core framework needed

### 2. **Capability-Based Routing**
- Automatic agent selection using semantic capability matching
- Task keywords → Agent capabilities scoring
- Intelligent delegation without manual configuration
- Works with any number/type of agents

### 3. **Weighted Conflict Arbitration**
- Systematic conflict resolution using multi-factor weighting
- `score = confidence × priority × domain_weight`
- Domain-specific rules (e.g., security overrides style)
- Full audit trail of all resolutions

### 4. **Goal-Driven Execution Loop**
- Autonomous iterative refinement until quality criteria met
- `Goal → Plan → Act → Evaluate → Refine → Repeat`
- Self-improving system without human intervention
- Full transparency with evaluation history

### 5. **Shared Memory Model**
- Persistent learning across iterations and tasks
- Store/retrieve patterns, conflicts, performance data
- Context-aware retrieval with filtering
- Enables continuous improvement

### 6. **Hybrid Reasoning Support**
- Seamless integration of deterministic + probabilistic agents
- Deterministic: Pattern matching, rule-based (high confidence)
- LLM-based: Probabilistic reasoning, edge cases (conservative confidence)
- Coordinator treats both types identically

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/AgentMesh.git
cd AgentMesh

# Install dependencies
pip install -r requirements.txt

# Set up environment (optional - for LLM agent)
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### Basic Usage

#### Example 1: Single-Pass Task Analysis

```python
from core.message_bus import MessageBus
from core.agent_registry import AgentRegistry
from agents.coordinator_new import Coordinator
from plugins.security_agent import SecurityAgent
from core.models import Task

# Setup
bus = MessageBus()
registry = AgentRegistry()
registry.register(SecurityAgent(bus), capabilities=['security'])
coordinator = Coordinator(bus, registry)

# Execute
task = Task(
    task_id="review-001",
    task_type="code_review",
    description="Review authentication endpoint for vulnerabilities"
)
report = coordinator.process_task(task)

# Results
print(f"Decision: {report.decision}")
print(f"Confidence: {report.confidence:.2f}")
print(f"Critical findings: {len(report.critical_findings)}")
```

#### Example 2: Goal-Driven Iterative Analysis

```python
from core.models import Goal, SuccessCriteria

# Define quality requirements
goal = Goal(
    goal_id="goal-001",
    description="Comprehensive security review of payment system",
    success_criteria=SuccessCriteria(
        min_confidence=0.90,
        max_conflicts=0,
        require_consensus=True,
        min_findings=5
    ),
    max_iterations=5
)

# Execute (system autonomously iterates)
report = coordinator.process_goal(goal)

# Track refinement
print(f"Iterations: {report.iterations_completed}")
print(f"Goal achieved: {report.goal_achieved}")
for eval in report.evaluation_history:
    print(f"  Iter {eval.iteration}: {eval.confidence_score:.2%}")
```

#### Example 3: Hybrid Reasoning (Deterministic + LLM)

```python
from plugins.security_agent import SecurityAgent
from plugins.llm_reasoning_agent import LLMReasoningAgent

# Register both agent types
registry.register(
    SecurityAgent(bus),
    capabilities=['security', 'vulnerability'],
    priority=9  # High priority
)

registry.register(
    LLMReasoningAgent("llm-agent", bus),
    capabilities=['reasoning', 'edge-cases'],
    priority=6  # Medium priority
)

# Execute - both agents contribute
report = coordinator.process_task(task)
```

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      CLIENT INTERFACES                           │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   REST API   │    │     CLI      │    │  Python SDK  │      │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘      │
└─────────┼────────────────────┼────────────────────┼──────────────┘
          │                    │                    │
          └────────────────────┼────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                   GOAL EXECUTION LOOP                            │
│  Goal → Plan → Act → Evaluate → Refine → Repeat                │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    COORDINATOR                            │  │
│  │  • Orchestrates workflow                                 │  │
│  │  • Manages agent selection                               │  │
│  │  • Triggers conflict resolution                          │  │
│  │  • Aggregates results                                    │  │
│  └─────┬────────────────┬────────────────┬──────────────────┘  │
└────────┼────────────────┼────────────────┼─────────────────────┘
         │                │                │
         ▼                ▼                ▼
┌───────────────┐  ┌──────────┐  ┌─────────────┐
│Agent Registry │  │ Message  │  │   Shared    │
│ • Capability  │  │   Bus    │  │   Memory    │
│   matching    │  │ • Events │  │ • Learning  │
│ • Dynamic     │  │ • Pub/sub│  │ • Patterns  │
│   selection   │  │          │  │ • Context   │
└───────┬───────┘  └──────────┘  └─────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────────┐
│                   SPECIALIST AGENTS (Plugins)                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  DETERMINISTIC: Security, CodeQuality, Performance        │  │
│  │  MODEL-BASED: LLM Reasoning (Groq)                       │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              CONFLICT RESOLUTION + AGGREGATION                   │
│  • Weighted voting • Domain arbitration • Final report          │
└─────────────────────────────────────────────────────────────────┘
```

📖 **[View Detailed Architecture Diagram →](docs/ARCHITECTURE.md#-system-architecture-diagram)**

---

## 📁 Project Structure

```
AgentMesh/
├── agents/
│   ├── base_agent.py              # Abstract base class
│   └── coordinator_new.py         # Orchestration with goal loop
├── plugins/
│   ├── security_agent.py          # Security specialist (deterministic)
│   ├── code_quality_agent.py      # Quality specialist (deterministic)
│   ├── performance_agent.py       # Performance specialist (deterministic)
│   ├── documentation_agent.py     # Documentation specialist (deterministic)
│   └── llm_reasoning_agent.py     # LLM reasoning (probabilistic)
├── core/
│   ├── models.py                  # Data structures (Task, Goal, Finding, etc.)
│   ├── message_bus.py             # Event communication layer
│   ├── conflict_resolver.py       # Weighted conflict arbitration
│   ├── aggregator.py              # Report generation
│   ├── agent_registry.py          # Plugin management & capability routing
│   └── goal_evaluator.py          # Goal achievement assessment
├── memory/
│   └── shared_memory.py           # Stateful learning across iterations
├── api/
│   └── rest_api.py                # REST API interface
├── cli/
│   └── cli.py                     # Command-line interface
├── tests/
│   ├── test_*.py                  # Comprehensive test suite
│   └── verify_groq_api.py         # API key verification
├── docs/
│   ├── ARCHITECTURE.md            # Complete architecture documentation
│   ├── STEP7_GOAL_LOOP.md         # Goal-driven loop details
│   └── STEP8_SHARED_MEMORY.md     # Memory system details
├── config.py                      # Configuration (agents, LLM, etc.)
├── .env                           # Environment variables (API keys)
├── requirements.txt               # Dependencies
└── README.md                      # This file
```

---

## 🎓 Educational Value

### For System Design Interviews

**Topics Demonstrated:**
- ✅ Multi-agent orchestration patterns
- ✅ Plugin architectures and extensibility
- ✅ Conflict resolution algorithms
- ✅ Event-driven systems (message bus)
- ✅ Stateful vs stateless design
- ✅ Hybrid AI systems (deterministic + ML)
- ✅ Goal-driven autonomous systems
- ✅ Capability-based routing

### Interview Talking Points

**Q: "How would you design a system that automatically delegates tasks to appropriate workers?"**
→ AgentMesh capability-based routing with semantic matching

**Q: "How do you handle disagreements between multiple AI models?"**
→ AgentMesh weighted conflict resolution with domain-specific arbitration

**Q: "How would you build an extensible plugin system?"**
→ AgentMesh agent registry + BaseAgent interface with dynamic loading

**Q: "How do you combine rule-based and ML-based systems?"**
→ AgentMesh hybrid reasoning with deterministic + LLM agents

**Q: "How would you ensure an AI system improves over time?"**
→ AgentMesh goal loop + shared memory for continuous learning

---

## 🔧 Technical Highlights

### 1. Zero-Config Plugin System
```python
# Just extend BaseAgent and register
class MyAgent(BaseAgent):
    def _analyze(self, task): ...

registry.register(MyAgent(bus), capabilities=['custom'])
# Framework automatically routes relevant tasks
```

### 2. Intelligent Conflict Resolution
```python
# Scenario: Security vs Performance disagreement
Security: "BLOCK" (confidence=0.9, priority=9) → score=8.1
Performance: "APPROVE" (confidence=0.7, priority=5) → score=3.5
# Result: Security wins (higher weighted score)
```

### 3. Autonomous Quality Improvement
```python
# Define quality bar
goal = Goal(
    description="Review payment system",
    success_criteria=SuccessCriteria(min_confidence=0.9)
)
# System iterates until criteria met (no manual intervention)
```

### 4. Hybrid Reasoning
```python
# Deterministic: Pattern matching (fast, reliable)
SecurityAgent: "SQL injection found" (confidence=0.95)

# Probabilistic: LLM reasoning (flexible, creative)
LLMAgent: "Edge case: timezone handling" (confidence=0.70)

# Both contribute to final decision
```

---

## 🚀 Getting Started

### 1. Installation

```bash
git clone https://github.com/yourusername/AgentMesh.git
cd AgentMesh
pip install -r requirements.txt
```

### 2. Configure LLM (Optional)

```bash
# Get free API key from https://console.groq.com/
cp .env.example .env
# Edit .env: GROQ_API_KEY=your_key_here
```

### 3. Run Example

```python
python demo/demo_complete.py
```

### 4. Run Tests

```bash
# Unit tests
pytest tests/test_llm_reasoning_agent.py -v

# Integration test
python tests/test_step9_completion.py

# API verification
python tests/verify_groq_api.py
```

---

## 📚 Documentation

- **[Complete Architecture](docs/ARCHITECTURE.md)** - Full system design, components, data flows
- **[Goal Loop](docs/STEP7_GOAL_LOOP.md)** - Autonomous iterative refinement
- **[Shared Memory](docs/STEP8_SHARED_MEMORY.md)** - Stateful learning system
- **[Framework Conversion](FRAMEWORK_CONVERSION.md)** - Domain-agnostic design

---

## 🎯 Use Cases

### 1. Code Review System
```python
task = Task(
    description="Review authentication system for vulnerabilities",
    task_type="code_review"
)
report = coordinator.process_task(task)
# Automatic security + quality + performance analysis
```

### 2. Security Analysis Platform
```python
goal = Goal(
    description="Comprehensive security audit",
    success_criteria=SuccessCriteria(
        min_confidence=0.95,
        max_conflicts=0
    )
)
report = coordinator.process_goal(goal)
# Iterates until security standards met
```

### 3. Multi-Perspective Decision System
```python
# Multiple agents contribute different perspectives
# Conflicts resolved with weighted voting
# Final decision considers all viewpoints
```

---

## 🔮 Future Enhancements

**Potential Extensions:**
- [ ] Distributed agents (run on different machines)
- [ ] Real-time monitoring dashboard
- [ ] RL-based agent selection optimization
- [ ] Multi-modal support (image/video analysis)
- [ ] Database backend (PostgreSQL/MongoDB)
- [ ] Agent marketplace (share/download plugins)

---

## 🤝 Contributing

Contributions welcome! Areas of interest:
- New specialist agents (testing, documentation, etc.)
- Additional LLM providers (OpenAI, Anthropic, etc.)
- Performance optimizations
- Enhanced conflict resolution strategies

---

## 📄 License

MIT License - See LICENSE file for details

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)

---

## 🙏 Acknowledgments

Built as a production-ready demonstration of:
- Multi-agent system design
- Plugin architectures
- Autonomous AI systems
- Hybrid reasoning approaches

Perfect for:
- System design interviews
- AI architecture discussions
- Software engineering portfolios
- Academic research

---

**⭐ Star this repo if you find it useful!**

