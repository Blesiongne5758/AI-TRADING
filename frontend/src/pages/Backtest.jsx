import React, { useState } from 'react';
import { BarChart3, Code, TrendingUp } from 'lucide-react';
import BacktestPanel from '../components/BacktestPanel';
import StrategyEditor from '../components/StrategyEditor';
import BacktestResults from '../components/BacktestResults';

const Backtest = () => {
  const [activeTab, setActiveTab] = useState('backtest');
  const [backtestResult, setBacktestResult] = useState(null);

  const handleBacktestComplete = (result) => {
    setBacktestResult(result);
    setActiveTab('results');
  };

  const handleStrategySaved = (strategy) => {
    console.log('Strategy saved:', strategy);
    // Could show a toast notification here
  };

  const tabs = [
    { id: 'backtest', label: 'Backtest', icon: BarChart3 },
    { id: 'strategies', label: 'Strategy Editor', icon: Code },
    { id: 'results', label: 'Results', icon: TrendingUp }
  ];

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Backtesting</h1>
        <p className="text-slate-400">
          Test and optimize your trading strategies with historical data
        </p>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 border-b border-slate-700">
        {tabs.map(tab => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-4 py-3 font-medium transition-colors relative ${
                activeTab === tab.id
                  ? 'text-blue-400'
                  : 'text-slate-400 hover:text-slate-300'
              }`}
            >
              <Icon className="w-4 h-4" />
              {tab.label}
              {activeTab === tab.id && (
                <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-400" />
              )}
            </button>
          );
        })}
      </div>

      {/* Tab Content */}
      <div className="mt-6">
        {activeTab === 'backtest' && (
          <BacktestPanel onBacktestComplete={handleBacktestComplete} />
        )}

        {activeTab === 'strategies' && (
          <StrategyEditor onStrategySaved={handleStrategySaved} />
        )}

        {activeTab === 'results' && (
          <BacktestResults result={backtestResult} />
        )}
      </div>
    </div>
  );
};

export default Backtest;
