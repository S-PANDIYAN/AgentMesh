"""
REST API for AgentMesh Framework
Provides HTTP endpoints for task submission, status checking, and agent management.
"""
import uuid
import time
import threading
from typing import Dict, List, Any, Optional
from datetime import datetime
from queue import Queue
from flask import Flask, request, jsonify
from flask_cors import CORS

from framework_init import initialize_framework
from core.models import Task


class TaskQueue:
    """Thread-safe task queue with status tracking."""
    
    def __init__(self):
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.queue = Queue()
        self.lock = threading.Lock()
    
    def submit(self, task_id: str, task_data: Dict[str, Any]) -> str:
        """Submit a new task for processing."""
        with self.lock:
            self.tasks[task_id] = {
                'task_id': task_id,
                'status': 'queued',
                'submitted_at': datetime.utcnow().isoformat(),
                'data': task_data,
                'result': None,
                'error': None
            }
        self.queue.put(task_id)
        return task_id
    
    def get_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task status."""
        with self.lock:
            return self.tasks.get(task_id)
    
    def update_status(self, task_id: str, status: str, result: Any = None, error: str = None):
        """Update task status."""
        with self.lock:
            if task_id in self.tasks:
                self.tasks[task_id]['status'] = status
                self.tasks[task_id]['result'] = result
                self.tasks[task_id]['error'] = error
                self.tasks[task_id]['updated_at'] = datetime.utcnow().isoformat()
    
    def list_tasks(self, limit: int = 100) -> List[Dict[str, Any]]:
        """List recent tasks."""
        with self.lock:
            tasks = sorted(
                self.tasks.values(),
                key=lambda t: t.get('submitted_at', ''),
                reverse=True
            )
            return tasks[:limit]


class TaskWorker:
    """Background worker for processing tasks."""
    
    def __init__(self, task_queue: TaskQueue, coordinator, logger):
        self.task_queue = task_queue
        self.coordinator = coordinator
        self.logger = logger
        self.running = False
        self.thread: Optional[threading.Thread] = None
    
    def start(self):
        """Start the worker thread."""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._worker_loop, daemon=True)
            self.thread.start()
            self.logger.logger.info("Task worker started")
    
    def stop(self):
        """Stop the worker thread."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
            self.logger.logger.info("Task worker stopped")
    
    def _worker_loop(self):
        """Main worker loop."""
        while self.running:
            try:
                # Get task from queue (blocking with timeout)
                task_id = self.task_queue.queue.get(timeout=1)
                
                # Update status to processing
                self.task_queue.update_status(task_id, 'processing')
                
                # Get task data
                task_info = self.task_queue.get_status(task_id)
                if not task_info:
                    continue
                
                task_data = task_info['data']
                
                # Create Task object
                task = Task(
                    task_id=task_id,
                    description=task_data.get('description', ''),
                    priority=task_data.get('priority', 'MEDIUM'),
                    task_type=task_data.get('task_type', 'code_review'),
                    payload=task_data.get('payload', {})
                )
                
                # Process task
                start_time = time.time()
                report = self.coordinator.process_task(task)
                processing_time = time.time() - start_time
                
                # Prepare result
                result = {
                    'task_id': task_id,
                    'decision': report.final_decision,
                    'confidence': report.confidence_score,
                    'agents_consulted': len(report.agent_reports),
                    'findings': [
                        {
                            'agent': r.agent_id,
                            'decision': r.decision,
                            'confidence': r.confidence,
                            'findings': r.findings
                        }
                        for r in report.agent_reports
                    ],
                    'conflicts_resolved': report.conflicts_resolved,
                    'processing_time_ms': round(processing_time * 1000, 2)
                }
                
                # Update status to completed
                self.task_queue.update_status(task_id, 'completed', result=result)
                self.logger.logger.info(f"Task {task_id} completed in {processing_time*1000:.2f}ms")
                
            except Exception as e:
                if hasattr(e, '__name__') and 'Empty' in str(type(e)):
                    # Queue timeout - continue
                    continue
                
                # Update task status to failed
                if 'task_id' in locals():
                    self.task_queue.update_status(
                        task_id,
                        'failed',
                        error=str(e)
                    )
                self.logger.logger.error(f"Task processing error: {e}")


