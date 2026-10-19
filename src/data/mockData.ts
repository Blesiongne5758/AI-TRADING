export interface TradeSignal {
  id: string;
  symbol: string;
  timeframe: string;
  signal: 'BUY' | 'SELL' | 'HOLD';
  confidence: number;
  reasons: string[];
  timestamp: string;
  price: number;
  executed: boolean;
  pnl?: number;
}

export interface PortfolioStats {
  totalBalance: number;
  availableBalance: number;
  totalPnL: number;
  totalPnLPercent: number;
  winRate: number;
  totalTrades: number;
  winningTrades: number;
  losingTrades: number;
  maxDrawdown: number;
  sharpeRatio: number;
}

export interface Position {
  symbol: string;
  side: 'LONG' | 'SHORT';
  entryPrice: number;
  currentPrice: number;
  quantity: number;
  pnl: number;
  pnlPercent: number;
  stopLoss: number;
  takeProfit: number;
  entryTime: string;
}

export interface OHLCVData {
  time: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface NewsItem {
  id: string;
  title: string;
  source: string;
  sentiment: number;
  timestamp: string;
  summary: string;
}

export interface GlossaryTerm {
  term: string;
  definition: string;
  example: string;
}

export const portfolioStats: PortfolioStats = {
  totalBalance: 11247.83,
  availableBalance: 7832.50,
  totalPnL: 1247.83,
  totalPnLPercent: 12.48,
  winRate: 68.5,
  totalTrades: 47,
  winningTrades: 32,
  losingTrades: 15,
  maxDrawdown: 4.2,
  sharpeRatio: 1.85,
};

export const positions: Position[] = [
  {
    symbol: 'BTC/USDT',
    side: 'LONG',
    entryPrice: 67250.00,
    currentPrice: 68842.50,
    quantity: 0.045,
    pnl: 71.31,
    pnlPercent: 2.36,
    stopLoss: 65900.00,
    takeProfit: 71000.00,
    entryTime: '2024-01-15 08:30:00',
  },
  {
    symbol: 'ETH/USDT',
    side: 'LONG',
    entryPrice: 3420.00,
    currentPrice: 3512.80,
    quantity: 1.2,
    pnl: 111.36,
    pnlPercent: 2.71,
    stopLoss: 3320.00,
    takeProfit: 3650.00,
    entryTime: '2024-01-15 10:15:00',
  },
  {
    symbol: 'SOL/USDT',
    side: 'LONG',
    entryPrice: 142.50,
    currentPrice: 138.20,
    quantity: 25,
    pnl: -107.50,
    pnlPercent: -3.02,
    stopLoss: 135.00,
    takeProfit: 155.00,
    entryTime: '2024-01-14 22:00:00',
  },
];

export const recentSignals: TradeSignal[] = [
  {
    id: 'sig-001',
    symbol: 'BTC/USDT',
    timeframe: '1H',
    signal: 'BUY',
    confidence: 82,
    reasons: [
      'RSI (14) menunjukkan oversold di 28 pada timeframe 1H',
      'EMA 20 memotong ke atas EMA 50 (Golden Cross)',
      'Sentimen berita positif (+0.65) setelah berita adopsi institusi',
      'Volume meningkat 45% di atas rata-rata 20 hari',
    ],
    timestamp: '2024-01-15 08:30:00',
    price: 67250.00,
    executed: true,
    pnl: 71.31,
  },
  {
    id: 'sig-002',
    symbol: 'ETH/USDT',
    timeframe: '4H',
    signal: 'BUY',
    confidence: 75,
    reasons: [
      'MACD histogram berbalik positif setelah 3 candle bearish',
      'Harga memantul dari support kuat di $3,400',
      'Bollinger Bands menunjukkan squeeze - breakout imminent',
      'Sentimen pasar crypto secara keseluruhan bullish (+0.42)',
    ],
    timestamp: '2024-01-15 10:15:00',
    price: 3420.00,
    executed: true,
    pnl: 111.36,
  },
  {
    id: 'sig-003',
    symbol: 'SOL/USDT',
    timeframe: '15M',
    signal: 'BUY',
    confidence: 65,
    reasons: [
      'RSI recovery dari oversold region (32 → 38)',
      'Pola bullish engulfing pada candlestick 15M',
      'Volume spike di resistance level',
    ],
    timestamp: '2024-01-14 22:00:00',
    price: 142.50,
    executed: true,
    pnl: -107.50,
  },
  {
    id: 'sig-004',
    symbol: 'BTC/USDT',
    timeframe: '1H',
    signal: 'SELL',
    confidence: 71,
    reasons: [
      'RSI mencapai overbought di 78',
      'Bearish divergence pada MACD',
      'Harga menyentuh upper Bollinger Band',
      'Sentimen berita negatif (-0.35) setelah regulasi baru',
    ],
    timestamp: '2024-01-14 16:00:00',
    price: 69500.00,
    executed: true,
    pnl: 225.00,
  },
  {
    id: 'sig-005',
    symbol: 'ADA/USDT',
    timeframe: '4H',
    signal: 'HOLD',
    confidence: 45,
    reasons: [
      'Indikator teknikal menunjukkan sinyal campuran',
      'RSI netral di 52',
      'Sentimen berita netral (-0.05)',
      'Tidak ada pola chart yang jelas',
    ],
    timestamp: '2024-01-14 12:00:00',
    price: 0.58,
    executed: false,
  },
  {
    id: 'sig-006',
    symbol: 'AVAX/USDT',
    timeframe: '1H',
    signal: 'BUY',
    confidence: 88,
    reasons: [
      'Triple bottom pattern confirmed di $34.50',
      'Volume breakout 3x average',
      'EMA 20 > EMA 50 > EMA 200 (strong uptrend)',
      'Sentimen sangat positif (+0.78) dari partnership announcement',
    ],
    timestamp: '2024-01-13 20:00:00',
    price: 34.50,
    executed: true,
    pnl: 185.00,
  },
];

export const newsItems: NewsItem[] = [
  {
    id: 'news-001',
    title: 'BlackRock Bitcoin ETF sees record $1.1B inflows in single day',
    source: 'CoinDesk',
    sentiment: 0.85,
    timestamp: '2024-01-15 07:00:00',
    summary: 'Institutional adoption continues as BlackRock\'s iShares Bitcoin Trust records unprecedented single-day inflows.',
  },
  {
    id: 'news-002',
    title: 'Ethereum Dencun upgrade scheduled for March, could reduce L2 fees by 90%',
    source: 'CoinTelegraph',
    sentiment: 0.72,
    timestamp: '2024-01-15 05:30:00',
    summary: 'The upcoming Dencun upgrade promises to dramatically reduce transaction costs on Layer 2 networks.',
  },
  {
    id: 'news-003',
    title: 'SEC delays decision on multiple altcoin ETF applications',
    source: 'CoinDesk',
    sentiment: -0.45,
    timestamp: '2024-01-14 22:00:00',
    summary: 'Regulatory uncertainty continues as SEC pushes back decision timeline for several cryptocurrency ETF proposals.',
  },
  {
    id: 'news-004',
    title: 'Solana DeFi TVL reaches new all-time high of $8.5B',
    source: 'CoinTelegraph',
    sentiment: 0.68,
    timestamp: '2024-01-14 18:00:00',
    summary: 'Solana ecosystem continues to grow with total value locked in DeFi protocols hitting new records.',
  },
  {
    id: 'news-005',
    title: 'Major exchange reports 40% increase in trading volume this week',
    source: 'CoinDesk',
    sentiment: 0.35,
    timestamp: '2024-01-14 14:00:00',
    summary: 'Increased market activity suggests growing interest from both retail and institutional traders.',
  },
];

export const glossaryTerms: GlossaryTerm[] = [
  {
    term: 'RSI (Relative Strength Index)',
    definition: 'Indikator momentum yang mengukur kecepatan dan perubahan pergerakan harga. Nilainya 0-100. Di atas 70 = overbought (potensi turun), di bawah 30 = oversold (potensi naik).',
    example: 'RSI BTC = 28 → Market oversold, potensi harga naik dalam waktu dekat.',
  },
  {
    term: 'MACD (Moving Average Convergence Divergence)',
    definition: 'Indikator trend-following yang menunjukkan hubungan antara dua moving average harga. Terdiri dari MACD line, signal line, dan histogram.',
    example: 'MACD histogram berbalik positif → Momentum bullish, sinyal beli.',
  },
  {
    term: 'Golden Cross',
    definition: 'Ketika EMA/Moving Average jangka pendek (misal EMA 20) memotong ke atas EMA jangka panjang (misal EMA 50/200). Ini sinyal bullish yang kuat.',
    example: 'EMA 20 memotong EMA 50 ke atas → Golden Cross terkonfirmasi, tren naik dimulai.',
  },
  {
    term: 'Bollinger Bands',
    definition: 'Indikator volatilitas yang terdiri dari 3 garis: middle band (SMA 20), upper band, dan lower band. Harga cenderung bergerak di antara upper dan lower band.',
    example: 'Harga menyentuh lower band + RSI oversold → Potensi reversal naik.',
  },
  {
    term: 'Stop Loss',
    definition: 'Order otomatis untuk menjual aset ketika harga mencapai level tertentu, membatasi kerugian. Bot menggunakan max 2% risiko per trade.',
    example: 'Entry BTC $67,250, Stop Loss $65,900 → Max loss 2% jika terkena SL.',
  },
  {
    term: 'Drawdown',
    definition: 'Penurunan portfolio dari peak tertinggi ke trough terendah. Mengukur risiko maksimum yang pernah dialami.',
    example: 'Max drawdown 4.2% → Portfolio pernah turun 4.2% dari titik tertinggi.',
  },
  {
    term: 'Confidence Score',
    definition: 'Skor 0-100% yang menunjukkan seberapa yakin bot dengan sinyal tradingnya. Semakin tinggi, semakin banyak indikator yang mendukung sinyal.',
    example: 'Confidence 82% → 82% dari indikator teknikal dan sentimen mendukung sinyal BUY.',
  },
  {
    term: 'Sentiment Analysis',
    definition: 'Analisis berita dan media sosial menggunakan AI (FinBERT) untuk mengukur sentimen pasar. Skor -1 (sangat negatif) sampai +1 (sangat positif).',
    example: 'Sentimen +0.65 → Berita secara keseluruhan positif, mendukung sinyal beli.',
  },
  {
    term: 'Paper Trading',
    definition: 'Simulasi trading dengan uang virtual. Memungkinkan Anda belajar dan menguji strategi tanpa risiko kehilangan uang nyata.',
    example: 'Portfolio virtual $10,000 → Semua trade disimulasikan, tidak ada uang asli yang digunakan.',
  },
  {
    term: 'Sharpe Ratio',
    definition: 'Mengukur return yang disesuaikan dengan risiko. Semakin tinggi, semakin baik return per unit risiko yang diambil. > 1 dianggap baik.',
    example: 'Sharpe Ratio 1.85 → Return yang baik relatif terhadap risiko yang diambil.',
  },
];

// Generate OHLCV data for chart
export function generateOHLCVData(days: number = 90): OHLCVData[] {
  const data: OHLCVData[] = [];
  let price = 62000;
  const now = Math.floor(Date.now() / 1000);
  const dayInSeconds = 86400;

  for (let i = days; i >= 0; i--) {
    const time = now - (i * dayInSeconds);
    const change = (Math.random() - 0.48) * 2000;
    const open = price;
    const close = price + change;
    const high = Math.max(open, close) + Math.random() * 1000;
    const low = Math.min(open, close) - Math.random() * 1000;
    const volume = Math.floor(Math.random() * 50000 + 20000);

    data.push({
      time,
      open: Math.round(open * 100) / 100,
      high: Math.round(high * 100) / 100,
      low: Math.round(low * 100) / 100,
      close: Math.round(close * 100) / 100,
      volume,
    });

    price = close;
  }

  return data;
}

export const equityCurveData = [
  { date: 'Jan 1', balance: 10000 },
  { date: 'Jan 3', balance: 10120 },
  { date: 'Jan 5', balance: 10050 },
  { date: 'Jan 7', balance: 10280 },
  { date: 'Jan 9', balance: 10450 },
  { date: 'Jan 11', balance: 10380 },
  { date: 'Jan 13', balance: 10650 },
  { date: 'Jan 15', balance: 10820 },
  { date: 'Jan 17', balance: 10750 },
  { date: 'Jan 19', balance: 10980 },
  { date: 'Jan 21', balance: 11050 },
  { date: 'Jan 23', balance: 10920 },
  { date: 'Jan 25', balance: 11100 },
  { date: 'Jan 27', balance: 11247 },
];

export const performanceBySymbol = [
  { symbol: 'BTC/USDT', trades: 15, winRate: 73, pnl: 580 },
  { symbol: 'ETH/USDT', trades: 12, winRate: 67, pnl: 340 },
  { symbol: 'SOL/USDT', trades: 8, winRate: 50, pnl: -50 },
  { symbol: 'AVAX/USDT', trades: 6, winRate: 83, pnl: 280 },
  { symbol: 'ADA/USDT', trades: 4, winRate: 50, pnl: 45 },
  { symbol: 'LINK/USDT', trades: 2, winRate: 100, pnl: 52 },
];

// Trade History
export interface TradeHistory {
  id: string;
  symbol: string;
  side: 'BUY' | 'SELL';
  type: 'MARKET' | 'LIMIT';
  price: number;
  quantity: number;
  total: number;
  fee: number;
  timestamp: string;
  signalId: string;
  status: 'FILLED' | 'PARTIAL' | 'CANCELLED';
}

export const tradeHistory: TradeHistory[] = [
  { id: 't-001', symbol: 'BTC/USDT', side: 'BUY', type: 'MARKET', price: 67250.00, quantity: 0.045, total: 3026.25, fee: 3.03, timestamp: '2024-01-15 08:30:12', signalId: 'sig-001', status: 'FILLED' },
  { id: 't-002', symbol: 'ETH/USDT', side: 'BUY', type: 'MARKET', price: 3420.00, quantity: 1.2, total: 4104.00, fee: 4.10, timestamp: '2024-01-15 10:15:08', signalId: 'sig-002', status: 'FILLED' },
  { id: 't-003', symbol: 'SOL/USDT', side: 'BUY', type: 'LIMIT', price: 142.50, quantity: 25, total: 3562.50, fee: 3.56, timestamp: '2024-01-14 22:00:45', signalId: 'sig-003', status: 'FILLED' },
  { id: 't-004', symbol: 'BTC/USDT', side: 'SELL', type: 'MARKET', price: 69500.00, quantity: 0.032, total: 2224.00, fee: 2.22, timestamp: '2024-01-14 16:00:22', signalId: 'sig-004', status: 'FILLED' },
  { id: 't-005', symbol: 'AVAX/USDT', side: 'BUY', type: 'MARKET', price: 34.50, quantity: 100, total: 3450.00, fee: 3.45, timestamp: '2024-01-13 20:00:15', signalId: 'sig-006', status: 'FILLED' },
  { id: 't-006', symbol: 'LINK/USDT', side: 'BUY', type: 'LIMIT', price: 15.20, quantity: 150, total: 2280.00, fee: 2.28, timestamp: '2024-01-13 14:30:00', signalId: 'sig-007', status: 'FILLED' },
  { id: 't-007', symbol: 'BTC/USDT', side: 'BUY', type: 'MARKET', price: 65800.00, quantity: 0.03, total: 1974.00, fee: 1.97, timestamp: '2024-01-12 09:00:00', signalId: 'sig-008', status: 'FILLED' },
  { id: 't-008', symbol: 'ETH/USDT', side: 'SELL', type: 'MARKET', price: 3380.00, quantity: 0.8, total: 2704.00, fee: 2.70, timestamp: '2024-01-11 18:45:00', signalId: 'sig-009', status: 'FILLED' },
  { id: 't-009', symbol: 'SOL/USDT', side: 'SELL', type: 'MARKET', price: 148.00, quantity: 15, total: 2220.00, fee: 2.22, timestamp: '2024-01-11 12:00:00', signalId: 'sig-010', status: 'FILLED' },
  { id: 't-010', symbol: 'AVAX/USDT', side: 'SELL', type: 'LIMIT', price: 36.80, quantity: 50, total: 1840.00, fee: 1.84, timestamp: '2024-01-10 20:30:00', signalId: 'sig-011', status: 'FILLED' },
];

// System Module Status (Backend health)
export interface ModuleStatus {
  name: string;
  module: string;
  status: 'running' | 'warning' | 'error' | 'stopped';
  uptime: string;
  lastAction: string;
  details: string;
  metrics: { label: string; value: string }[];
}

export const moduleStatuses: ModuleStatus[] = [
  {
    name: 'Data Collector',
    module: 'data_collector',
    status: 'running',
    uptime: '14d 6h 32m',
    lastAction: '2 seconds ago',
    details: 'WebSocket connected to Binance. Collecting OHLCV data for 6 symbols across 6 timeframes.',
    metrics: [
      { label: 'WS Connections', value: '6/6' },
      { label: 'Candles Stored', value: '142,847' },
      { label: 'News Fetched', value: '847 today' },
      { label: 'DB Size', value: '234 MB' },
    ],
  },
  {
    name: 'Analysis Engine',
    module: 'analysis',
    status: 'running',
    uptime: '14d 6h 30m',
    lastAction: '15 seconds ago',
    details: 'Computing technical indicators and sentiment analysis. FinBERT model loaded.',
    metrics: [
      { label: 'Indicators', value: 'RSI, MACD, EMA, BB' },
      { label: 'Signals Today', value: '12' },
      { label: 'Avg Confidence', value: '72%' },
      { label: 'Model', value: 'FinBERT' },
    ],
  },
  {
    name: 'Paper Trading',
    module: 'paper_trading',
    status: 'running',
    uptime: '14d 6h 28m',
    lastAction: '5 minutes ago',
    details: 'Portfolio manager active. Risk management enforcing 2% max risk per trade.',
    metrics: [
      { label: 'Open Positions', value: '3' },
      { label: 'Total Trades', value: '47' },
      { label: 'Win Rate', value: '68.5%' },
      { label: 'Risk/Trade', value: '2%' },
    ],
  },
  {
    name: 'XAI Module',
    module: 'xai',
    status: 'running',
    uptime: '14d 6h 25m',
    lastAction: '1 minute ago',
    details: 'Explanation generator active. Chat agent ready for user queries.',
    metrics: [
      { label: 'Explanations', value: '47 generated' },
      { label: 'Chat Queries', value: '23 today' },
      { label: 'Avg Response', value: '1.2s' },
      { label: 'Language', value: 'ID/EN' },
    ],
  },
  {
    name: 'Telegram Bot',
    module: 'notifications',
    status: 'warning',
    uptime: '14d 6h 20m',
    lastAction: '12 minutes ago',
    details: 'Bot connected. Rate limit approaching. Consider upgrading to premium API.',
    metrics: [
      { label: 'Messages Sent', value: '156 today' },
      { label: 'Rate Limit', value: '78%' },
      { label: 'Subscribers', value: '1' },
      { label: 'Latency', value: '245ms' },
    ],
  },
  {
    name: 'FastAPI Server',
    module: 'api',
    status: 'running',
    uptime: '14d 6h 32m',
    lastAction: 'Active',
    details: 'REST API serving frontend requests. All endpoints healthy.',
    metrics: [
      { label: 'Endpoints', value: '12 active' },
      { label: 'Requests/min', value: '34' },
      { label: 'Avg Response', value: '45ms' },
      { label: 'Error Rate', value: '0.01%' },
    ],
  },
];

// Daily PnL data
export const dailyPnL = [
  { date: 'Jan 1', pnl: 0 },
  { date: 'Jan 3', pnl: 120 },
  { date: 'Jan 5', pnl: -70 },
  { date: 'Jan 7', pnl: 230 },
  { date: 'Jan 9', pnl: 170 },
  { date: 'Jan 11', pnl: -70 },
  { date: 'Jan 13', pnl: 270 },
  { date: 'Jan 15', pnl: 170 },
  { date: 'Jan 17', pnl: -70 },
  { date: 'Jan 19', pnl: 230 },
  { date: 'Jan 21', pnl: 70 },
  { date: 'Jan 23', pnl: -130 },
  { date: 'Jan 25', pnl: 180 },
  { date: 'Jan 27', pnl: 147 },
];

// Indicator values for current analysis
export interface IndicatorValue {
  name: string;
  value: string;
  signal: 'bullish' | 'bearish' | 'neutral';
  description: string;
}

export const currentIndicators: IndicatorValue[] = [
  { name: 'RSI (14)', value: '42.5', signal: 'neutral', description: 'Netral - tidak overbought/oversold' },
  { name: 'MACD', value: '+125.3', signal: 'bullish', description: 'Histogram positif, momentum naik' },
  { name: 'EMA 20', value: '68,250', signal: 'bullish', description: 'Harga di atas EMA 20' },
  { name: 'EMA 50', value: '67,100', signal: 'bullish', description: 'EMA 20 > EMA 50 (uptrend)' },
  { name: 'EMA 200', value: '62,800', signal: 'bullish', description: 'Jangka panjang masih bullish' },
  { name: 'Bollinger Bands', value: 'Middle', signal: 'neutral', description: 'Harga di tengah band' },
  { name: 'Volume', value: '+15%', signal: 'bullish', description: 'Volume di atas rata-rata 20 hari' },
  { name: 'Sentiment', value: '+0.42', signal: 'bullish', description: 'Berita cenderung positif' },
];
