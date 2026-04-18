/**
 * Frontend Environment Configuration
 * Update these values based on your deployment environment
 */

// API Configuration
const CONFIG = {
  // Backend API URL
  API_BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:5000',
  
  // Authentication
  AUTH_TIMEOUT: 3600000, // 1 hour in milliseconds
  
  // Request timeouts
  REQUEST_TIMEOUT: 30000, // 30 seconds
  
  // File uploads
  MAX_FILE_SIZE: 100 * 1024 * 1024, // 100MB
  
  // Features
  ENABLE_WEBHOOKS: true,
  ENABLE_NOTIFICATIONS: true,
  ENABLE_ANALYTICS: true,
  
  // Logging
  DEBUG_MODE: false,
  LOG_LEVEL: 'info', // 'debug', 'info', 'warn', 'error'
  
  // Polling
  POLL_INTERVAL: 2000, // 2 seconds
  POLL_MAX_ATTEMPTS: 150, // 5 minutes total
};

/**
 * Get configuration value with environment variable override
 */
function getConfig(key, defaultValue) {
  const envKey = 'REACT_APP_' + key.toUpperCase();
  return process.env[envKey] || CONFIG[key] || defaultValue;
}

/**
 * Environment detection
 */
function isProduction() {
  return process.env.NODE_ENV === 'production';
}

function isDevelopment() {
  return process.env.NODE_ENV === 'development';
}

// Export configuration
window.CONFIG = CONFIG;
window.getConfig = getConfig;
window.isProduction = isProduction;
window.isDevelopment = isDevelopment;
