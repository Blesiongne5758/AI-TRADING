import React, { useState, useEffect } from 'react';
import { Play, Settings, TrendingUp, DollarSign, Calendar } from 'lucide-react';
import axios from 'axios';

const BacktestPanel = ({ onBacktestComplete }) => {
  const [strategies, setStrategies] = useState([]);
  const [selectedStrategy, setSelectedStrategy] = useState('');
  const [strategyParams, setStrategyParams] = useState({});
  const [symbol, setSymbol] = useState('BTC/USDT');
  const [timeframe, setTimeframe] = useState('1h');
  const [startDate, setStartDate] = useState('2024-01-01');
  const [endDate, setEndDate] = useState('2024-12-31');
  const [initialBalance, setInitialBalance] = useState(10000);
  const [commission, setCommission] = useState(0.1);
  const [isRunning, setIsRunning] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadStrategies();
  }, []);

  const loadStrategies = async () => {
    try {
      const response = await axios.get('/api/backtest/strategies');
      setStrategies(response.data);
      if (response.data.length > 0) {
        setSelectedStrategy(response.data[0].name);
        setStrategyParams(response.data[0].default_params);
      }
    } catch (err) {
      setError('Failed to load strategies');
      console.error(err);
    }
  };

  const handleStrategyChange = (strategyName) => {
    setSelectedStrategy(strategyName);
    const strategy = strategies.find(s => s.name === strategyName);
    if (strategy) {
      setStrategyParams(strategy.default_params);
    }
  };

  const handleParamChange = (paramName, value) => {
    setStrategyParams(prev => ({
      ...prev,
      [paramName]: value
    }));
  };

  const handleRunBacktest = async () => {
    setIsRunning(true);
    setError('');

    try {
      const response = await axios.post('/api/backtest/run', {
        symbol,
        timeframe,
        start_date: startDate,
        end_date: endDate,
        strategy: selectedStrategy,
        strategy_params: strategyParams,
        initial_balance: initialBalance,
        commission: commission / 100
      });

      if (onBacktestComplete) {
        onBacktestComplete(response.data);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Backtest failed');
      console.error(err);
    } finally {
      setIsRunning(false);
    }
  };

  const selectedStrategyInfo = strategies.find(s => s.name === selectedStrategy);

  return (
    <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
      <div className="flex items-center gap-2 mb-6">
        <Settings className="w-6 h-6 text-blue-400" />
        <h2 className="text-2xl font-bold text-white">Backtest Configuration</h2>
      </div>

      {error && (
        <div className="bg-red-500/10 border border-red-500/50 rounded-lg p-4 mb-6">
          <p className="text-red-400">{error}</p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Symbol & Timeframe */}
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              <TrendingUp className="w-4 h-4 inline mr-1" />
              Symbol
            </label>
            <select
              value={symbol}
              onChange={(e) => setSymbol(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
            >
              <option value="BTC/USDT">BTC/USDT</option>
              <option value="ETH/USDT">ETH/USDT</option>
              <option value="SOL/USDT">SOL/USDT</option>
              <option value="BNB/USDT">BNB/USDT</option>
              <option value="XRP/USDT">XRP/USDT</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Timeframe
            </label>
            <select
              value={timeframe}
              onChange={(e) => setTimeframe(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
            >
              <option value="1m">1 Minute</option>
              <option value="5m">5 Minutes</option>
              <option value="15m">15 Minutes</option>
              <option value="1h">1 Hour</option>
              <option value="4h">4 Hours</option>
              <option value="1d">1 Day</option>
            </select>
          </div>
        </div>

        {/* Date Range */}
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              <Calendar className="w-4 h-4 inline mr-1" />
              Start Date
            </label>
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              <Calendar className="w-4 h-4 inline mr-1" />
              End Date
            </label>
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
            />
          </div>
        </div>

        {/* Strategy Selection */}
        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-slate-300 mb-2">
            Strategy
          </label>
          <select
            value={selectedStrategy}
            onChange={(e) => handleStrategyChange(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
          >
            {strategies.map(strategy => (
              <option key={strategy.name} value={strategy.name}>
                {strategy.name}
              </option>
            ))}
          </select>
          {selectedStrategyInfo && (
            <p className="text-sm text-slate-400 mt-2">
              {selectedStrategyInfo.description}
            </p>
          )}
        </div>

        {/* Strategy Parameters */}
        {selectedStrategyInfo && Object.keys(strategyParams).length > 0 && (
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Strategy Parameters
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 bg-slate-900/50 rounded-lg p-4 border border-slate-700">
              {Object.entries(strategyParams).map(([key, value]) => (
                <div key={key}>
                  <label className="block text-xs text-slate-400 mb-1">
                    {key}
                  </label>
                  <input
                    type="number"
                    value={value}
                    onChange={(e) => handleParamChange(key, parseFloat(e.target.value))}
                    className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-blue-500"
                  />
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Balance & Commission */}
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              <DollarSign className="w-4 h-4 inline mr-1" />
              Initial Balance ($)
            </label>
            <input
              type="number"
              value={initialBalance}
              onChange={(e) => setInitialBalance(parseFloat(e.target.value))}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-300 mb-2">
            Commission (%)
          </label>
          <input
            type="number"
            value={commission}
            onChange={(e) => setCommission(parseFloat(e.target.value))}
            step="0.01"
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
          />
        </div>
      </div>

      {/* Run Button */}
      <div className="mt-6">
        <button
          onClick={handleRunBacktest}
          disabled={isRunning}
          className={`w-full flex items-center justify-center gap-2 px-6 py-3 rounded-lg font-medium transition-colors ${
            isRunning
              ? 'bg-slate-700 text-slate-400 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700 text-white'
          }`}
        >
          <Play className="w-5 h-5" />
          {isRunning ? 'Running Backtest...' : 'Run Backtest'}
        </button>
      </div>
    </div>
  );
};

export default BacktestPanel;
