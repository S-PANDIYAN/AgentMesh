# 📦 AgentMesh CLI Tool - Installation & Deployment Guide

## Quick Install

### Option 1: Install from Source (Development)
```bash
git clone <repository-url>
cd AgentMesh
pip install -e .
```

### Option 2: Install as Package (Production)
```bash
pip install agentmesh
```

---

## 🚀 Quick Start

Once installed, you can use these commands from anywhere in your terminal:

### Command-Line Interface
```bash
# List all agents
agentmesh agents

# Review a code file
agentmesh review mycode.py

# Select agents for a task
agentmesh select "Check for security issues"

# Show help
agentmesh --help
```

### REST API Server
```bash
# Start the API server
agentmesh-server --port 5000

# Use with different options
agentmesh-server --host 127.0.0.1 --port 8000 --debug
```

### Interactive Demo
```bash
# Run the interactive menu
agentmesh-demo
```

---

## 📋 Available Commands

### agentmesh (CLI Tool)

```bash
agentmesh --help                    # Show all commands
agentmesh agents                    # List agents
agentmesh review <file>             # Review code
agentmesh select <description>      # Select agents
agentmesh reload                    # Reload plugins
agentmesh benchmark --tasks 100     # Run benchmark
```

### agentmesh-server (REST API)

```bash
agentmesh-server                    # Start on 0.0.0.0:5000
agentmesh-server --port 8000        # Custom port
agentmesh-server --debug            # Debug mode
agentmesh-server --help             # Show options
```

### agentmesh-demo (Interactive Demo)

```bash
agentmesh-demo                      # Run interactive menu
```

---

## 💻 Installation Methods

### Windows (PowerShell)

**Method 1: Global Install**
```powershell
# Install from source
git clone <repo>
cd AgentMesh
pip install -e .

# Test installation
agentmesh --help
agentmesh agents
```

**Method 2: Virtual Environment (Recommended)**
```powershell
# Create venv
python -m venv agentmesh_env
agentmesh_env\Scripts\Activate.ps1

# Install
pip install -e .

# Run
agentmesh agents
```

### macOS / Linux (Bash)

**Method 1: Global Install**
```bash
# Install from source
git clone <repo>
cd AgentMesh
pip install -e .

# Test
agentmesh --help
agentmesh agents
```

**Method 2: Virtual Environment (Recommended)**
```bash
# Create venv
python3 -m venv agentmesh_env
source agentmesh_env/bin/activate

# Install
pip install -e .

# Run
agentmesh agents
```

---

## 🔧 Configuration

### Environment Variables

Create `.env` file in your project directory:

```bash
# Groq API Key (Optional - for LLM agent)
GROQ_API_KEY=your_actual_key_here

# Add more as needed
DEBUG=True
LOG_LEVEL=DEBUG
```

Get free Groq API key: https://console.groq.com/

---

## 📖 Usage Examples

### Example 1: Review a Python File
```bash
# Review your code
agentmesh review path/to/mycode.py

# With JSON output
agentmesh review path/to/mycode.py --format json

# Save report
agentmesh review path/to/mycode.py --save
```

### Example 2: Select Agents for Task
```bash
# Standard selection
agentmesh select "Check for SQL injection"

# Weighted selection
agentmesh select "performance optimization" --weighted
```

### Example 3: List All Agents
```bash
# Text format (default)
agentmesh agents

# JSON format
agentmesh agents --format json
```

### Example 4: Start REST API
```bash
# Start server
agentmesh-server

# Then in another terminal:
curl http://localhost:5000/agents
curl http://localhost:5000/health
```

---

## 🐳 Docker Deployment (Optional)

### Build Docker Image
```bash
docker build -t agentmesh:latest .
```

### Run with Docker
```bash
# Interactive demo
docker run -it agentmesh:latest agentmesh-demo

# CLI command
docker run agentmesh:latest agentmesh agents

# REST API
docker run -p 5000:5000 agentmesh:latest agentmesh-server
```

---

## ✅ Verify Installation

```bash
# Check Python version
python --version          # Should be 3.10+

# Check pip installation
pip show agentmesh        # Should show package info

# Test CLI
agentmesh --version       # Show version
agentmesh --help          # Show help

# Test framework
agentmesh agents          # Should list 4 agents
```

---

## 🆘 Troubleshooting

### Issue: Command not found
```bash
# Make sure it's installed
pip install -e .

# Or check PATH
pip show -f agentmesh
```

### Issue: ModuleNotFoundError
```bash
# Reinstall
pip install -e . --force-reinstall

# Or use virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\Activate.ps1
pip install -e .
```

### Issue: Permission denied (macOS/Linux)
```bash
# Try with user flag
pip install --user -e .

# Or use virtual environment
python -m venv venv
source venv/bin/activate
pip install -e .
```

### Issue: Port already in use
```bash
# Use different port
agentmesh-server --port 8000
```

---

## 📦 Package Contents

```
agentmesh/
├── cli/              → Command-line interface
├── api/              → REST API server
├── core/             → Core framework
├── agents/           → Agent coordination
├── plugins/          → Specialist agents
├── memory/           → Shared memory system
└── tests/            → Test suite
```

**4 Built-in Agents:**
- SecurityAgent (Vulnerability detection)
- CodeQualityAgent (Code structure & style)
- PerformanceAgent (Optimization analysis)
- DocumentationAgent (Documentation quality)

---

## 🚀 Deployment Options

### Option 1: Local CLI
```bash
agentmesh review mycode.py
```

### Option 2: CI/CD Pipeline
```bash
# Add to GitHub Actions
- name: Review with AgentMesh
  run: agentmesh review ${{ github.workspace }}
```

### Option 3: API Server
```bash
# Production deployment
agentmesh-server --host 0.0.0.0 --port 5000
```

### Option 4: Docker Container
```bash
docker run -p 5000:5000 agentmesh:latest agentmesh-server
```

---

## 📝 Development

### Install with Dev Dependencies
```bash
pip install -e ".[dev]"
```

### Run Tests
```bash
pytest tests/ -v
```

### Code Quality
```bash
black .
flake8 .
mypy .
```

---

## 📚 Documentation

- `INSTALLATION_GUIDE.md` - Detailed installation
- `README.md` - Project overview
- `USER_GUIDE.md` - Feature documentation
- `docs/ARCHITECTURE.md` - System design

---

## 🔐 Security Notes

- Keep `GROQ_API_KEY` in `.env` file (never commit)
- Use `.gitignore` to exclude `.env` and logs
- API server should be behind reverse proxy in production
- Use environment variables for sensitive data

---

## 📞 Support

- Check documentation in `docs/`
- Review examples in `examples/`
- Run tests to verify setup
- Check logs in `logs/` directory

---

**✅ Installation Complete! You can now use AgentMesh from anywhere! 🎉**

```bash
agentmesh agents
```
