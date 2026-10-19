import { useState, useEffect } from 'react';
import { portfolioAPI, signalsAPI, marketAPI, chatAPI, systemAPI } from '../api';

// ============================================
// Portfolio Hooks
// ============================================

export const usePortfolioSummary = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await portfolioAPI.getSummary();
        setData(response);
        setError(null);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { data, loading, error };
};

export const usePortfolioPositions = () => {
  const [positions, setPositions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPositions = async () => {
      try {
        setLoading(true);
        const response = await portfolioAPI.getPositions();
        setPositions(response.positions || []);
        setError(null);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchPositions();
  }, []);

  return { positions, loading, error };
};

// ============================================
// Signals Hooks
// ============================================

export const useActiveSignals = () => {
  const [signals, setSignals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSignals = async () => {
      try {
        setLoading(true);
        const response = await signalsAPI.getActive();
        setSignals(response.signals || []);
        setError(null);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchSignals();
  }, []);

  return { signals, loading, error };
};

export const useSignalAnalysis = (symbol, timeframe = '1h') => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        setLoading(true);
        const response = await signalsAPI.analyze(symbol, timeframe);
        setData(response);
        setError(null);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (symbol) {
      fetchAnalysis();
    }
  }, [symbol, timeframe]);

  return { data, loading, error };
};

// ============================================
// Market Hooks
// ============================================

export const useMarketTickers = () => {
  const [tickers, setTickers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTickers = async () => {
      try {
        setLoading(true);
        const response = await marketAPI.getTickers();
        setTickers(response.tickers || []);
        setError(null);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchTickers();
  }, []);

  return { tickers, loading, error };
};

export const useMarketCandles = (symbol, timeframe = '1h', limit = 100) => {
  const [candles, setCandles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCandles = async () => {
      try {
        setLoading(true);
        const response = await marketAPI.getCandles(symbol, timeframe, limit);
        setCandles(response.candles || []);
        setError(null);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (symbol) {
      fetchCandles();
    }
  }, [symbol, timeframe, limit]);

  return { candles, loading, error };
};

export const useMarketNews = (limit = 20) => {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchNews = async () => {
      try {
        setLoading(true);
        const response = await marketAPI.getNews(limit);
        setNews(response.news || []);
        setError(null);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchNews();
  }, [limit]);

  return { news, loading, error };
};

// ============================================
// Chat Hooks
// ============================================

export const useChat = () => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const sendMessage = async (message) => {
    try {
      setLoading(true);
      
      // Add user message
      const userMessage = { role: 'user', content: message, timestamp: new Date() };
      setMessages(prev => [...prev, userMessage]);

      // Get AI response
      const response = await chatAPI.sendMessage(message);
      
      // Add AI response
      const aiMessage = { 
        role: 'ai', 
        content: response.response, 
        timestamp: new Date() 
      };
      setMessages(prev => [...prev, aiMessage]);
      
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return { messages, sendMessage, loading, error };
};

export const useChatSuggestions = () => {
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSuggestions = async () => {
      try {
        setLoading(true);
        const response = await chatAPI.getSuggestions();
        setSuggestions(response.suggestions || []);
        setError(null);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchSuggestions();
  }, []);

  return { suggestions, loading, error };
};

// ============================================
// System Hooks
// ============================================

export const useSystemStatus = () => {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        setLoading(true);
        const response = await systemAPI.getStatus();
        setStatus(response);
        setError(null);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchStatus();
  }, []);

  return { status, loading, error };
};
