import { useState } from 'react';
import { moduleStatuses, currentIndicators } from '../data/mockData';
import {
  Activity,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  Power,
  Database,
  Brain,
  BarChart3,
  MessageSquare,
  Bell,
  Server,
  RefreshCw,
  Cpu,
  Zap,
} from 'lucide-react';

const moduleIcons: Record<string, React.ComponentType<{ className?: string }>> = {
  data_collector: Database,
  analysis: Brain,
  paper_trading: BarChart3,
  xai: MessageSquare,
  notifications: Bell,
  api: Server,
};

const statusColors = {
  running: { bg: 'bg-success/10', border: 'border-success/30', text: 'text-success', dot: 'bg-success' },
  warning: { bg: 'bg-warning/10', border: 'border-warning/30', text: 'text-warning', dot: 'bg-warning' },
  error: { bg: 'bg-danger/10', border: 'border-danger/30', text: 'text-danger', dot: 'bg-danger' },
  stopped: { bg: 'bg-dark-border', border: 'border-dark-border', text: 'text-dark-muted', dot: 'bg-dark-muted' },
};

export default function SystemStatus() {
  const [refreshing, setRefreshing] = useState(false);

  const handleRefresh = () => {
    setRefreshing(true);
    setTimeout(() => setRefreshing(false), 1500);
  };

  const runningCount = moduleStatuses.filter(m => m.status === 'running').length;
  const warningCount = moduleStatuses.filter(m => m.status === 'warning').length;

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">System Status</h1>
          <p className="text-sm text-dark-muted mt-1">Monitor semua modul backend AI Trading Agent</p>
        </div>
        <button
          onClick={handleRefresh}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium border border-dark-border text-dark-muted hover:text-white hover:border-primary/30 transition-all ${
            refreshing ? 'animate-pulse' : ''
          }`}
        >
          <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
          Refresh
        </button>
      </div>

      {/* Overall Status */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-dark-card rounded-xl border border-dark-border p-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-success/10 flex items-center justify-center">
              <CheckCircle2 className="w-5 h-5 text-success" />
            </div>
            <div>
              <p className="text-2xl font-bold text-white">{runningCount}/{moduleStatuses.length}</p>
              <p className="text-xs text-dark-muted">Modules Running</p>
            </div>
          </div>
        </div>
        <div className="bg-dark-card rounded-xl border border-dark-border p-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-warning/10 flex items-center justify-center">
              <AlertTriangle className="w-5 h-5 text-warning" />
            </div>
            <div>
              <p className="text-2xl font-bold text-white">{warningCount}</p>
              <p className="text-xs text-dark-muted">Warnings</p>
            </div>
          </div>
        </div>
        <div className="bg-dark-card rounded-xl border border-dark-border p-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
              <Cpu className="w-5 h-5 text-primary" />
            </div>
            <div>
              <p className="text-2xl font-bold text-white">99.9%</p>
              <p className="text-xs text-dark-muted">System Uptime</p>
            </div>
          </div>
        </div>
      </div>

      {/* Module Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {moduleStatuses.map((mod) => {
          const Icon = moduleIcons[mod.module] || Activity;
          const colors = statusColors[mod.status];

          return (
            <div
              key={mod.module}
              className={`bg-dark-card rounded-xl border ${colors.border} p-5 hover:shadow-lg transition-all`}
            >
              {/* Header */}
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-3">
                  <div className={`w-10 h-10 rounded-lg ${colors.bg} flex items-center justify-center`}>
                    <Icon className={`w-5 h-5 ${colors.text}`} />
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-white">{mod.name}</h3>
                    <p className="text-xs text-dark-muted font-mono">{mod.module}</p>
                  </div>
                </div>
                <div className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full ${colors.bg} border ${colors.border}`}>
                  <div className={`w-1.5 h-1.5 rounded-full ${colors.dot} ${mod.status === 'running' ? 'animate-pulse' : ''}`} />
                  <span className={`text-xs font-medium capitalize ${colors.text}`}>{mod.status}</span>
                </div>
              </div>

              {/* Details */}
              <p className="text-xs text-dark-muted leading-relaxed mb-3">{mod.details}</p>

              {/* Metrics */}
              <div className="grid grid-cols-2 gap-2 mb-3">
                {mod.metrics.map((metric) => (
                  <div key={metric.label} className="bg-dark-bg/50 rounded-lg px-3 py-2 border border-dark-border/50">
                    <p className="text-xs text-dark-muted">{metric.label}</p>
                    <p className="text-xs font-semibold text-white mt-0.5">{metric.value}</p>
                  </div>
                ))}
              </div>

              {/* Footer */}
              <div className="flex items-center justify-between pt-3 border-t border-dark-border/50">
                <div className="flex items-center gap-1 text-xs text-dark-muted">
                  <Activity className="w-3 h-3" />
                  <span>Uptime: {mod.uptime}</span>
                </div>
                <span className="text-xs text-dark-muted">Last: {mod.lastAction}</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Current Indicators Analysis */}
      <div className="bg-dark-card rounded-xl border border-dark-border p-5">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
            <Zap className="w-5 h-5 text-primary" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-white">Live Indicator Analysis</h3>
            <p className="text-xs text-dark-muted">BTC/USDT • Real-time technical indicators</p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {currentIndicators.map((ind) => (
            <div
              key={ind.name}
              className={`rounded-lg p-3 border ${
                ind.signal === 'bullish' ? 'bg-success/5 border-success/20' :
                ind.signal === 'bearish' ? 'bg-danger/5 border-danger/20' :
                'bg-dark-bg border-dark-border/50'
              }`}
            >
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-medium text-dark-muted">{ind.name}</span>
                <span className={`text-xs font-bold ${
                  ind.signal === 'bullish' ? 'text-success' :
                  ind.signal === 'bearish' ? 'text-danger' :
                  'text-warning'
                }`}>
                  {ind.value}
                </span>
              </div>
              <p className="text-xs text-dark-text">{ind.description}</p>
            </div>
          ))}
        </div>

        {/* Summary */}
        <div className="mt-4 p-3 rounded-lg bg-primary/5 border border-primary/20">
          <div className="flex items-center gap-2 mb-1">
            <Brain className="w-4 h-4 text-primary" />
            <span className="text-xs font-semibold text-primary">AI Analysis Summary</span>
          </div>
          <p className="text-xs text-dark-text leading-relaxed">
            6 dari 8 indikator menunjukkan sinyal <span className="text-success font-semibold">bullish</span>. 
            MACD dan EMA menunjukkan momentum positif. Sentimen berita mendukung (+0.42). 
            Namun, RSI netral dan Bollinger Bands menunjukkan konsolidasi. 
            <span className="text-primary font-semibold"> Overall: Moderately Bullish (72% confidence)</span>
          </p>
        </div>
      </div>

      {/* Architecture Overview */}
      <div className="bg-dark-card rounded-xl border border-dark-border p-5">
        <h3 className="text-sm font-semibold text-white mb-4">🏗️ Arsitektur Sistem</h3>
        <div className="relative">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            {/* Data Collector */}
            <div className="flex flex-col items-center">
              <div className="w-16 h-16 rounded-xl bg-blue-500/10 border border-blue-500/30 flex items-center justify-center">
                <Database className="w-7 h-7 text-blue-400" />
              </div>
              <span className="text-xs font-medium text-white mt-2">Data Collector</span>
              <span className="text-xs text-dark-muted">Binance WS + RSS</span>
            </div>

            <div className="hidden sm:block text-dark-muted">→</div>
            <div className="sm:hidden text-dark-muted">↓</div>

            {/* Analysis */}
            <div className="flex flex-col items-center">
              <div className="w-16 h-16 rounded-xl bg-purple-500/10 border border-purple-500/30 flex items-center justify-center">
                <Brain className="w-7 h-7 text-purple-400" />
              </div>
              <span className="text-xs font-medium text-white mt-2">Analysis Engine</span>
              <span className="text-xs text-dark-muted">TA + FinBERT</span>
            </div>

            <div className="hidden sm:block text-dark-muted">→</div>
            <div className="sm:hidden text-dark-muted">↓</div>

            {/* Paper Trading */}
            <div className="flex flex-col items-center">
              <div className="w-16 h-16 rounded-xl bg-green-500/10 border border-green-500/30 flex items-center justify-center">
                <BarChart3 className="w-7 h-7 text-green-400" />
              </div>
              <span className="text-xs font-medium text-white mt-2">Paper Trading</span>
              <span className="text-xs text-dark-muted">Portfolio + Risk</span>
            </div>

            <div className="hidden sm:block text-dark-muted">→</div>
            <div className="sm:hidden text-dark-muted">↓</div>

            {/* XAI */}
            <div className="flex flex-col items-center">
              <div className="w-16 h-16 rounded-xl bg-orange-500/10 border border-orange-500/30 flex items-center justify-center">
                <MessageSquare className="w-7 h-7 text-orange-400" />
              </div>
              <span className="text-xs font-medium text-white mt-2">XAI Module</span>
              <span className="text-xs text-dark-muted">Explain + Chat</span>
            </div>
          </div>

          {/* API Layer */}
          <div className="mt-6 flex items-center justify-center">
            <div className="flex flex-col items-center">
              <div className="w-full h-12 rounded-xl bg-primary/10 border border-primary/30 flex items-center justify-center gap-3 px-6">
                <Server className="w-5 h-5 text-primary" />
                <span className="text-xs font-medium text-primary">FastAPI REST API</span>
                <span className="text-xs text-dark-muted">•</span>
                <span className="text-xs text-dark-muted">SQLite Database</span>
                <span className="text-xs text-dark-muted">•</span>
                <span className="text-xs text-dark-muted">Telegram Bot</span>
              </div>
              <span className="text-xs text-dark-muted mt-2">Infrastructure Layer → React Frontend</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
