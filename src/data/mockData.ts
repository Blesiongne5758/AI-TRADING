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
