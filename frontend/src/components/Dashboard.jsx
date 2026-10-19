import { useEffect, useState } from 'react'
import { TrendingUp, TrendingDown, DollarSign, Target, Activity } from 'lucide-react'
import axios from 'axios'

export default function Dashboard() {
  const [portfolio, setPortfolio] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchPortfolio()
  }, [])

  const fetchPortfolio = async () => {
    try {
      const response = await axios.get('/api/portfolio/summary')
      setPortfolio(response.data)
    } catch (error) {
      console.error('Error fetching portfolio:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="p-6 text-white">Loading...</div>
  }

  if (!portfolio) {
    return <div className="p-6 text-white">Failed to load portfolio</div>
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white">Dashboard</h1>
        <p className="text-dark-muted mt-1">Portfolio overview & performance</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Balance"
          value={`$${portfolio.balance.toLocaleString()}`}
          icon={DollarSign}
          color="blue"
        />
        <StatCard
          title="Total P&L"
          value={`$${portfolio.stats.total_pnl.toLocaleString()}`}
          icon={portfolio.stats.total_pnl >= 0 ? TrendingUp : TrendingDown}
          color={portfolio.stats.total_pnl >= 0 ? 'green' : 'red'}
        />
        <StatCard
          title="Win Rate"
          value={`${portfolio.stats.win_rate.toFixed(1)}%`}
          icon={Target}
          color="purple"
        />
        <StatCard
          title="Open Positions"
          value={portfolio.open_positions.toString()}
          icon={Activity}
          color="orange"
        />
      </div>

      {/* Performance Metrics */}
      <div className="bg-dark-card rounded-lg border border-dark-border p-6">
        <h2 className="text-xl font-bold text-white mb-4">Performance Metrics</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Metric label="Total Trades" value={portfolio.stats.total_trades} />
          <Metric label="Winning Trades" value={portfolio.stats.wins} />
          <Metric label="Losing Trades" value={portfolio.stats.losses} />
          <Metric label="Profit Factor" value={portfolio.stats.profit_factor.toFixed(2)} />
        </div>
      </div>

      {/* Open Positions */}
      {portfolio.positions && portfolio.positions.length > 0 && (
        <div className="bg-dark-card rounded-lg border border-dark-border p-6">
          <h2 className="text-xl font-bold text-white mb-4">Open Positions</h2>
          <div className="space-y-3">
            {portfolio.positions.map((pos, idx) => (
              <PositionCard key={idx} position={pos} />
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

function StatCard({ title, value, icon: Icon, color }) {
  const colors = {
    blue: 'bg-blue-500/10 text-blue-500',
    green: 'bg-green-500/10 text-green-500',
    red: 'bg-red-500/10 text-red-500',
    purple: 'bg-purple-500/10 text-purple-500',
    orange: 'bg-orange-500/10 text-orange-500',
  }

  return (
    <div className="bg-dark-card rounded-lg border border-dark-border p-6">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm text-dark-muted">{title}</span>
        <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${colors[color]}`}>
          <Icon className="w-5 h-5" />
        </div>
      </div>
      <p className="text-2xl font-bold text-white">{value}</p>
    </div>
  )
}

function Metric({ label, value }) {
  return (
    <div className="text-center">
      <p className="text-2xl font-bold text-white">{value}</p>
      <p className="text-sm text-dark-muted mt-1">{label}</p>
    </div>
  )
}

function PositionCard({ position }) {
  const pnl = position.pnl || 0
  const isProfit = pnl >= 0

  return (
    <div className="bg-dark-bg rounded-lg border border-dark-border p-4">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <span className="text-lg font-bold text-white">{position.symbol}</span>
          <span className={`px-2 py-1 rounded text-xs font-medium ${
            position.side === 'long' ? 'bg-green-500/10 text-green-500' : 'bg-red-500/10 text-red-500'
          }`}>
            {position.side.toUpperCase()}
          </span>
        </div>
        <span className={`text-lg font-bold ${isProfit ? 'text-green-500' : 'text-red-500'}`}>
          {isProfit ? '+' : ''}${pnl.toFixed(2)}
        </span>
      </div>
      <div className="grid grid-cols-3 gap-4 text-sm">
        <div>
          <p className="text-dark-muted">Entry</p>
          <p className="text-white font-medium">${position.entry_price.toFixed(2)}</p>
        </div>
        <div>
          <p className="text-dark-muted">Stop Loss</p>
          <p className="text-red-500 font-medium">${position.stop_loss.toFixed(2)}</p>
        </div>
        <div>
          <p className="text-dark-muted">Take Profit</p>
          <p className="text-green-500 font-medium">${position.take_profit.toFixed(2)}</p>
        </div>
      </div>
    </div>
  )
}