# Initialize framework
registry, loader, coordinator, logger = initialize_framework()

# Create task queue and worker
task_queue = TaskQueue()
worker = TaskWorker(task_queue, coordinator, logger)
worker.start()

# Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'agents_loaded': len(registry.list_agents()),
        'tasks_queued': task_queue.queue.qsize()
    })


@app.route('/agents', methods=['GET'])
def list_agents():
    """List all available agents."""
    agents = registry.list_agents()
    agent_info = []
    
    for agent in agents:
        capabilities = registry.get_agent_capabilities(agent.agent_id)
        priority = registry._agent_priorities.get(agent.agent_id, 5)
        
        agent_info.append({
            'id': agent.agent_id,
            'type': agent.agent_type.value,
            'capabilities': capabilities,
            'priority': priority,
            'description': agent.description if hasattr(agent, 'description') else ''
        })
    
    return jsonify({
        'agents': agent_info,
        'total': len(agent_info)
    })


@app.route('/review', methods=['POST'])
def submit_review():
    """Submit a code review task."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        if 'description' not in data and 'code' not in data.get('payload', {}):
            return jsonify({'error': 'description or payload.code required'}), 400
        
        # Generate task ID
        task_id = data.get('task_id', f"task-{uuid.uuid4().hex[:8]}")
        
        # Submit to queue
        task_queue.submit(task_id, data)
        
        return jsonify({
            'task_id': task_id,
            'status': 'queued',
            'message': 'Task submitted successfully'
        }), 202
        
    except Exception as e:
        logger.logger.error(f"Error submitting task: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/status/<task_id>', methods=['GET'])
def get_task_status(task_id: str):
    """Get task status and result."""
    task_info = task_queue.get_status(task_id)
    
    if not task_info:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(task_info)


@app.route('/tasks', methods=['GET'])
def list_tasks():
    """List recent tasks."""
    limit = request.args.get('limit', 100, type=int)
    tasks = task_queue.list_tasks(limit=limit)
    
    return jsonify({
        'tasks': tasks,
        'total': len(tasks)
    })


@app.route('/reload', methods=['POST'])
def reload_plugins():
    """Hot-reload all plugins."""
    try:
        results = loader.reload_all_plugins()
        
        # Re-register agents
        registry._agents.clear()
        registry._capabilities.clear()
        
        for plugin_name, plugin_info in loader.loaded_plugins.items():
            agent = loader.create_agent_instance(plugin_name, coordinator.message_bus)
            capabilities = plugin_info.get('capabilities', [])
            priority = plugin_info.get('priority', 5)
            
            registry.register(
                agent,
                capabilities=capabilities,
                priority=priority
            )
        
        return jsonify({
            'message': 'Plugins reloaded successfully',
            'results': results,
            'agents_loaded': len(registry.list_agents())
        })
        
    except Exception as e:
        logger.logger.error(f"Error reloading plugins: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/select', methods=['POST'])
def select_agents():
    """Select agents for a task based on description."""
    try:
        data = request.get_json()
        
        if not data or 'description' not in data:
            return jsonify({'error': 'description required'}), 400
        
        description = data['description']
        use_weighted = data.get('use_weighted', False)
        min_score = data.get('min_score', 0.0)
        
        # Select agents
        selected = registry.auto_select_agents(
            description,
            use_weighted=use_weighted,
            min_score=min_score
        )
        
        return jsonify({
            'description': description,
            'agents_selected': [
                {
                    'id': agent.agent_id,
                    'type': agent.agent_type.value,
                    'capabilities': registry.get_agent_capabilities(agent.agent_id)
                }
                for agent in selected
            ],
            'total': len(selected)
        })
        
    except Exception as e:
        logger.logger.error(f"Error selecting agents: {e}")
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.logger.error(f"Internal error: {error}")
    return jsonify({'error': 'Internal server error'}), 500


def run_api(host='0.0.0.0', port=5000, debug=False):
    """Run the Flask API server."""
    logger.logger.info(f"Starting AgentMesh API on {host}:{port}")
    logger.logger.info(f"Loaded {len(registry.list_agents())} agents")
    
    try:
        app.run(host=host, port=port, debug=debug, threaded=True)
    finally:
        worker.stop()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='AgentMesh REST API Server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    run_api(host=args.host, port=args.port, debug=args.debug)
