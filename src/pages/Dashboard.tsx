import {
  TrendingUp,
  TrendingDown,
  DollarSign,
  Target,
  BarChart3,
  Shield,
  Activity,
  ArrowUpRight,
  ArrowDownRight,
  Clock,
  History,
} from 'lucide-react';
import {
  AreaChart, Area, BarChart, Bar,
  XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid,
} from 'recharts';
import {
  portfolioStats, positions, recentSignals,
  equityCurveData, performanceBySymbol, tradeHistory, dailyPnL,
} from '../data/mockData';

export default function Dashboard() {
  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">Dashboard Overview</h1>
          <p className="text-sm text-dark-muted mt-1">Portfolio performance & bot activity</p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-dark-muted">Last updated:</span>
          <span className="text-xs text-white font-medium">2 min ago</span>
          <Activity className="w-3 h-3 text-success animate-pulse" />
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Balance"
          value={`$${portfolioStats.totalBalance.toLocaleString()}`}
          change="+12.48%"
          positive={true}
          icon={DollarSign}
          subtitle="Virtual Portfolio"
        />
        <StatCard
          title="Total P&L"
          value={`+$${portfolioStats.totalPnL.toLocaleString()}`}
          change="+12.48%"
          positive={true}
          icon={TrendingUp}
          subtitle="Since inception"
        />
        <StatCard
          title="Win Rate"
          value={`${portfolioStats.winRate}%`}
          change={`${portfolioStats.winningTrades}W / ${portfolioStats.losingTrades}L`}
          positive={true}
          icon={Target}
          subtitle={`${portfolioStats.totalTrades} total trades`}
        />
        <StatCard
          title="Max Drawdown"
          value={`${portfolioStats.maxDrawdown}%`}
          change={`Sharpe: ${portfolioStats.sharpeRatio}`}
          positive={true}
          icon={Shield}
          subtitle="Risk controlled"
        />
      </div>

      {/* Equity Curve & Daily PnL */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Equity Curve */}
        <div className="lg:col-span-2 bg-dark-card rounded-xl border border-dark-border p-4">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-white">Equity Curve</h3>
            <div className="flex items-center gap-1 text-xs text-success">
              <ArrowUpRight className="w-3 h-3" />
              <span>+12.48% total return</span>
            </div>
          </div>
          <div className="h-48">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={equityCurveData}>
                <defs>
                  <linearGradient id="equityGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1a1d29" />
                <XAxis dataKey="date" tick={{ fontSize: 10, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 10, fill: '#94a3b8' }} axisLine={false} tickLine={false} domain={['dataMin - 100', 'dataMax + 100']} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1a1d29', border: '1px solid #2a2d3a', borderRadius: '8px' }}
                  labelStyle={{ color: '#94a3b8', fontSize: 11 }}
                  itemStyle={{ color: '#6366f1', fontSize: 11 }}
                />
                <Area type="monotone" dataKey="balance" stroke="#6366f1" strokeWidth={2} fill="url(#equityGradient)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Daily PnL */}
        <div className="bg-dark-card rounded-xl border border-dark-border p-4">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-white">Daily P&L</h3>
            <BarChart3 className="w-4 h-4 text-dark-muted" />
          </div>
          <div className="h-48">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={dailyPnL}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1a1d29" />
                <XAxis dataKey="date" tick={{ fontSize: 9, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 9, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1a1d29', border: '1px solid #2a2d3a', borderRadius: '8px' }}
                  labelStyle={{ color: '#94a3b8', fontSize: 11 }}
                  formatter={(value: number) => [`$${value}`, 'P&L']}
                />
                <Bar
                  dataKey="pnl"
                  fill="#6366f1"
                  radius={[2, 2, 0, 0]}
                  shape={(props: any) => {
                    const { x, y, width, height, payload } = props;
                    const color = payload.pnl >= 0 ? '#10b981' : '#ef4444';
                    return <rect x={x} y={y} width={width} height={height} fill={color} rx={2} />;
                  }}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Active Positions & Performance by Symbol */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Active Positions */}
        <div className="bg-dark-card rounded-xl border border-dark-border p-4">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-white">Active Positions</h3>
            <span className="text-xs text-dark-muted">{positions.length} open</span>
          </div>
          <div className="space-y-3">
            {positions.map((pos) => (
              <div key={pos.symbol} className="bg-dark-bg/50 rounded-lg p-3 border border-dark-border">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-semibold text-white">{pos.symbol}</span>
                    <span className={`text-xs px-1.5 py-0.5 rounded ${
                      pos.side === 'LONG' ? 'bg-success/10 text-success' : 'bg-danger/10 text-danger'
                    }`}>
                      {pos.side}
                    </span>
                  </div>
                  <div className={`flex items-center gap-1 text-xs font-semibold ${
                    pos.pnl >= 0 ? 'text-success' : 'text-danger'
                  }`}>
                    {pos.pnl >= 0 ? <ArrowUpRight className="w-3 h-3" /> : <ArrowDownRight className="w-3 h-3" />}
                    {pos.pnl >= 0 ? '+' : ''}{pos.pnlPercent.toFixed(2)}%
                  </div>
                </div>
                <div className="grid grid-cols-3 gap-2 text-xs">
                  <div>
                    <span className="text-dark-muted">Entry</span>
                    <p className="text-white font-medium">${pos.entryPrice.toLocaleString()}</p>
                  </div>
                  <div>
                    <span className="text-dark-muted">Current</span>
                    <p className="text-white font-medium">${pos.currentPrice.toLocaleString()}</p>
                  </div>
                  <div>
                    <span className="text-dark-muted">P&L</span>
                    <p className={`font-medium ${pos.pnl >= 0 ? 'text-success' : 'text-danger'}`}>
                      {pos.pnl >= 0 ? '+' : ''}${pos.pnl.toFixed(2)}
                    </p>
                  </div>
                </div>
                <div className="mt-2 pt-2 border-t border-dark-border/50">
                  <div className="flex justify-between text-xs">
                    <span className="text-danger">SL: ${pos.stopLoss.toLocaleString()}</span>
                    <span className="text-success">TP: ${pos.takeProfit.toLocaleString()}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Performance by Symbol */}
        <div className="bg-dark-card rounded-xl border border-dark-border p-4">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-white">Performance by Symbol</h3>
            <Target className="w-4 h-4 text-dark-muted" />
          </div>
          <div className="space-y-3">
            {performanceBySymbol.map((item) => (
              <div key={item.symbol} className="flex items-center justify-between p-2 rounded-lg bg-dark-bg/30">
                <div className="flex items-center gap-3">
                  <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${
                    item.pnl >= 0 ? 'bg-success/10' : 'bg-danger/10'
                  }`}>
                    <span className="text-xs font-bold text-white">{item.symbol.split('/')[0]}</span>
                  </div>
                  <div>
                    <span className="text-xs font-medium text-white">{item.symbol}</span>
                    <p className="text-xs text-dark-muted">{item.trades} trades • {item.winRate}% WR</p>
                  </div>
                </div>
                <div className="text-right">
                  <span className={`text-sm font-bold ${item.pnl >= 0 ? 'text-success' : 'text-danger'}`}>
                    {item.pnl >= 0 ? '+' : ''}${item.pnl}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recent Signals & Trade History */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Recent Signals */}
        <div className="bg-dark-card rounded-xl border border-dark-border p-4">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-white">Recent Bot Signals</h3>
            <Activity className="w-4 h-4 text-dark-muted" />
          </div>
          <div className="space-y-2">
            {recentSignals.slice(0, 5).map((signal) => (
              <div key={signal.id} className="flex items-center gap-3 p-2.5 rounded-lg bg-dark-bg/50 border border-dark-border/50 hover:border-dark-border transition-colors">
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${
                  signal.signal === 'BUY' ? 'bg-success/10' : signal.signal === 'SELL' ? 'bg-danger/10' : 'bg-warning/10'
                }`}>
                  {signal.signal === 'BUY' ? (
                    <TrendingUp className="w-4 h-4 text-success" />
                  ) : signal.signal === 'SELL' ? (
                    <TrendingDown className="w-4 h-4 text-danger" />
                  ) : (
                    <Activity className="w-4 h-4 text-warning" />
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-semibold text-white">{signal.symbol}</span>
                    <span className={`text-xs font-bold ${
                      signal.signal === 'BUY' ? 'text-success' : signal.signal === 'SELL' ? 'text-danger' : 'text-warning'
                    }`}>
                      {signal.signal}
                    </span>
                    <span className="text-xs text-dark-muted">{signal.timeframe}</span>
                  </div>
                  <div className="flex items-center gap-2 mt-0.5">
                    <div className="flex-1 h-1 bg-dark-border rounded-full overflow-hidden">
                      <div
                        className={`h-full rounded-full ${
                          signal.confidence >= 70 ? 'bg-success' : signal.confidence >= 50 ? 'bg-warning' : 'bg-danger'
                        }`}
                        style={{ width: `${signal.confidence}%` }}
                      />
                    </div>
                    <span className="text-xs text-dark-muted">{signal.confidence}%</span>
                  </div>
                </div>
                {signal.executed && signal.pnl !== undefined && (
                  <span className={`text-xs font-semibold ${signal.pnl >= 0 ? 'text-success' : 'text-danger'}`}>
                    {signal.pnl >= 0 ? '+' : ''}${signal.pnl.toFixed(0)}
                  </span>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Recent Trades */}
        <div className="bg-dark-card rounded-xl border border-dark-border p-4">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-white">Recent Trades</h3>
            <History className="w-4 h-4 text-dark-muted" />
          </div>
          <div className="space-y-2">
            {tradeHistory.slice(0, 6).map((trade) => (
              <div key={trade.id} className="flex items-center gap-3 p-2 rounded-lg bg-dark-bg/50 border border-dark-border/50">
                <div className={`w-7 h-7 rounded flex items-center justify-center ${
                  trade.side === 'BUY' ? 'bg-success/10' : 'bg-danger/10'
                }`}>
                  <span className={`text-xs font-bold ${
                    trade.side === 'BUY' ? 'text-success' : 'text-danger'
                  }`}>
                    {trade.side === 'BUY' ? 'B' : 'S'}
                  </span>
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-semibold text-white">{trade.symbol}</span>
                    <span className="text-xs text-dark-muted">{trade.type}</span>
                  </div>
                  <div className="flex items-center gap-2 text-xs text-dark-muted">
                    <Clock className="w-3 h-3" />
                    <span>{trade.timestamp.split(' ')[1]}</span>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-xs font-medium text-white">${trade.total.toFixed(2)}</p>
                  <p className="text-xs text-dark-muted">{trade.quantity} @ ${trade.price.toLocaleString()}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, change, positive, icon: Icon, subtitle }: {
  title: string;
  value: string;
  change: string;
  positive: boolean;
  icon: React.ComponentType<{ className?: string }>;
  subtitle: string;
}) {
  return (
    <div className="bg-dark-card rounded-xl border border-dark-border p-4 hover:border-primary/30 transition-colors">
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs text-dark-muted font-medium">{title}</span>
        <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center">
          <Icon className="w-4 h-4 text-primary" />
        </div>
      </div>
      <p className="text-xl font-bold text-white">{value}</p>
      <div className="flex items-center gap-2 mt-1">
        <span className={`text-xs font-medium ${positive ? 'text-success' : 'text-danger'}`}>
          {change}
        </span>
        <span className="text-xs text-dark-muted">{subtitle}</span>
      </div>
    </div>
  );
}
