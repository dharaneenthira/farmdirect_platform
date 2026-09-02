/**
 * FarmDirect Frontend API Client Utility
 */
const API_BASE_URL = 'http://127.0.0.1:5000/api';

const ApiClient = {
  /**
   * Check backend health status
   * GET /api/health
   */
  async checkHealth() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      if (!response.ok) {
        throw new Error(`HTTP Error status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.warn('Backend API connection check failed:', error.message);
      return { status: 'error', message: error.message };
    }
  }
};
