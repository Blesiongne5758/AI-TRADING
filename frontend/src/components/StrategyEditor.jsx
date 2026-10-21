import React, { useState, useEffect } from 'react';
import { Code, Save, Plus, Trash2, Edit2 } from 'lucide-react';
import axios from 'axios';

const StrategyEditor = ({ onStrategySaved }) => {
  const [customStrategies, setCustomStrategies] = useState([]);
  const [selectedStrategy, setSelectedStrategy] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [strategyName, setStrategyName] = useState('');
  const [strategyDescription, setStrategyDescription] = useState('');
  const [conditions, setConditions] = useState([]);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    loadCustomStrategies();
  }, []);

  const loadCustomStrategies = async () => {
    try {
      const response = await axios.get('/api/backtest/custom-strategies');
      setCustomStrategies(response.data);
    } catch (err) {
      console.error('Failed to load custom strategies:', err);
    }
  };

  const handleNewStrategy = () => {
    setSelectedStrategy(null);
    setIsEditing(true);
    setStrategyName('');
    setStrategyDescription('');
    setConditions([]);
    setError('');
    setSuccess('');
  };

  const handleEditStrategy = (strategy) => {
    setSelectedStrategy(strategy);
    setIsEditing(true);
    setStrategyName(strategy.name);
    setStrategyDescription(strategy.description);
    setConditions(strategy.conditions || []);
    setError('');
    setSuccess('');
  };

  const handleDeleteStrategy = async (strategyId) => {
    if (!window.confirm('Are you sure you want to delete this strategy?')) {
      return;
    }

    try {
      await axios.delete(`/api/backtest/custom-strategies/${strategyId}`);
      setCustomStrategies(prev => prev.filter(s => s.id !== strategyId));
      if (selectedStrategy?.id === strategyId) {
        setSelectedStrategy(null);
        setIsEditing(false);
      }
    } catch (err) {
      setError('Failed to delete strategy');
      console.error(err);
    }
  };

  const handleAddCondition = () => {
    setConditions(prev => [
      ...prev,
      {
        id: Date.now(),
        indicator: 'rsi',
        operator: 'less_than',
        value: 30,
        logic: 'AND'
      }
    ]);
  };

  const handleUpdateCondition = (id, field, value) => {
    setConditions(prev =>
      prev.map(cond =>
        cond.id === id ? { ...cond, [field]: value } : cond
      )
    );
  };

  const handleRemoveCondition = (id) => {
    setConditions(prev => prev.filter(cond => cond.id !== id));
  };

  const handleSaveStrategy = async () => {
    setError('');
    setSuccess('');

    if (!strategyName.trim()) {
      setError('Strategy name is required');
      return;
    }

    if (conditions.length === 0) {
      setError('At least one condition is required');
      return;
    }

    try {
      const payload = {
        name: strategyName,
        description: strategyDescription,
        conditions: conditions
      };

      let response;
      if (selectedStrategy) {
        // Update existing strategy
        response = await axios.put(
          `/api/backtest/custom-strategies/${selectedStrategy.id}`,
          payload
        );
        setSuccess('Strategy updated successfully');
      } else {
        // Create new strategy
        response = await axios.post('/api/backtest/custom-strategies', payload);
        setSuccess('Strategy created successfully');
      }

      await loadCustomStrategies();
      setIsEditing(false);
      setSelectedStrategy(null);

      if (onStrategySaved) {
        onStrategySaved(response.data);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save strategy');
      console.error(err);
    }
  };

  const handleCancel = () => {
    setIsEditing(false);
    setSelectedStrategy(null);
    setStrategyName('');
    setStrategyDescription('');
    setConditions([]);
    setError('');
    setSuccess('');
  };

  const indicators = [
    { value: 'rsi', label: 'RSI' },
    { value: 'macd', label: 'MACD' },
    { value: 'ema', label: 'EMA' },
    { value: 'sma', label: 'SMA' },
    { value: 'bollinger', label: 'Bollinger Bands' },
    { value: 'volume', label: 'Volume' },
    { value: 'price', label: 'Price' }
  ];

  const operators = [
    { value: 'less_than', label: '<' },
    { value: 'greater_than', label: '>' },
    { value: 'equals', label: '=' },
    { value: 'crosses_above', label: 'Crosses Above' },
    { value: 'crosses_below', label: 'Crosses Below' }
  ];

  const logics = [
    { value: 'AND', label: 'AND' },
    { value: 'OR', label: 'OR' }
  ];

  return (
    <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <Code className="w-6 h-6 text-purple-400" />
          <h2 className="text-2xl font-bold text-white">Strategy Editor</h2>
        </div>
        {!isEditing && (
          <button
            onClick={handleNewStrategy}
            className="flex items-center gap-2 px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors"
          >
            <Plus className="w-4 h-4" />
            New Strategy
          </button>
        )}
      </div>

      {error && (
        <div className="bg-red-500/10 border border-red-500/50 rounded-lg p-4 mb-6">
          <p className="text-red-400">{error}</p>
        </div>
      )}

      {success && (
        <div className="bg-green-500/10 border border-green-500/50 rounded-lg p-4 mb-6">
          <p className="text-green-400">{success}</p>
        </div>
      )}

      {/* Strategy List */}
      {!isEditing && (
        <div className="space-y-4">
          {customStrategies.length === 0 ? (
            <div className="text-center py-12">
              <Code className="w-12 h-12 text-slate-600 mx-auto mb-4" />
              <p className="text-slate-400">No custom strategies yet</p>
              <p className="text-sm text-slate-500 mt-2">
                Click "New Strategy" to create your first custom strategy
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-4">
              {customStrategies.map(strategy => (
                <div
                  key={strategy.id}
                  className="bg-slate-900/50 border border-slate-700 rounded-lg p-4 hover:border-slate-600 transition-colors"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-white mb-1">
                        {strategy.name}
                      </h3>
                      <p className="text-sm text-slate-400 mb-2">
                        {strategy.description}
                      </p>
                      <div className="flex items-center gap-2 text-xs text-slate-500">
                        <span>{strategy.conditions?.length || 0} conditions</span>
                        <span>•</span>
                        <span>Created {new Date(strategy.created_at).toLocaleDateString()}</span>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => handleEditStrategy(strategy)}
                        className="p-2 text-blue-400 hover:bg-blue-500/10 rounded-lg transition-colors"
                        title="Edit"
                      >
                        <Edit2 className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleDeleteStrategy(strategy.id)}
                        className="p-2 text-red-400 hover:bg-red-500/10 rounded-lg transition-colors"
                        title="Delete"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Strategy Editor */}
      {isEditing && (
        <div className="space-y-6">
          {/* Strategy Info */}
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Strategy Name
              </label>
              <input
                type="text"
                value={strategyName}
                onChange={(e) => setStrategyName(e.target.value)}
                placeholder="My Custom Strategy"
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-purple-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Description
              </label>
              <textarea
                value={strategyDescription}
                onChange={(e) => setStrategyDescription(e.target.value)}
                placeholder="Describe your strategy..."
                rows={3}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-purple-500 resize-none"
              />
            </div>
          </div>

          {/* Conditions */}
          <div>
            <div className="flex items-center justify-between mb-4">
              <label className="block text-sm font-medium text-slate-300">
                Conditions
              </label>
              <button
                onClick={handleAddCondition}
                className="flex items-center gap-1 px-3 py-1 bg-purple-600 hover:bg-purple-700 text-white text-sm rounded-lg transition-colors"
              >
                <Plus className="w-3 h-3" />
                Add Condition
              </button>
            </div>

            {conditions.length === 0 ? (
              <div className="text-center py-8 bg-slate-900/50 rounded-lg border border-slate-700">
                <p className="text-slate-400">No conditions added yet</p>
                <p className="text-sm text-slate-500 mt-1">
                  Click "Add Condition" to define your strategy logic
                </p>
              </div>
            ) : (
              <div className="space-y-3">
                {conditions.map((condition, index) => (
                  <div
                    key={condition.id}
                    className="bg-slate-900/50 border border-slate-700 rounded-lg p-4"
                  >
                    <div className="flex items-start gap-3">
                      <div className="flex-1 grid grid-cols-1 md:grid-cols-4 gap-3">
                        {/* Indicator */}
                        <div>
                          <label className="block text-xs text-slate-400 mb-1">
                            Indicator
                          </label>
                          <select
                            value={condition.indicator}
                            onChange={(e) =>
                              handleUpdateCondition(condition.id, 'indicator', e.target.value)
                            }
                            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-purple-500"
                          >
                            {indicators.map(ind => (
                              <option key={ind.value} value={ind.value}>
                                {ind.label}
                              </option>
                            ))}
                          </select>
                        </div>

                        {/* Operator */}
                        <div>
                          <label className="block text-xs text-slate-400 mb-1">
                            Operator
                          </label>
                          <select
                            value={condition.operator}
                            onChange={(e) =>
                              handleUpdateCondition(condition.id, 'operator', e.target.value)
                            }
                            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-purple-500"
                          >
                            {operators.map(op => (
                              <option key={op.value} value={op.value}>
                                {op.label}
                              </option>
                            ))}
                          </select>
                        </div>

                        {/* Value */}
                        <div>
                          <label className="block text-xs text-slate-400 mb-1">
                            Value
                          </label>
                          <input
                            type="number"
                            value={condition.value}
                            onChange={(e) =>
                              handleUpdateCondition(condition.id, 'value', parseFloat(e.target.value))
                            }
                            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-purple-500"
                          />
                        </div>

                        {/* Logic */}
                        {index < conditions.length - 1 && (
                          <div>
                            <label className="block text-xs text-slate-400 mb-1">
                              Logic
                            </label>
                            <select
                              value={condition.logic}
                              onChange={(e) =>
                                handleUpdateCondition(condition.id, 'logic', e.target.value)
                              }
                              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-purple-500"
                            >
                              {logics.map(logic => (
                                <option key={logic.value} value={logic.value}>
                                  {logic.label}
                                </option>
                              ))}
                            </select>
                          </div>
                        )}
                      </div>

                      {/* Remove Button */}
                      <button
                        onClick={() => handleRemoveCondition(condition.id)}
                        className="p-2 text-red-400 hover:bg-red-500/10 rounded-lg transition-colors"
                        title="Remove condition"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Action Buttons */}
          <div className="flex items-center gap-3 pt-4 border-t border-slate-700">
            <button
              onClick={handleSaveStrategy}
              className="flex items-center gap-2 px-6 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors"
            >
              <Save className="w-4 h-4" />
              {selectedStrategy ? 'Update Strategy' : 'Save Strategy'}
            </button>
            <button
              onClick={handleCancel}
              className="px-6 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-colors"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default StrategyEditor;
