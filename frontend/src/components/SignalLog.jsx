import { useActiveSignals } from '../hooks';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

export default function SignalLog() {
  const { signals, loading, error } = useActiveSignals();

  if (loading) {
    return (
      <div className="bg-slate-800 rounded-lg border border-slate-700 p-6">
        <div className="text-white text-center">Loading signals...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-slate-800 rounded-lg border border-slate-700 p-6">
        <div className="text-red-500 text-center">Error: {error}</div>
      </div>
    );
  }

  const getSignalIcon = (signal) => {
    if (signal.includes('BUY')) {
      return <TrendingUp className="w-5 h-5 text-green-500" />;
    } else if (signal.includes('SELL')) {
      return <TrendingDown className="w-5 h-5 text-red-500" />;
    } else {
      return <Minus className="w-5 h-5 text-slate-500" />;
    }
  };

  const getSignalColor = (signal) => {
    if (signal.includes('BUY')) {
      return 'bg-green-500/10 border-green-500/20 text-green-500';
    } else if (signal.includes('SELL')) {
      return 'bg-red-500/10 border-red-500/20 text-red-500';
    } else {
      return 'bg-slate-500/10 border-slate-500/20 text-slate-500';
    }
  };

  return (
    <div className="bg-slate-800 rounded-lg border border-slate-700 p-6">
      <h2 className="text-xl font-bold text-white mb-4">Active Signals</h2>
      
      {signals.length === 0 ? (
        <div className="text-center text-slate-400 py-8">
          No active signals
        </div>
      ) : (
        <div className="space-y-3">
          {signals.map((signal, index) => (
            <div
              key={index}
              className={`border rounded-lg p-4 ${getSignalColor(signal.signal)}`}
            >
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  {getSignalIcon(signal.signal)}
                  <span className="font-bold text-lg">{signal.symbol}</span>
                </div>
                <span className="text-sm font-medium">
                  {signal.confidence.toFixed(1)}% confidence
                </span>
              </div>
              
              <div className="grid grid-cols-2 gap-4 text-sm mb-3">
                <div>
                  <span className="text-slate-400">Signal:</span>
                  <span className="ml-2 font-medium">{signal.signal}</span>
                </div>
                <div>
                  <span className="text-slate-400">Price:</span>
                  <span className="ml-2 font-medium">${signal.latest_price.toFixed(2)}</span>
                </div>
                <div>
                  <span className="text-slate-400">Timeframe:</span>
                  <span className="ml-2 font-medium">{signal.timeframe}</span>
                </div>
                <div>
                  <span className="text-slate-400">Score:</span>
                  <span className="ml-2 font-medium">{signal.final_score.toFixed(2)}</span>
                </div>
              </div>

              {signal.reasons && signal.reasons.length > 0 && (
                <div className="mt-3 pt-3 border-t border-slate-700/30">
                  <div className="text-xs text-slate-400 mb-1">Reasons:</div>
                  <ul className="space-y-1">
                    {signal.reasons.slice(0, 3).map((reason, idx) => (
                      <li key={idx} className="text-xs">
                        • {reason}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {signal.suggested_actions && signal.suggested_actions.action !== 'HOLD' && (
                <div className="mt-3 pt-3 border-t border-slate-700/30">
                  <div className="text-xs text-slate-400 mb-2">Suggested Actions:</div>
                  <div className="grid grid-cols-3 gap-2 text-xs">
                    <div>
                      <span className="text-slate-400">Entry:</span>
                      <div className="font-medium">
                        ${signal.suggested_actions.entry?.toFixed(2) || 'N/A'}
                      </div>
                    </div>
                    <div>
                      <span className="text-slate-400">Stop Loss:</span>
                      <div className="font-medium text-red-500">
                        ${signal.suggested_actions.stop_loss?.toFixed(2) || 'N/A'}
                      </div>
                    </div>
                    <div>
                      <span className="text-slate-400">Take Profit:</span>
                      <div className="font-medium text-green-500">
                        ${signal.suggested_actions.take_profit?.toFixed(2) || 'N/A'}
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
