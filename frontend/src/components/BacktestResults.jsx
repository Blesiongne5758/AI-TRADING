import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { TrendingUp, TrendingDown, DollarSign, Percent, Target, Award } from 'lucide-react';

const BacktestResults = ({ result }) => {
  if (!result) {
    return (
      <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
        <div className="text-center py-12">
          <TrendingUp className="w-12 h-12 text-slate-600 mx-auto mb-4" />
          <p className="text-slate-400">No backtest results yet</p>
          <p className="text-sm text-slate-500 mt-2">
            Run a backtest to see results here
          </p>
        </div>
      </div>
    );
  }

  const {
    status,
    symbol,
    timeframe,
    strategy,
    start_date,
    end_date,
    initial_balance,
    final_balance,
    total_return,
    total_return_pct,
    max_drawdown,
    max_drawdown_pct,
    sharpe_ratio,
    win_rate,
    total_trades,
    winning_trades,
    losing_trades,
    avg_win,
    avg_loss,
    profit_factor,
    equity_curve,
    trades
  } = result;

  const isProfitable = total_return > 0;

  // Format currency
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(value);
  };

  // Format percentage
  const formatPercent = (value) => {
    return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`;
  };

  // Prepare equity curve data
  const equityData = equity_curve?.map((point, index) => ({
    index,
    balance: point.balance,
    drawdown: point.drawdown || 0
  })) || [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold text-white mb-1">
              Backtest Results
            </h2>
            <p className="text-slate-400">
              {symbol} • {timeframe} • {strategy}
            </p>
          </div>
          <div className={`px-4 py-2 rounded-lg ${
            status === 'completed' ? 'bg-green-500/10 text-green-400' : 'bg-yellow-500/10 text-yellow-400'
          }`}>
            {status === 'completed' ? '✓ Completed' : '⏳ Running'}
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <p className="text-slate-400">Period</p>
            <p className="text-white font-medium">
              {new Date(start_date).toLocaleDateString()} - {new Date(end_date).toLocaleDateString()}
            </p>
          </div>
          <div>
            <p className="text-slate-400">Initial Balance</p>
            <p className="text-white font-medium">{formatCurrency(initial_balance)}</p>
          </div>
          <div>
            <p className="text-slate-400">Final Balance</p>
            <p className={`font-medium ${isProfitable ? 'text-green-400' : 'text-red-400'}`}>
              {formatCurrency(final_balance)}
            </p>
          </div>
          <div>
            <p className="text-slate-400">Total Return</p>
            <p className={`font-medium ${isProfitable ? 'text-green-400' : 'text-red-400'}`}>
              {formatPercent(total_return_pct)}
            </p>
          </div>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Return Metrics */}
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <div className="flex items-center gap-2 mb-4">
            <DollarSign className="w-5 h-5 text-blue-400" />
            <h3 className="text-lg font-semibold text-white">Return</h3>
          </div>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-slate-400">Total Return</span>
              <span className={`font-medium ${isProfitable ? 'text-green-400' : 'text-red-400'}`}>
                {formatPercent(total_return_pct)}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Total Return ($)</span>
              <span className={`font-medium ${isProfitable ? 'text-green-400' : 'text-red-400'}`}>
                {formatCurrency(total_return)}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Sharpe Ratio</span>
              <span className="text-white font-medium">{sharpe_ratio.toFixed(2)}</span>
            </div>
          </div>
        </div>

        {/* Risk Metrics */}
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <div className="flex items-center gap-2 mb-4">
            <Target className="w-5 h-5 text-orange-400" />
            <h3 className="text-lg font-semibold text-white">Risk</h3>
          </div>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-slate-400">Max Drawdown</span>
              <span className="text-red-400 font-medium">
                {formatPercent(max_drawdown_pct)}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Max Drawdown ($)</span>
              <span className="text-red-400 font-medium">
                {formatCurrency(max_drawdown)}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Profit Factor</span>
              <span className="text-white font-medium">{profit_factor.toFixed(2)}</span>
            </div>
          </div>
        </div>

        {/* Trade Metrics */}
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <div className="flex items-center gap-2 mb-4">
            <Award className="w-5 h-5 text-purple-400" />
            <h3 className="text-lg font-semibold text-white">Trades</h3>
          </div>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-slate-400">Total Trades</span>
              <span className="text-white font-medium">{total_trades}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Win Rate</span>
              <span className="text-white font-medium">{win_rate.toFixed(1)}%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Winning / Losing</span>
              <span className="text-white font-medium">
                <span className="text-green-400">{winning_trades}</span>
                {' / '}
                <span className="text-red-400">{losing_trades}</span>
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Equity Curve */}
      {equityData.length > 0 && (
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <h3 className="text-lg font-semibold text-white mb-4">Equity Curve</h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={equityData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="index" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1e293b',
                  border: '1px solid #334155',
                  borderRadius: '8px'
                }}
                labelStyle={{ color: '#94a3b8' }}
              />
              <Area
                type="monotone"
                dataKey="balance"
                stroke="#3b82f6"
                fill="#3b82f6"
                fillOpacity={0.1}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Drawdown Chart */}
      {equityData.length > 0 && (
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <h3 className="text-lg font-semibold text-white mb-4">Drawdown</h3>
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={equityData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="index" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1e293b',
                  border: '1px solid #334155',
                  borderRadius: '8px'
                }}
                labelStyle={{ color: '#94a3b8' }}
              />
              <Area
                type="monotone"
                dataKey="drawdown"
                stroke="#ef4444"
                fill="#ef4444"
                fillOpacity={0.2}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Trade List */}
      {trades && trades.length > 0 && (
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <h3 className="text-lg font-semibold text-white mb-4">
            Trade History ({trades.length} trades)
          </h3>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-slate-700">
                  <th className="text-left py-3 px-4 text-sm font-medium text-slate-400">#</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-slate-400">Type</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-slate-400">Entry</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-slate-400">Exit</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-slate-400">P&L</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-slate-400">P&L %</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-slate-400">Duration</th>
                </tr>
              </thead>
              <tbody>
                {trades.slice(0, 20).map((trade, index) => {
                  const isWin = trade.pnl > 0;
                  return (
                    <tr key={index} className="border-b border-slate-700/50 hover:bg-slate-700/30">
                      <td className="py-3 px-4 text-sm text-slate-300">{index + 1}</td>
                      <td className="py-3 px-4">
                        <span className={`inline-flex items-center gap-1 px-2 py-1 rounded text-xs font-medium ${
                          trade.type === 'BUY'
                            ? 'bg-green-500/10 text-green-400'
                            : 'bg-red-500/10 text-red-400'
                        }`}>
                          {trade.type === 'BUY' ? (
                            <TrendingUp className="w-3 h-3" />
                          ) : (
                            <TrendingDown className="w-3 h-3" />
                          )}
                          {trade.type}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-sm text-slate-300">
                        {formatCurrency(trade.entry_price)}
                      </td>
                      <td className="py-3 px-4 text-sm text-slate-300">
                        {formatCurrency(trade.exit_price)}
                      </td>
                      <td className={`py-3 px-4 text-sm font-medium ${
                        isWin ? 'text-green-400' : 'text-red-400'
                      }`}>
                        {formatCurrency(trade.pnl)}
                      </td>
                      <td className={`py-3 px-4 text-sm font-medium ${
                        isWin ? 'text-green-400' : 'text-red-400'
                      }`}>
                        {formatPercent(trade.pnl_pct)}
                      </td>
                      <td className="py-3 px-4 text-sm text-slate-400">
                        {trade.duration || '-'}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
          {trades.length > 20 && (
            <p className="text-sm text-slate-400 mt-4 text-center">
              Showing first 20 of {trades.length} trades
            </p>
          )}
        </div>
      )}

      {/* Average Win/Loss */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp className="w-5 h-5 text-green-400" />
            <h3 className="text-lg font-semibold text-white">Average Win</h3>
          </div>
          <p className="text-3xl font-bold text-green-400">
            {formatCurrency(avg_win)}
          </p>
        </div>

        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <div className="flex items-center gap-2 mb-4">
            <TrendingDown className="w-5 h-5 text-red-400" />
            <h3 className="text-lg font-semibold text-white">Average Loss</h3>
          </div>
          <p className="text-3xl font-bold text-red-400">
            {formatCurrency(avg_loss)}
          </p>
        </div>
      </div>
    </div>
  );
};

export default BacktestResults;
