import { useState } from 'react';
import { recentSignals, newsItems, tradeHistory } from '../data/mockData';
import {
  TrendingUp,
  TrendingDown,
  Activity,
  CheckCircle2,
  XCircle,
  Clock,
  Filter,
  Search,
  Newspaper,
  History,
  ArrowUpRight,
  ArrowDownRight,
} from 'lucide-react';

export default function LogPage() {
  const [filter, setFilter] = useState<'ALL' | 'BUY' | 'SELL' | 'HOLD'>('ALL');
  const [searchQuery, setSearchQuery] = useState('');
  const [activeTab, setActiveTab] = useState<'signals' | 'trades' | 'news'>('signals');

  const filteredSignals = recentSignals.filter((s) => {
    if (filter !== 'ALL' && s.signal !== filter) return false;
    if (searchQuery && !s.symbol.toLowerCase().includes(searchQuery.toLowerCase())) return false;
    return true;
  });

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">Decision Log</h1>
          <p className="text-sm text-dark-muted mt-1">Complete history of bot decisions, trades, and news sentiment</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-1 bg-dark-card rounded-lg border border-dark-border p-1 w-fit">
        <button
          onClick={() => setActiveTab('signals')}
          className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
            activeTab === 'signals' ? 'bg-primary text-white' : 'text-dark-muted hover:text-white'
          }`}
        >
          <Activity className="w-4 h-4" />
          Trading Signals
        </button>
        <button
          onClick={() => setActiveTab('trades')}
          className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
            activeTab === 'trades' ? 'bg-primary text-white' : 'text-dark-muted hover:text-white'
          }`}
        >
          <History className="w-4 h-4" />
          Trade History
        </button>
        <button
          onClick={() => setActiveTab('news')}
          className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
            activeTab === 'news' ? 'bg-primary text-white' : 'text-dark-muted hover:text-white'
          }`}
        >
          <Newspaper className="w-4 h-4" />
          News Sentiment
        </button>
      </div>

      {activeTab === 'signals' && (
        <>
          {/* Filters */}
          <div className="flex flex-wrap items-center gap-3">
            <div className="relative flex-1 max-w-xs">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-dark-muted" />
              <input
                type="text"
                placeholder="Search symbol..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-9 pr-4 py-2 bg-dark-card border border-dark-border rounded-lg text-sm text-white placeholder:text-dark-muted focus:outline-none focus:border-primary/50"
              />
            </div>
            <div className="flex items-center gap-1 bg-dark-card rounded-lg border border-dark-border p-1">
              {(['ALL', 'BUY', 'SELL', 'HOLD'] as const).map((f) => (
                <button
                  key={f}
                  onClick={() => setFilter(f)}
                  className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                    filter === f ? 'bg-primary text-white' : 'text-dark-muted hover:text-white'
                  }`}
                >
                  {f}
                </button>
              ))}
            </div>
            <div className="flex items-center gap-1 text-xs text-dark-muted">
              <Filter className="w-3 h-3" />
              <span>{filteredSignals.length} results</span>
            </div>
          </div>

          {/* Signal Cards */}
          <div className="space-y-3">
            {filteredSignals.map((signal) => (
              <div
                key={signal.id}
                className="bg-dark-card rounded-xl border border-dark-border p-4 hover:border-dark-border/80 transition-colors"
              >
                <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
                  <div className="flex items-start gap-3">
                    <div className={`w-10 h-10 rounded-lg flex items-center justify-center shrink-0 ${
                      signal.signal === 'BUY' ? 'bg-success/10' : signal.signal === 'SELL' ? 'bg-danger/10' : 'bg-warning/10'
                    }`}>
                      {signal.signal === 'BUY' ? (
                        <TrendingUp className="w-5 h-5 text-success" />
                      ) : signal.signal === 'SELL' ? (
                        <TrendingDown className="w-5 h-5 text-danger" />
                      ) : (
                        <Activity className="w-5 h-5 text-warning" />
                      )}
                    </div>
                    <div>
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className="text-sm font-bold text-white">{signal.symbol}</span>
                        <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                          signal.signal === 'BUY' ? 'bg-success/10 text-success' : signal.signal === 'SELL' ? 'bg-danger/10 text-danger' : 'bg-warning/10 text-warning'
                        }`}>
                          {signal.signal}
                        </span>
                        <span className="text-xs text-dark-muted bg-dark-bg px-2 py-0.5 rounded">{signal.timeframe}</span>
                        <span className="text-xs text-dark-muted">@ ${signal.price.toLocaleString()}</span>
                      </div>
                      <div className="flex items-center gap-3 mt-1">
                        <div className="flex items-center gap-1 text-xs text-dark-muted">
                          <Clock className="w-3 h-3" />
                          {signal.timestamp}
                        </div>
                        <div className="flex items-center gap-1">
                          {signal.executed ? (
                            <span className="flex items-center gap-1 text-xs text-success">
                              <CheckCircle2 className="w-3 h-3" /> Executed
                            </span>
                          ) : (
                            <span className="flex items-center gap-1 text-xs text-dark-muted">
                              <XCircle className="w-3 h-3" /> Not Executed
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-4 sm:text-right">
                    <div>
                      <p className="text-xs text-dark-muted">Confidence</p>
                      <div className="flex items-center gap-2">
                        <div className="w-20 h-1.5 bg-dark-border rounded-full overflow-hidden">
                          <div
                            className={`h-full rounded-full ${
                              signal.confidence >= 70 ? 'bg-success' : signal.confidence >= 50 ? 'bg-warning' : 'bg-danger'
                            }`}
                            style={{ width: `${signal.confidence}%` }}
                          />
                        </div>
                        <span className="text-sm font-bold text-white">{signal.confidence}%</span>
                      </div>
                    </div>
                    {signal.pnl !== undefined && (
                      <div>
                        <p className="text-xs text-dark-muted">P&L</p>
                        <span className={`text-sm font-bold ${signal.pnl >= 0 ? 'text-success' : 'text-danger'}`}>
                          {signal.pnl >= 0 ? '+' : ''}${signal.pnl.toFixed(2)}
                        </span>
                      </div>
                    )}
                  </div>
                </div>

                {/* Reasons */}
                <div className="mt-3 pt-3 border-t border-dark-border/50">
                  <p className="text-xs font-medium text-dark-muted mb-2">REASONS:</p>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-1.5">
                    {signal.reasons.map((reason, idx) => (
                      <div key={idx} className="flex items-start gap-2">
                        <span className="text-xs text-primary font-bold mt-0.5 shrink-0">{idx + 1}.</span>
                        <p className="text-xs text-dark-text leading-relaxed">{reason}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </>
      )}

      {activeTab === 'trades' && (
        <div className="bg-dark-card rounded-xl border border-dark-border overflow-hidden">
          <div className="px-4 py-3 border-b border-dark-border">
            <h3 className="text-sm font-semibold text-white">All Trades ({tradeHistory.length})</h3>
          </div>
          {/* Table Header */}
          <div className="hidden sm:grid grid-cols-7 gap-2 px-4 py-2 border-b border-dark-border/50 text-xs text-dark-muted font-medium">
            <span>Time</span>
            <span>Symbol</span>
            <span>Side</span>
            <span>Price</span>
            <span>Qty</span>
            <span>Total</span>
            <span>Status</span>
          </div>
          {/* Table Body */}
          <div className="divide-y divide-dark-border/50">
            {tradeHistory.map((trade) => (
              <div key={trade.id} className="grid grid-cols-2 sm:grid-cols-7 gap-2 px-4 py-3 hover:bg-white/[0.02] transition-colors items-center">
                <div className="flex items-center gap-1 text-xs text-dark-muted">
                  <Clock className="w-3 h-3" />
                  <span className="sm:hidden mr-1">Time:</span>
                  {trade.timestamp.split(' ')[1]}
                </div>
                <span className="text-xs font-semibold text-white">{trade.symbol}</span>
                <div className="flex items-center gap-1">
                  {trade.side === 'BUY' ? (
                    <ArrowUpRight className="w-3 h-3 text-success" />
                  ) : (
                    <ArrowDownRight className="w-3 h-3 text-danger" />
                  )}
                  <span className={`text-xs font-bold ${trade.side === 'BUY' ? 'text-success' : 'text-danger'}`}>
                    {trade.side}
                  </span>
                </div>
                <span className="text-xs text-white">${trade.price.toLocaleString()}</span>
                <span className="text-xs text-dark-muted">{trade.quantity}</span>
                <span className="text-xs text-white font-medium">${trade.total.toFixed(2)}</span>
                <span className="flex items-center gap-1 text-xs text-success">
                  <CheckCircle2 className="w-3 h-3" />
                  {trade.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'news' && (
        <div className="space-y-3">
          {newsItems.map((news) => (
            <div key={news.id} className="bg-dark-card rounded-xl border border-dark-border p-4">
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs text-primary font-medium">{news.source}</span>
                    <span className="text-xs text-dark-muted">•</span>
                    <span className="text-xs text-dark-muted">{news.timestamp}</span>
                  </div>
                  <h4 className="text-sm font-semibold text-white mb-1">{news.title}</h4>
                  <p className="text-xs text-dark-muted leading-relaxed">{news.summary}</p>
                </div>
                <div className={`shrink-0 px-3 py-1.5 rounded-lg text-sm font-bold ${
                  news.sentiment > 0.3 ? 'bg-success/10 text-success' :
                  news.sentiment < -0.3 ? 'bg-danger/10 text-danger' :
                  'bg-warning/10 text-warning'
                }`}>
                  {news.sentiment > 0 ? '+' : ''}{news.sentiment.toFixed(2)}
                </div>
              </div>
              <div className="mt-2 flex items-center gap-2">
                <span className="text-xs text-dark-muted">Sentiment:</span>
                <div className="flex-1 h-1.5 bg-dark-border rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full ${
                      news.sentiment > 0.3 ? 'bg-success' :
                      news.sentiment < -0.3 ? 'bg-danger' :
                      'bg-warning'
                    }`}
                    style={{ width: `${Math.abs(news.sentiment) * 100}%` }}
                  />
                </div>
                <span className="text-xs text-dark-muted">
                  {news.sentiment > 0.3 ? 'Bullish' : news.sentiment < -0.3 ? 'Bearish' : 'Neutral'}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
