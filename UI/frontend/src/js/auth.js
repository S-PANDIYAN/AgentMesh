/**
 * Frontend Authentication Module
 * Handles user authentication with the backend (JWT tokens and API keys)
 */

class AuthManager {
  /**
   * Initialize auth manager
   */
  static init() {
    this.loadFromStorage();
    this.setupInterceptors();
  }

  /**
   * Load authentication data from localStorage
   */
  static loadFromStorage() {
    try {
      this.accessToken = localStorage.getItem('agentmesh_access_token');
      this.apiKey = localStorage.getItem('agentmesh_api_key');
      this.userId = localStorage.getItem('agentmesh_user_id');
      this.username = localStorage.getItem('agentmesh_username');
      this.expiresAt = localStorage.getItem('agentmesh_expires_at');
    } catch (error) {
      console.error('Failed to load auth data from storage:', error);
    }
  }

  /**
   * Save authentication data to localStorage
   */
  static saveToStorage() {
    try {
      if (this.accessToken) localStorage.setItem('agentmesh_access_token', this.accessToken);
      if (this.apiKey) localStorage.setItem('agentmesh_api_key', this.apiKey);
      if (this.userId) localStorage.setItem('agentmesh_user_id', this.userId);
      if (this.username) localStorage.setItem('agentmesh_username', this.username);
      if (this.expiresAt) localStorage.setItem('agentmesh_expires_at', this.expiresAt);
    } catch (error) {
      console.error('Failed to save auth data to storage:', error);
    }
  }

  /**
   * Register new user
   */
  static async register(email, username, password) {
    try {
      const response = await fetch(`${CONFIG.API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, username, password })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Registration failed');
      }

      const data = await response.json();
      this.setAuth(data);
      return { success: true, data };
    } catch (error) {
      console.error('Registration error:', error);
      return { success: false, error: error.message };
    }
  }

  /**
   * Login user
   */
  static async login(email, password) {
    try {
      const response = await fetch(`${CONFIG.API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Login failed');
      }

      const data = await response.json();
      this.setAuth(data);
      return { success: true, data };
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, error: error.message };
    }
  }

  /**
   * Set authentication data
   */
  static setAuth(data) {
    this.accessToken = data.access_token;
    this.apiKey = data.api_key;
    this.userId = data.user_id;
    this.username = data.username || data.email;
    
    // JWT tokens expire in 1 hour
    const expiresAt = new Date().getTime() + 3600000;
    this.expiresAt = expiresAt.toString();
    
    this.saveToStorage();
    
    if (CONFIG.DEBUG_MODE) {
      console.log('Authentication set:', { userId: this.userId, username: this.username });
    }
  }

  /**
   * Logout user
   */
  static logout() {
    this.accessToken = null;
    this.apiKey = null;
    this.userId = null;
    this.username = null;
    this.expiresAt = null;
    
    try {
      localStorage.removeItem('agentmesh_access_token');
      localStorage.removeItem('agentmesh_api_key');
      localStorage.removeItem('agentmesh_user_id');
      localStorage.removeItem('agentmesh_username');
      localStorage.removeItem('agentmesh_expires_at');
    } catch (error) {
      console.error('Failed to clear storage:', error);
    }
  }

  /**
   * Check if user is authenticated
   */
  static isAuthenticated() {
    if (!this.accessToken && !this.apiKey) {
      return false;
    }

    // Check token expiration
    if (this.expiresAt) {
      const now = new Date().getTime();
      if (now > parseInt(this.expiresAt)) {
        this.logout();
        return false;
      }
    }

    return true;
  }

  /**
   * Validate current token
   */
  static async validateToken() {
    try {
      const response = await fetch(`${CONFIG.API_BASE_URL}/auth/validate-token`, {
        method: 'GET',
        headers: this.getAuthHeaders()
      });

      if (!response.ok) {
        this.logout();
        return false;
      }

      const data = await response.json();
      return !!data.user_id;
    } catch (error) {
      console.error('Token validation error:', error);
      return false;
    }
  }

  /**
   * Generate new API key
   */
  static async generateAPIKey(name, rateLimit = 100) {
    try {
      const response = await fetch(`${CONFIG.API_BASE_URL}/api-keys/generate`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({ name, rate_limit: rateLimit })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to generate API key');
      }

      const data = await response.json();
      this.apiKey = data.api_key;
      this.saveToStorage();
      return { success: true, apiKey: data.api_key };
    } catch (error) {
      console.error('API key generation error:', error);
      return { success: false, error: error.message };
    }
  }

  /**
   * Get authentication headers
   */
  static getAuthHeaders() {
    const headers = { 'Content-Type': 'application/json' };

    if (this.apiKey) {
      headers['X-API-Key'] = this.apiKey;
    } else if (this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`;
    }

    return headers;
  }

  /**
   * Setup request interceptors
   */
  static setupInterceptors() {
    // Store original fetch
    const originalFetch = window.fetch;

    // Override fetch to add auth headers
    window.fetch = function(...args) {
      const [resource, config] = args;
      const url = typeof resource === 'string' ? resource : resource.url;

      // Only add auth to AgentMesh API calls
      if (url && url.includes(CONFIG.API_BASE_URL)) {
        const newConfig = config || {};
        newConfig.headers = { ...newConfig.headers, ...AuthManager.getAuthHeaders() };
        return originalFetch(resource, newConfig);
      }

      return originalFetch(...args);
    };
  }

  /**
   * Get user info
   */
  static getUserInfo() {
    return {
      userId: this.userId,
      username: this.username,
      apiKey: this.apiKey ? this.apiKey.substring(0, 10) + '...' : null,
      isAuthenticated: this.isAuthenticated()
    };
  }
}

// Initialize on load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => AuthManager.init());
} else {
  AuthManager.init();
}

// Export for use
window.AuthManager = AuthManager;
