/**
 * API Integration Module
 * Handles all communication with AgentMesh REST API
 */

const API_BASE = 'http://localhost:5000';

class AgentMeshAPI {
  /**
   * Health check
   */
  static async checkHealth() {
    try {
      const response = await fetch(`${API_BASE}/health`);
      return await response.json();
    } catch (error) {
      console.error('Health check failed:', error);
      return null;
    }
  }

  /**
   * Get all available agents
   */
  static async getAgents() {
    try {
      const response = await fetch(`${API_BASE}/agents`);
      return await response.json();
    } catch (error) {
      console.error('Failed to fetch agents:', error);
      return [];
    }
  }

  /**
   * Submit code for review
   */
  static async submitReview(filePath, code, agents = null, priority = 'MEDIUM') {
    try {
      const payload = {
        file_path: filePath,
        code: code,
        priority: priority
      };
      
      if (agents) {
        payload.agents = agents;
      }

      const response = await fetch(`${API_BASE}/review`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });

      return await response.json();
    } catch (error) {
      console.error('Failed to submit review:', error);
      return { error: error.message };
    }
  }

  /**
   * Get task status
   */
  static async getTaskStatus(taskId) {
    try {
      const response = await fetch(`${API_BASE}/status/${taskId}`);
      return await response.json();
    } catch (error) {
      console.error(`Failed to get status for task ${taskId}:`, error);
      return null;
    }
  }

  /**
   * Get all tasks
   */
  static async getAllTasks() {
    try {
      const response = await fetch(`${API_BASE}/tasks`);
      return await response.json();
    } catch (error) {
      console.error('Failed to fetch tasks:', error);
      return [];
    }
  }

  /**
   * Reload agents/plugins
   */
  static async reloadAgents() {
    try {
      const response = await fetch(`${API_BASE}/reload`, {
        method: 'POST'
      });
      return await response.json();
    } catch (error) {
      console.error('Failed to reload agents:', error);
      return { error: error.message };
    }
  }

  /**
   * Select agents for a task
   */
  static async selectAgents(taskDescription) {
    try {
      const response = await fetch(`${API_BASE}/select`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ task_description: taskDescription })
      });

      return await response.json();
    } catch (error) {
      console.error('Failed to select agents:', error);
      return { error: error.message };
    }
  }

  /**
   * Poll task status until completion
   */
  static async pollTaskStatus(taskId, maxAttempts = 60, intervalMs = 1000) {
    for (let attempt = 0; attempt < maxAttempts; attempt++) {
      const status = await this.getTaskStatus(taskId);
      
      if (status && status.status === 'completed') {
        return status;
      }
      
      if (status && status.status === 'failed') {
        throw new Error(status.error || 'Task failed');
      }

      // Wait before next poll
      await new Promise(resolve => setTimeout(resolve, intervalMs));
    }

    throw new Error('Task polling timeout');
  }
}

// Export for use in HTML scripts
window.AgentMeshAPI = AgentMeshAPI;
