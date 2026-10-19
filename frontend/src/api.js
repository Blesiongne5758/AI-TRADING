import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// ============================================
// Portfolio API
// ============================================

export const portfolioAPI = {
  getSummary: async () => {
    const response = await api.get('/api/portfolio/summary');
    return response.data;
  },

  getPositions: async () => {
    const response = await api.get('/api/portfolio/positions');
    return response.data;
  },

  getHistory: async (limit = 50) => {
    const response = await api.get('/api/portfolio/history', { params: { limit } });
    return response.data;
  },

  getEquityCurve: async (hours = 24) => {
    const response = await api.get('/api/portfolio/equity-curve', { params: { hours } });
    return response.data;
  },
};

// ============================================
// Signals API
// ============================================

export const signalsAPI = {
  analyze: async (symbol, timeframe = '1h') => {
    const response = await api.get(`/api/signals/analyze/${symbol}`, {
      params: { timeframe },
    });
    return response.data;
  },

  getActive: async () => {
    const response = await api.get('/api/signals/active');
    return response.data;
  },

  getHistory: async (limit = 20) => {
    const response = await api.get('/api/signals/history', { params: { limit } });
    return response.data;
  },
};

// ============================================
// Market API
// ============================================

export const marketAPI = {
  getTickers: async () => {
    const response = await api.get('/api/market/tickers');
    return response.data;
  },

  getCandles: async (symbol, timeframe = '1h', limit = 100) => {
    const response = await api.get(`/api/market/candles/${symbol}`, {
      params: { timeframe, limit },
    });
    return response.data;
  },

  getNews: async (limit = 20) => {
    const response = await api.get('/api/market/news', { params: { limit } });
    return response.data;
  },
};

// ============================================
// Chat API
// ============================================

export const chatAPI = {
  sendMessage: async (message) => {
    const response = await api.post('/api/chat/message', { message });
    return response.data;
  },

  getSuggestions: async () => {
    const response = await api.get('/api/chat/suggestions');
    return response.data;
  },
};

// ============================================
// System API
// ============================================

export const systemAPI = {
  getStatus: async () => {
    const response = await api.get('/api/status');
    return response.data;
  },

  healthCheck: async () => {
    const response = await api.get('/');
    return response.data;
  },
};

// ============================================
// WebSocket
// ============================================

export const createWebSocket = (onMessage, onError, onClose) => {
  const ws = new WebSocket('ws://localhost:8000/ws');

  ws.onopen = () => {
    console.log('✅ WebSocket connected');
    
    // Send ping every 30 seconds to keep connection alive
    const pingInterval = setInterval(() => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send('ping');
      }
    }, 30000);

    ws.onclose = () => {
      clearInterval(pingInterval);
      if (onClose) onClose();
    };
  };

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      if (onMessage) onMessage(data);
    } catch (error) {
      console.error('❌ WebSocket message parse error:', error);
    }
  };

  ws.onerror = (error) => {
    console.error('❌ WebSocket error:', error);
    if (onError) onError(error);
  };

  return ws;
};

export default api;
