/**
 * Utility Functions
 */

/**
 * Format confidence percentage with color
 */
function formatConfidence(confidence) {
  if (confidence >= 90) return { text: `${Math.round(confidence)}%`, color: 'text-green-600' };
  if (confidence >= 75) return { text: `${Math.round(confidence)}%`, color: 'text-yellow-600' };
  if (confidence >= 60) return { text: `${Math.round(confidence)}%`, color: 'text-orange-600' };
  return { text: `${Math.round(confidence)}%`, color: 'text-red-600' };
}

/**
 * Format severity level
 */
function formatSeverity(severity) {
  const severities = {
    'CRITICAL': { color: 'bg-red-100 text-red-800', icon: '🔴' },
    'HIGH': { color: 'bg-orange-100 text-orange-800', icon: '🟠' },
    'MEDIUM': { color: 'bg-yellow-100 text-yellow-800', icon: '🟡' },
    'LOW': { color: 'bg-green-100 text-green-800', icon: '🟢' }
  };
  return severities[severity] || severities['LOW'];
}

/**
 * Truncate text with ellipsis
 */
function truncateText(text, maxLength = 50) {
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
}

/**
 * Format timestamp
 */
function formatTime(timestamp) {
  const date = new Date(timestamp);
  return date.toLocaleTimeString();
}

/**
 * Debounce function
 */
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

/**
 * Create a simple notification
 */
function showNotification(message, type = 'info') {
  const notification = document.createElement('div');
  notification.className = `fixed top-4 right-4 p-4 rounded shadow-lg z-50`;
  
  const bg = {
    'success': 'bg-green-500',
    'error': 'bg-red-500',
    'warning': 'bg-yellow-500',
    'info': 'bg-blue-500'
  }[type] || 'bg-blue-500';

  notification.className += ` ${bg} text-white`;
  notification.textContent = message;
  
  document.body.appendChild(notification);
  
  setTimeout(() => notification.remove(), 3000);
}

// Export for use in HTML scripts
window.Utils = {
  formatConfidence,
  formatSeverity,
  truncateText,
  formatTime,
  debounce,
  showNotification
};
