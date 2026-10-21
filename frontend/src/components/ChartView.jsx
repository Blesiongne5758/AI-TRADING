import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { createChart, CandlestickSeries, HistogramSeries } from 'lightweight-charts';

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
    // Cleanup previous chart
    if (chartRef.current) {
      chartRef.current.remove();
      chartRef.current = null;
    }

    if (!chartContainerRef.current || candles.length === 0) return;

    // Create chart dengan null check
    const container = chartContainerRef.current;
    if (!container) return;

    const chart = createChart(container, {
      width: container.clientWidth,
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

    chartRef.current = chart;

    // Add candlestick series (API v4)
    const candleSeries = chart.addSeries(CandlestickSeries, {
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

    // Add volume series (API v4)
    const volumeSeries = chart.addSeries(HistogramSeries, {
      color: '#6366f1',
      priceFormat: {
        type: 'volume',
      },
      priceScaleId: '',
    });

    volumeSeries.priceScale().applyOptions({
      scaleMargins: {
        top: 0.8,
        bottom: 0,
      },
    });

    const volumeData = candles.map(c => ({
      time: c.timestamp / 1000,
      value: c.volume,
      color: c.close >= c.open ? 'rgba(16, 185, 129, 0.5)' : 'rgba(239, 68, 68, 0.5)',
    }));

    volumeSeries.setData(volumeData);

    chart.timeScale().fitContent();

    // Handle resize
    const handleResize = () => {
      if (chartContainerRef.current && chartRef.current) {
        chartRef.current.applyOptions({ width: chartContainerRef.current.clientWidth });
      }
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      if (chartRef.current) {
        chartRef.current.remove();
        chartRef.current = null;
      }
    };
  }, [candles]);

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
