import { useState, useEffect } from 'react';
import axios from 'axios';
import { TrendingUp, TrendingDown, DollarSign, Activity, Target } from 'lucide-react';

export default function Dashboard() {
  const [portfolio, setPortfolio] = useState(null);
  const [positions, setPositions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 10000); // Update setiap 10 detik
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const [portfolioRes, positionsRes] = await Promise.all([
        axios.get('http://localhost:8000/api/portfolio/summary'),
        axios.get('http://localhost:8000/api/portfolio/positions'),
      ]);
      
      setPortfolio(portfolioRes.data);
      setPositions(positionsRes.data.positions);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-white">Loading...</div>
      </div>
    );
  }

  const summary = portfolio?.summary || {};
  const stats = portfolio?.stats || {};

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-white mb-8">Dashboard</h1>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Total Balance"
          value={`$${summary.total_balance?.toFixed(2) || '0.00'}`}
          change={summary.total_return_percent}
          icon={DollarSign}
          color="blue"
        />
        <StatCard
          title="Unrealized PnL"
          value={`$${summary.unrealized_pnl?.toFixed(2) || '0.00'}`}
          isProfit={summary.unrealized_pnl > 0}
          icon={TrendingUp}
          color="green"
        />
        <StatCard
          title="Realized PnL"
          value={`$${summary.realized_pnl?.toFixed(2) || '0.00'}`}
          isProfit={summary.realized_pnl > 0}
          icon={Activity}
          color="purple"
        />
        <StatCard
          title="Win Rate"
          value={`${stats.win_rate?.toFixed(1) || '0.0'}%`}
          subtitle={`${stats.wins || 0}W / ${stats.losses || 0}L`}
          icon={Target}
          color="orange"
        />
      </div>

      {/* Open Positions */}
      <div className="bg-slate-800 rounded-lg p-6">
        <h2 className="text-xl font-bold text-white mb-4">Open Positions</h2>
        
        {positions.length === 0 ? (
          <p className="text-slate-400">No open positions</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="text-left text-slate-400 border-b border-slate-700">
                  <th className="pb-3">Symbol</th>
                  <th className="pb-3">Side</th>
                  <th className="pb-3">Entry</th>
                  <th className="pb-3">Current</th>
                  <th className="pb-3">PnL</th>
                  <th className="pb-3">SL / TP</th>
                </tr>
              </thead>
              <tbody>
                {positions.map((pos) => (
                  <tr key={pos.id} className="border-b border-slate-700">
                    <td className="py-4 text-white font-medium">{pos.symbol}</td>
                    <td className="py-4">
                      <span className={`px-2 py-1 rounded text-xs font-medium ${
                        pos.side === 'long' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                      }`}>
                        {pos.side.toUpperCase()}
                      </span>
                    </td>
                    <td className="py-4 text-slate-300">${pos.entry_price.toFixed(2)}</td>
                    <td className="py-4 text-white">${pos.current_price.toFixed(2)}</td>
                    <td className="py-4">
                      <span className={pos.pnl > 0 ? 'text-green-400' : 'text-red-400'}>
                        ${pos.pnl.toFixed(2)} ({pos.pnl_percent.toFixed(2)}%)
                      </span>
                    </td>
                    <td className="py-4 text-slate-400 text-sm">
                      <div>SL: ${pos.stop_loss.toFixed(2)}</div>
                      <div>TP: ${pos.take_profit.toFixed(2)}</div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

function StatCard({ title, value, change, isProfit, subtitle, icon: Icon, color }) {
  const colorClasses = {
    blue: 'bg-blue-500/10 text-blue-400',
    green: 'bg-green-500/10 text-green-400',
    purple: 'bg-purple-500/10 text-purple-400',
    orange: 'bg-orange-500/10 text-orange-400',
  };

  return (
    <div className="bg-slate-800 rounded-lg p-6">
      <div className="flex items-center justify-between mb-4">
        <div className={`p-3 rounded-lg ${colorClasses[color]}`}>
          <Icon className="w-6 h-6" />
        </div>
      </div>
      <h3 className="text-slate-400 text-sm mb-2">{title}</h3>
      <p className="text-2xl font-bold text-white">{value}</p>
      {change !== undefined && (
        <p className={`text-sm mt-2 ${change >= 0 ? 'text-green-400' : 'text-red-400'}`}>
          {change >= 0 ? '+' : ''}{change.toFixed(2)}%
        </p>
      )}
      {subtitle && <p className="text-sm text-slate-400 mt-2">{subtitle}</p>}
    </div>
  );
}
