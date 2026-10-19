import { useEffect, useRef, useState } from 'react';
import { createChart, CandlestickSeries, LineSeries, HistogramSeries, createSeriesMarkers } from 'lightweight-charts';
import type { IChartApi, Time } from 'lightweight-charts';
import { generateOHLCVData, recentSignals } from '../data/mockData';
import { TrendingUp, TrendingDown, Activity, Info } from 'lucide-react';

export default function ChartPage() {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const [selectedSymbol, setSelectedSymbol] = useState('BTC/USDT');
  const [selectedTimeframe, setSelectedTimeframe] = useState('1D');
  const [showSignals, setShowSignals] = useState(true);
  const [selectedSignal, setSelectedSignal] = useState(recentSignals[0]);

  const symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'AVAX/USDT', 'ADA/USDT'];
  const timeframes = ['5M', '15M', '1H', '4H', '1D'];

  useEffect(() => {
    if (!chartContainerRef.current) return;

    if (chartRef.current) {
      chartRef.current.remove();
      chartRef.current = null;
    }

    const chart = createChart(chartContainerRef.current, {
      layout: {
        background: { color: '#0f1117' },
        textColor: '#94a3b8',
      },
      grid: {
        vertLines: { color: '#1a1d29' },
        horzLines: { color: '#1a1d29' },
      },
      crosshair: {
        vertLine: { color: '#6366f1', width: 1, style: 2, labelBackgroundColor: '#6366f1' },
        horzLine: { color: '#6366f1', width: 1, style: 2, labelBackgroundColor: '#6366f1' },
      },
      rightPriceScale: {
        borderColor: '#2a2d3a',
      },
      timeScale: {
        borderColor: '#2a2d3a',
        timeVisible: true,
      },
      width: chartContainerRef.current.clientWidth,
      height: 400,
    });

    // Candlestick series
    const candlestickSeries = chart.addSeries(CandlestickSeries, {
      upColor: '#10b981',
      downColor: '#ef4444',
      borderDownColor: '#ef4444',
      borderUpColor: '#10b981',
      wickDownColor: '#ef4444',
      wickUpColor: '#10b981',
    });

    const data = generateOHLCVData(90);
    const candleData = data.map(d => ({
      time: d.time as Time,
      open: d.open,
      high: d.high,
      low: d.low,
      close: d.close,
    }));
    candlestickSeries.setData(candleData);

    // EMA 20 line
    const ema20Series = chart.addSeries(LineSeries, {
      color: '#f59e0b',
      lineWidth: 1,
      title: 'EMA 20',
    });

    const ema50Series = chart.addSeries(LineSeries, {
      color: '#6366f1',
      lineWidth: 1,
      title: 'EMA 50',
    });

    const ema20Data = calculateEMA(data, 20);
    const ema50Data = calculateEMA(data, 50);
    ema20Series.setData(ema20Data as any);
    ema50Series.setData(ema50Data as any);

    // Signal markers
    if (showSignals) {
      const markers = generateSignalMarkers(data);
      createSeriesMarkers(candlestickSeries, markers);
    }

    // Volume histogram
    const volumeSeries = chart.addSeries(HistogramSeries, {
      color: '#6366f1',
      priceFormat: { type: 'volume' },
      priceScaleId: 'volume',
    });

    chart.priceScale('volume').applyOptions({
      scaleMargins: { top: 0.85, bottom: 0 },
    });

    const volumeData = data.map(d => ({
      time: d.time as Time,
      value: d.volume,
      color: d.close >= d.open ? 'rgba(16, 185, 129, 0.3)' : 'rgba(239, 68, 68, 0.3)',
    }));
    volumeSeries.setData(volumeData);

    chart.timeScale().fitContent();
    chartRef.current = chart;

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
  }, [selectedSymbol, selectedTimeframe, showSignals]);

  return (
    <div className="space-y-4 animate-fade-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">Chart & Signals</h1>
          <p className="text-sm text-dark-muted mt-1">Technical analysis with bot signal overlays</p>
        </div>
      </div>

      {/* Controls */}
      <div className="flex flex-wrap items-center gap-3">
        <div className="flex items-center gap-1 bg-dark-card rounded-lg border border-dark-border p-1">
          {symbols.map((sym) => (
            <button
              key={sym}
              onClick={() => setSelectedSymbol(sym)}
              className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                selectedSymbol === sym ? 'bg-primary text-white' : 'text-dark-muted hover:text-white'
              }`}
            >
              {sym.split('/')[0]}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-1 bg-dark-card rounded-lg border border-dark-border p-1">
          {timeframes.map((tf) => (
            <button
              key={tf}
              onClick={() => setSelectedTimeframe(tf)}
              className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                selectedTimeframe === tf ? 'bg-primary text-white' : 'text-dark-muted hover:text-white'
              }`}
            >
              {tf}
            </button>
          ))}
        </div>

        <button
          onClick={() => setShowSignals(!showSignals)}
          className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${
            showSignals
              ? 'bg-primary/10 border-primary/30 text-primary'
              : 'bg-dark-card border-dark-border text-dark-muted hover:text-white'
          }`}
        >
          <Activity className="w-3 h-3" />
          Bot Signals
        </button>
      </div>

      {/* Chart */}
      <div className="bg-dark-card rounded-xl border border-dark-border overflow-hidden">
        <div className="px-4 py-3 border-b border-dark-border flex items-center justify-between">
          <div className="flex items-center gap-3">
            <h3 className="text-sm font-semibold text-white">{selectedSymbol}</h3>
            <span className="text-xs text-dark-muted">{selectedTimeframe}</span>
          </div>
          <div className="flex items-center gap-4 text-xs">
            <div className="flex items-center gap-1">
              <div className="w-3 h-0.5 bg-warning" />
              <span className="text-dark-muted">EMA 20</span>
            </div>
            <div className="flex items-center gap-1">
              <div className="w-3 h-0.5 bg-primary" />
              <span className="text-dark-muted">EMA 50</span>
            </div>
            {showSignals && (
              <>
                <div className="flex items-center gap-1">
                  <div className="w-2 h-2 rounded-full bg-success" />
                  <span className="text-dark-muted">Buy</span>
                </div>
                <div className="flex items-center gap-1">
                  <div className="w-2 h-2 rounded-full bg-danger" />
                  <span className="text-dark-muted">Sell</span>
                </div>
              </>
            )}
          </div>
        </div>
        <div ref={chartContainerRef} className="w-full" />
      </div>

      {/* Signal Detail Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-1 bg-dark-card rounded-xl border border-dark-border p-4">
          <h3 className="text-sm font-semibold text-white mb-3">Signal History</h3>
          <div className="space-y-2 max-h-80 overflow-y-auto">
            {recentSignals.map((signal) => (
              <button
                key={signal.id}
                onClick={() => setSelectedSignal(signal)}
                className={`w-full text-left p-3 rounded-lg border transition-colors ${
                  selectedSignal.id === signal.id
                    ? 'border-primary/50 bg-primary/5'
                    : 'border-dark-border/50 hover:border-dark-border'
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <div className="flex items-center gap-2">
                    {signal.signal === 'BUY' ? (
                      <TrendingUp className="w-3 h-3 text-success" />
                    ) : signal.signal === 'SELL' ? (
                      <TrendingDown className="w-3 h-3 text-danger" />
                    ) : (
                      <Activity className="w-3 h-3 text-warning" />
                    )}
                    <span className="text-xs font-semibold text-white">{signal.symbol}</span>
                  </div>
                  <span className={`text-xs font-bold ${
                    signal.signal === 'BUY' ? 'text-success' : signal.signal === 'SELL' ? 'text-danger' : 'text-warning'
                  }`}>
                    {signal.confidence}%
                  </span>
                </div>
                <p className="text-xs text-dark-muted">{signal.timestamp}</p>
              </button>
            ))}
          </div>
        </div>

        <div className="lg:col-span-2 bg-dark-card rounded-xl border border-dark-border p-4">
          <div className="flex items-center gap-2 mb-4">
            <Info className="w-4 h-4 text-primary" />
            <h3 className="text-sm font-semibold text-white">Signal Explanation (XAI)</h3>
          </div>

          <div className="bg-dark-bg/50 rounded-lg p-4 border border-dark-border mb-4">
            <div className="flex items-center gap-3 mb-3">
              <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                selectedSignal.signal === 'BUY' ? 'bg-success/10' : selectedSignal.signal === 'SELL' ? 'bg-danger/10' : 'bg-warning/10'
              }`}>
                {selectedSignal.signal === 'BUY' ? (
                  <TrendingUp className="w-5 h-5 text-success" />
                ) : selectedSignal.signal === 'SELL' ? (
                  <TrendingDown className="w-5 h-5 text-danger" />
                ) : (
                  <Activity className="w-5 h-5 text-warning" />
                )}
              </div>
              <div>
                <p className="text-sm font-bold text-white">
                  Bot merekomendasikan <span className={
                    selectedSignal.signal === 'BUY' ? 'text-success' : selectedSignal.signal === 'SELL' ? 'text-danger' : 'text-warning'
                  }>{selectedSignal.signal}</span> {selectedSignal.symbol}
                </p>
                <p className="text-xs text-dark-muted">Timeframe: {selectedSignal.timeframe} • Confidence: {selectedSignal.confidence}%</p>
              </div>
            </div>

            <div className="space-y-2">
              <p className="text-xs font-medium text-dark-muted uppercase tracking-wider">Alasan:</p>
              {selectedSignal.reasons.map((reason, idx) => (
                <div key={idx} className="flex items-start gap-2">
                  <span className="text-xs text-primary font-bold mt-0.5">{idx + 1}.</span>
                  <p className="text-xs text-dark-text leading-relaxed">{reason}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-gradient-to-r from-primary/5 to-purple-500/5 rounded-lg p-4 border border-primary/20">
            <p className="text-xs font-medium text-primary mb-2">💡 Penjelasan untuk Pemula:</p>
            <p className="text-xs text-dark-text leading-relaxed">
              {selectedSignal.signal === 'BUY'
                ? `Bot mendeteksi peluang beli pada ${selectedSignal.symbol} karena beberapa indikator teknikal menunjukkan kondisi yang mendukung kenaikan harga. Dengan confidence ${selectedSignal.confidence}%, bot yakin ini adalah peluang yang baik. Risiko dibatasi dengan stop-loss otomatis.`
                : selectedSignal.signal === 'SELL'
                ? `Bot mendeteksi sinyal jual pada ${selectedSignal.symbol} karena indikator menunjukkan potensi penurunan harga. Dengan confidence ${selectedSignal.confidence}%, bot merekomendasikan untuk mengambil profit atau mengurangi posisi.`
                : `Bot belum memiliki sinyal yang jelas untuk ${selectedSymbol}. Indikator menunjukkan kondisi netral, jadi bot memilih untuk menunggu peluang yang lebih baik. Ini adalah keputusan yang aman dan tepat.`
              }
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

function calculateEMA(data: { time: number; close: number }[], period: number) {
  const result: { time: number; value: number }[] = [];
  const multiplier = 2 / (period + 1);
  let ema = data[0].close;
  for (let i = 0; i < data.length; i++) {
    ema = (data[i].close - ema) * multiplier + ema;
    if (i >= period - 1) {
      result.push({ time: data[i].time, value: Math.round(ema * 100) / 100 });
    }
  }
  return result;
}

function generateSignalMarkers(data: { time: number; low: number; high: number }[]) {
  const markers: any[] = [];
  const signalPositions = [15, 28, 42, 55, 68, 78, 85];

  signalPositions.forEach((pos, idx) => {
    if (pos < data.length) {
      const isBuy = idx % 3 !== 2;
      markers.push({
        time: data[pos].time as Time,
        position: isBuy ? 'belowBar' as const : 'aboveBar' as const,
        color: isBuy ? '#10b981' : '#ef4444',
        shape: isBuy ? 'arrowUp' as const : 'arrowDown' as const,
        text: isBuy ? 'BUY' : 'SELL',
      });
    }
  });

  return markers.sort((a, b) => (a.time as number) - (b.time as number));
}
