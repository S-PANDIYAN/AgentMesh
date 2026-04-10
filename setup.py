#!/usr/bin/env python
"""
AgentMesh Framework - Multi-Agent Code Review System
Setup script for pip installation
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "AgentMesh" / "README.md").read_text(encoding="utf-8")

setup(
    name="agentmesh",
    version="1.0.0",
    author="AgentMesh Team",
    author_email="support@agentmesh.dev",
    description="Production-Ready Multi-Agent Orchestration Framework for Code Review",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/AgentMesh",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/AgentMesh/issues",
        "Documentation": "https://github.com/yourusername/AgentMesh/blob/main/README.md",
    },
    packages=find_packages(where="AgentMesh"),
    package_dir={"": "AgentMesh"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
    python_requires=">=3.10",
    install_requires=[
        "groq>=0.4.0",
        "python-dotenv>=1.0.0",
        "click>=8.0.0",
        "rich>=13.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "agentmesh=cli.agentmesh_cli:cli",
            "agentmesh-server=api.rest_api:main",
            "agentmesh-demo=main:main",
        ],
    },
    include_package_data=True,
    keywords="multi-agent orchestration code-review security framework",
    zip_safe=False,
)
