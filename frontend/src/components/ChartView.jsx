import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { createChart } from 'lightweight-charts';

export default function ChartView() {
  const [symbol, setSymbol] = useState('BTC/USDT');
  const [timeframe, setTimeframe] = useState('1h');
  const [candles, setCandles] = useState([]);
  const [signal, setSignal] = useState(null);
  const chartContainerRef = useRef(null);
  const chartRef = useRef(null);

  const symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT', 'XRP/USDT'];
  const timeframes = ['1m', '5m', '15m', '1h', '4h', '1d'];

  useEffect(() => {
    fetchData();
  }, [symbol, timeframe]);

  useEffect(() => {
    if (!chartContainerRef.current || candles.length === 0) return;

    // Create chart
    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: 500,
      layout: {
        background: { color: '#1e293b' },
        textColor: '#e2e8f0',
      },
      grid: {
        vertLines: { color: '#334155' },
        horzLines: { color: '#334155' },
      },
      timeScale: {
        borderColor: '#475569',
      },
      rightPriceScale: {
        borderColor: '#475569',
      },
    });

    // Add candlestick series
    const candleSeries = chart.addCandlestickSeries({
      upColor: '#10b981',
      downColor: '#ef4444',
      borderDownColor: '#ef4444',
      borderUpColor: '#10b981',
      wickDownColor: '#ef4444',
      wickUpColor: '#10b981',
    });

    // Format data
    const chartData = candles.map(c => ({
      time: c.timestamp / 1000,
      open: c.open,
      high: c.high,
      low: c.low,
      close: c.close,
    }));

    candleSeries.setData(chartData);

    // Add markers untuk sinyal
    if (signal) {
      const markers = [];
      
      if (signal.signal === 'BUY' || signal.signal === 'STRONG_BUY') {
        markers.push({
          time: chartData[chartData.length - 1].time,
          position: 'belowBar',
          color: '#10b981',
          shape: 'arrowUp',
          text: 'BUY',
        });
      } else if (signal.signal === 'SELL' || signal.signal === 'STRONG_SELL') {
        markers.push({
          time: chartData[chartData.length - 1].time,
          position: 'aboveBar',
          color: '#ef4444',
          shape: 'arrowDown',
          text: 'SELL',
        });
      }

      candleSeries.setMarkers(markers);
    }

    chart.timeScale().fitContent();
    chartRef.current = chart;

    // Handle resize
    const handleResize = () => {
      chart.applyOptions({ width: chartContainerRef.current.clientWidth });
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      chart.remove();
    };
  }, [candles, signal]);

  const fetchData = async () => {
    try {
      const [candlesRes, signalRes] = await Promise.all([
        axios.get(`http://localhost:8000/api/market/candles/${symbol}?timeframe=${timeframe}&limit=100`),
        axios.get(`http://localhost:8000/api/signals/analyze/${symbol}?timeframe=${timeframe}`),
      ]);
      
      setCandles(candlesRes.data.candles);
      setSignal(signalRes.data.signal);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-white mb-8">Chart Analysis</h1>

      {/* Controls */}
      <div className="flex gap-4 mb-6">
        <select
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
          className="bg-slate-800 text-white px-4 py-2 rounded-lg border border-slate-700"
        >
          {symbols.map(s => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>

        <div className="flex gap-2">
          {timeframes.map(tf => (
            <button
              key={tf}
              onClick={() => setTimeframe(tf)}
              className={`px-4 py-2 rounded-lg ${
                timeframe === tf
                  ? 'bg-primary-500 text-white'
                  : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
              }`}
            >
              {tf}
            </button>
          ))}
        </div>
      </div>

      {/* Signal Info */}
      {signal && (
        <div className="bg-slate-800 rounded-lg p-6 mb-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-xl font-bold text-white">{signal.signal}</h3>
              <p className="text-slate-400">Confidence: {signal.confidence.toFixed(1)}%</p>
            </div>
            <div className="text-right">
              <p className="text-2xl font-bold text-white">${signal.latest_price.toFixed(2)}</p>
              <p className="text-slate-400">Score: {signal.final_score.toFixed(2)}</p>
            </div>
          </div>
        </div>
      )}

      {/* Chart */}
      <div ref={chartContainerRef} className="bg-slate-800 rounded-lg" />
    </div>
  );
}
