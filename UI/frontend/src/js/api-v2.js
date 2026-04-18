/**
 * Frontend API Integration Module v2
 * Handles all communication with AgentMesh REST API v2
 */

class AgentMeshAPIv2 {
  /**
   * Health check
   */
  static async checkHealth() {
    try {
      const response = await fetch(`${CONFIG.API_BASE_URL}/health`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error('Health check failed:', error);
      return { status: 'unhealthy', error: error.message };
    }
  }

  /**
   * ==================== AUTHENTICATION ====================
   */

  /**
   * Register new user
   */
  static async register(email, username, password) {
    return AuthManager.register(email, username, password);
  }

  /**
   * Login user
   */
  static async login(email, password) {
    return AuthManager.login(email, password);
  }

  /**
   * Logout user
   */
  static logout() {
    AuthManager.logout();
    return { success: true };
  }

  /**
   * Validate token
   */
  static async validateToken() {
    return AuthManager.validateToken();
  }

  /**
   * ==================== API KEYS ====================
   */

  /**
   * Generate API key
   */
  static async generateAPIKey(name, rateLimit = 100) {
    return AuthManager.generateAPIKey(name, rateLimit);
  }

  /**
   * List API keys
   */
  static async listAPIKeys() {
    try {
      const response = await fetch(`${CONFIG.API_BASE_URL}/api-keys`, {
        headers: AuthManager.getAuthHeaders()
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error('Failed to list API keys:', error);
      return { error: error.message };
    }
  }

  /**
   * Revoke API key
   */
  static async revokeAPIKey(keyId) {
    try {
      const response = await fetch(`${CONFIG.API_BASE_URL}/api-keys/${keyId}`, {
        method: 'DELETE',
        headers: AuthManager.getAuthHeaders()
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error('Failed to revoke API key:', error);
      return { error: error.message };
    }
  }

  /**
   * ==================== ANALYSIS ====================
   */

  /**
   * Submit code for analysis
   */
  static async submitAnalysis(code, fileName = null, description = null, agents = null, priority = 'MEDIUM') {
    try {
      const payload = {
        code,
        file_name: fileName || 'code.py',
        description: description || 'Code analysis',
        agents: agents || ['security', 'code_quality'],
        priority
      };

      const response = await fetch(`${CONFIG.API_BASE_URL}/review`, {
        method: 'POST',
        headers: AuthManager.getAuthHeaders(),
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || `HTTP ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Failed to submit analysis:', error);
      return { error: error.message };
    }
  }

  /**
   * Get analysis results
   */
  static async getAnalysis(analysisId) {
    try {
      const response = await fetch(`${CONFIG.API_BASE_URL}/analyses/${analysisId}`, {
        headers: AuthManager.getAuthHeaders()
      });

      if (!response.ok) {
        if (response.status === 404) throw new Error('Analysis not found');
        throw new Error(`HTTP ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`Failed to get analysis ${analysisId}:`, error);
      return { error: error.message };
    }
  }

  /**
   * List analyses
   */
  static async listAnalyses(limit = 50, status = null) {
    try {
      let url = `${CONFIG.API_BASE_URL}/analyses?limit=${limit}`;
      if (status) url += `&status=${status}`;

      const response = await fetch(url, {
        headers: AuthManager.getAuthHeaders()
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error('Failed to list analyses:', error);
      return { analyses: [], error: error.message };
    }
  }

  /**
   * ==================== REPORTS ====================
   */

  /**
   * Generate report
   */
  static async generateReport(analysisId, format = 'json', template = 'default') {
    try {
      const response = await fetch(`${CONFIG.API_BASE_URL}/reports/${analysisId}`, {
        method: 'POST',
        headers: AuthManager.getAuthHeaders(),
        body: JSON.stringify({ format, template })
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);

      if (format === 'json') {
        return await response.json();
      } else if (format === 'html') {
        return await response.text();
      } else if (format === 'pdf') {
        return await response.blob();
      }
    } catch (error) {
      console.error('Failed to generate report:', error);
      return { error: error.message };
    }
  }

  /**
   * ==================== FILE MANAGEMENT ====================
   */

  /**
   * Upload file
   */
  static async uploadFile(file) {
    try {
      if (file.size > CONFIG.MAX_FILE_SIZE) {
        throw new Error(`File size exceeds ${CONFIG.MAX_FILE_SIZE / 1024 / 1024}MB limit`);
      }

      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`${CONFIG.API_BASE_URL}/upload`, {
        method: 'POST',
        headers: { 'X-API-Key': AuthManager.apiKey || '' },
        body: formData
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || `HTTP ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Failed to upload file:', error);
      return { error: error.message };
    }
  }

  /**
   * Get file content
   */
  static async getFile(fileId) {
    try {
      const response = await fetch(`${CONFIG.API_BASE_URL}/files/${fileId}`, {
        headers: AuthManager.getAuthHeaders()
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error(`Failed to get file ${fileId}:`, error);
      return { error: error.message };
    }
  }

  /**
   * ==================== ANALYTICS ====================
   */

  /**
   * Get dashboard analytics
   */
  static async getDashboardAnalytics() {
    try {
      const response = await fetch(`${CONFIG.API_BASE_URL}/analytics/dashboard`, {
        headers: AuthManager.getAuthHeaders()
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error('Failed to get dashboard analytics:', error);
      return { error: error.message };
    }
  }

  /**
   * Get quality trends
   */
  static async getQualityTrends(days = 30) {
    try {
      const response = await fetch(`${CONFIG.API_BASE_URL}/analytics/trends?days=${days}`, {
        headers: AuthManager.getAuthHeaders()
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error('Failed to get quality trends:', error);
      return { error: error.message };
    }
  }

  /**
   * Get comprehensive analytics
   */
  static async getComprehensiveAnalytics() {
    try {
      const response = await fetch(`${CONFIG.API_BASE_URL}/analytics/comprehensive`, {
        headers: AuthManager.getAuthHeaders()
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error('Failed to get comprehensive analytics:', error);
      return { error: error.message };
    }
  }

  /**
   * ==================== NOTIFICATIONS ====================
   */

  /**
   * Get notifications
   */
  static async getNotifications(unreadOnly = false, limit = 50) {
    try {
      let url = `${CONFIG.API_BASE_URL}/notifications?unread=${unreadOnly}&limit=${limit}`;

      const response = await fetch(url, {
        headers: AuthManager.getAuthHeaders()
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error('Failed to get notifications:', error);
      return { notifications: [], error: error.message };
    }
  }

  /**
   * ==================== POLLING & HELPERS ====================
   */

  /**
   * Poll analysis status until completion
   */
  static async pollAnalysisStatus(analysisId, maxAttempts = null, intervalMs = null) {
    maxAttempts = maxAttempts || CONFIG.POLL_MAX_ATTEMPTS;
    intervalMs = intervalMs || CONFIG.POLL_INTERVAL;

    for (let attempt = 0; attempt < maxAttempts; attempt++) {
      const analysis = await this.getAnalysis(analysisId);

      if (analysis.error) {
        throw new Error(analysis.error);
      }

      if (analysis.status === 'COMPLETED') {
        return analysis;
      }

      if (analysis.status === 'FAILED') {
        throw new Error(analysis.error || 'Analysis failed');
      }

      // Wait before next poll
      await new Promise(resolve => setTimeout(resolve, intervalMs));
    }

    throw new Error(`Analysis polling timeout after ${maxAttempts} attempts`);
  }

  /**
   * Submit analysis and wait for results
   */
  static async analyzeAndWait(code, fileName = null, agents = null, priority = 'MEDIUM') {
    try {
      // Submit
      const submitResult = await this.submitAnalysis(code, fileName, null, agents, priority);

      if (submitResult.error) {
        throw new Error(submitResult.error);
      }

      const analysisId = submitResult.analysis_id;

      if (CONFIG.DEBUG_MODE) {
        console.log('Analysis submitted:', analysisId);
      }

      // Wait for completion
      const results = await this.pollAnalysisStatus(analysisId);
      return { success: true, analysis: results };
    } catch (error) {
      console.error('Analyze and wait error:', error);
      return { success: false, error: error.message };
    }
  }
}

// Export for use
window.AgentMeshAPI = AgentMeshAPIv2;
window.AgentMeshAPIv2 = AgentMeshAPIv2;
