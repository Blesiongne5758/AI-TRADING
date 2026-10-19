import { useState, useEffect } from 'react';
import axios from 'axios';
import { TrendingUp, TrendingDown } from 'lucide-react';

export default function SignalLog() {
  const [signals, setSignals] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSignals();
  }, []);

  const fetchSignals = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/signals/active');
      setSignals(res.data.signals);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching signals:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="p-8 text-white">Loading...</div>;
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-white mb-8">Active Signals</h1>

      <div className="space-y-4">
        {signals.map((signal, idx) => (
          <SignalCard key={idx} signal={signal} />
        ))}
      </div>
    </div>
  );
}

function SignalCard({ signal }) {
  const signalColors = {
    STRONG_BUY: 'bg-green-500/20 border-green-500',
    BUY: 'bg-green-500/10 border-green-500/50',
    NEUTRAL: 'bg-slate-500/10 border-slate-500/50',
    SELL: 'bg-red-500/10 border-red-500/50',
    STRONG_SELL: 'bg-red-500/20 border-red-500',
  };

  const signalIcons = {
    STRONG_BUY: TrendingUp,
    BUY: TrendingUp,
    NEUTRAL: null,
    SELL: TrendingDown,
    STRONG_SELL: TrendingDown,
  };

  const Icon = signalIcons[signal.signal];

  return (
    <div className={`bg-slate-800 rounded-lg p-6 border-l-4 ${signalColors[signal.signal]}`}>
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          {Icon && <Icon className="w-6 h-6 text-white" />}
          <div>
            <h3 className="text-xl font-bold text-white">{signal.symbol}</h3>
            <p className="text-slate-400">{signal.timeframe}</p>
          </div>
        </div>
        <div className="text-right">
          <p className="text-2xl font-bold text-white">${signal.latest_price.toFixed(2)}</p>
          <p className="text-slate-400">Confidence: {signal.confidence.toFixed(1)}%</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <p className="text-slate-400 text-sm">Technical Score</p>
          <p className={`text-lg font-bold ${signal.technical_score > 0 ? 'text-green-400' : 'text-red-400'}`}>
            {signal.technical_score.toFixed(2)}
          </p>
        </div>
        <div>
          <p className="text-slate-400 text-sm">Sentiment</p>
          <p className={`text-lg font-bold ${signal.sentiment_score > 0 ? 'text-green-400' : 'text-red-400'}`}>
            {signal.sentiment_label} ({signal.sentiment_score.toFixed(3)})
          </p>
        </div>
      </div>

      <div className="mb-4">
        <p className="text-slate-400 text-sm mb-2">Reasons:</p>
        <ul className="space-y-1">
          {signal.reasons.slice(0, 3).map((reason, idx) => (
            <li key={idx} className="text-slate-300 text-sm">• {reason}</li>
          ))}
        </ul>
      </div>

      {signal.suggested_actions.action !== 'HOLD' && (
        <div className="bg-slate-900 rounded-lg p-4">
          <p className="text-slate-400 text-sm mb-2">Suggested Actions:</p>
          <div className="grid grid-cols-3 gap-4 text-sm">
            <div>
              <p className="text-slate-400">Entry</p>
              <p className="text-white font-bold">${signal.suggested_actions.entry.toFixed(2)}</p>
            </div>
            <div>
              <p className="text-slate-400">Stop Loss</p>
              <p className="text-red-400 font-bold">${signal.suggested_actions.stop_loss.toFixed(2)}</p>
            </div>
            <div>
              <p className="text-slate-400">Take Profit</p>
              <p className="text-green-400 font-bold">${signal.suggested_actions.take_profit.toFixed(2)}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
