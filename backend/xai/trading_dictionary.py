"""
Trading Dictionary
Kamus istilah trading crypto dengan penjelasan dalam bahasa Indonesia
"""
from typing import Dict, Optional
from loguru import logger


class TradingDictionary:
    """
    Kamus istilah trading untuk edukasi pemula
    
    Berisi 50+ istilah trading dengan:
    - Definisi dalam bahasa Indonesia
    - Contoh penggunaan
    - Kategori (technical, fundamental, risk, dll)
    """

    def __init__(self):
        """Initialize kamus trading"""
        self.terms = self._build_dictionary()
        logger.info(f"📚 Trading Dictionary loaded: {len(self.terms)} terms")

    def _build_dictionary(self) -> Dict[str, Dict]:
        """Build kamus istilah trading"""
        return {
            # ========================================
            # TECHNICAL ANALYSIS
            # ========================================
            "rsi": {
                "term": "RSI (Relative Strength Index)",
                "definition": "Indikator momentum yang mengukur kecepatan dan perubahan pergerakan harga. Nilainya 0-100.",
                "interpretation": {
                    "> 70": "Overbought (jenuh beli) - potensi harga turun",
                    "< 30": "Oversold (jenuh jual) - potensi harga naik",
                    "30-70": "Netral - tidak ada sinyal kuat"
                },
                "example": "RSI BTC = 28 → Market oversold, potensi rebound naik",
                "category": "technical"
            },
            "macd": {
                "term": "MACD (Moving Average Convergence Divergence)",
                "definition": "Indikator trend-following yang menunjukkan hubungan antara dua moving average harga.",
                "components": {
                    "MACD Line": "EMA 12 - EMA 26",
                    "Signal Line": "EMA 9 dari MACD Line",
                    "Histogram": "MACD Line - Signal Line"
                },
                "interpretation": {
                    "MACD > Signal": "Bullish crossover - sinyal beli",
                    "MACD < Signal": "Bearish crossover - sinyal jual",
                    "Histogram positif": "Momentum naik",
                    "Histogram negatif": "Momentum turun"
                },
                "example": "MACD histogram berbalik positif → Momentum bullish, sinyal beli",
                "category": "technical"
            },
            "ema": {
                "term": "EMA (Exponential Moving Average)",
                "definition": "Rata-rata harga dengan bobot lebih besar pada data terbaru. Lebih responsif daripada SMA.",
                "periods": {
                    "EMA 20": "Short-term trend",
                    "EMA 50": "Medium-term trend",
                    "EMA 200": "Long-term trend"
                },
                "interpretation": {
                    "Price > EMA": "Bullish trend",
                    "Price < EMA": "Bearish trend",
                    "EMA 20 > EMA 50 > EMA 200": "Strong uptrend (golden alignment)"
                },
                "example": "EMA 20 memotong ke atas EMA 50 → Golden cross, sinyal bullish kuat",
                "category": "technical"
            },
            "bollinger": {
                "term": "Bollinger Bands",
                "definition": "Indikator volatilitas yang terdiri dari 3 garis: middle band (SMA 20), upper band, dan lower band.",
                "components": {
                    "Middle Band": "SMA 20 periode",
                    "Upper Band": "Middle + (2 × Standard Deviation)",
                    "Lower Band": "Middle - (2 × Standard Deviation)"
                },
                "interpretation": {
                    "Price > Upper": "Overbought - potensi pullback",
                    "Price < Lower": "Oversold - potensi bounce",
                    "Bands menyempit": "Low volatility - potensi breakout"
                },
                "example": "Harga menyentuh lower band + RSI oversold → Potensi reversal naik",
                "category": "technical"
            },
            "atr": {
                "term": "ATR (Average True Range)",
                "definition": "Indikator volatilitas yang mengukur rata-rata pergerakan harga dalam periode tertentu.",
                "usage": "Digunakan untuk menentukan stop-loss dan take-profit yang adaptif terhadap volatilitas market.",
                "example": "ATR = $1,400 → Stop-loss = 2 × ATR = $2,800 dari entry price",
                "category": "technical"
            },
            "volume": {
                "term": "Volume",
                "definition": "Jumlah aset yang diperdagangkan dalam periode tertentu. Mengkonfirmasi strength pergerakan harga.",
                "interpretation": {
                    "Volume tinggi + harga naik": "Strong bullish - konfirmasi uptrend",
                    "Volume tinggi + harga turun": "Strong bearish - konfirmasi downtrend",
                    "Volume rendah": "Weak movement - sinyal tidak reliable"
                },
                "example": "Volume 2x rata-rata + harga naik → Konfirmasi kuat untuk uptrend",
                "category": "technical"
            },
            "support": {
                "term": "Support",
                "definition": "Level harga di mana tekanan beli cukup kuat untuk mencegah harga turun lebih lanjut.",
                "characteristics": [
                    "Harga cenderung bounce dari level ini",
                    "Semakin sering di-test, semakin kuat",
                    "Break support = sinyal bearish"
                ],
                "example": "BTC support di $65,000 → Harga cenderung反弹 dari level ini",
                "category": "technical"
            },
            "resistance": {
                "term": "Resistance",
                "definition": "Level harga di mana tekanan jual cukup kuat untuk mencegah harga naik lebih lanjut.",
                "characteristics": [
                    "Harga cenderung reject dari level ini",
                    "Semakin sering di-test, semakin kuat",
                    "Break resistance = sinyal bullish"
                ],
                "example": "BTC resistance di $70,000 → Harga sulit tembus level ini",
                "category": "technical"
            },
            "golden_cross": {
                "term": "Golden Cross",
                "definition": "Ketika EMA/Moving Average jangka pendek memotong ke atas EMA jangka panjang. Sinyal bullish kuat.",
                "example": "EMA 20 memotong ke atas EMA 50 → Golden cross terkonfirmasi, uptrend dimulai",
                "category": "technical"
            },
            "death_cross": {
                "term": "Death Cross",
                "definition": "Ketika EMA/Moving Average jangka pendek memotong ke bawah EMA jangka panjang. Sinyal bearish kuat.",
                "example": "EMA 20 memotong ke bawah EMA 50 → Death cross terkonfirmasi, downtrend dimulai",
                "category": "technical"
            },

            # ========================================
            # TRADING TERMS
            # ========================================
            "long": {
                "term": "Long Position",
                "definition": "Posisi beli - mengharapkan harga naik untuk profit.",
                "example": "Open LONG BTC @ $67,000 → Profit jika harga naik di atas $67,000",
                "category": "trading"
            },
            "short": {
                "term": "Short Position",
                "definition": "Posisi jual - mengharapkan harga turun untuk profit.",
                "example": "Open SHORT BTC @ $67,000 → Profit jika harga turun di bawah $67,000",
                "category": "trading"
            },
            "entry": {
                "term": "Entry Price",
                "definition": "Harga saat membuka posisi trading.",
                "example": "Entry BTC LONG @ $67,234.50",
                "category": "trading"
            },
            "exit": {
                "term": "Exit Price",
                "definition": "Harga saat menutup posisi trading.",
                "example": "Exit BTC LONG @ $70,000 → Profit $2,765.50",
                "category": "trading"
            },
            "stop_loss": {
                "term": "Stop Loss (SL)",
                "definition": "Order otomatis untuk menutup posisi saat harga mencapai level tertentu, membatasi kerugian.",
                "importance": "WAJIB digunakan untuk risk management. Bot menggunakan max 2% risiko per trade.",
                "example": "Entry $67,000, SL $65,660 → Max loss 2% jika SL ter-trigger",
                "category": "risk"
            },
            "take_profit": {
                "term": "Take Profit (TP)",
                "definition": "Order otomatis untuk menutup posisi saat harga mencapai target profit.",
                "example": "Entry $67,000, TP $70,350 → Target profit 5%",
                "category": "risk"
            },
            "pnl": {
                "term": "P&L (Profit and Loss)",
                "definition": "Keuntungan atau kerugian dari trading. Dihitung setelah dikurangi trading fee.",
                "formula": "P&L = (Exit Price - Entry Price) × Quantity - Fees",
                "example": "P&L = +$100 (profit) atau -$50 (loss)",
                "category": "trading"
            },
            "drawdown": {
                "term": "Drawdown",
                "definition": "Penurunan portfolio dari peak tertinggi ke trough terendah. Mengukur risiko maksimum.",
                "example": "Max drawdown 5% → Portfolio pernah turun 5% dari titik tertinggi",
                "category": "risk"
            },
            "position_size": {
                "term": "Position Size",
                "definition": "Jumlah modal yang digunakan untuk satu trade. Bot menggunakan 2-10% dari portfolio.",
                "factors": [
                    "Confidence level (semakin tinggi = semakin besar)",
                    "Risk per trade (max 2%)",
                    "Available balance"
                ],
                "example": "Position size 5% dari $10,000 = $500",
                "category": "risk"
            },

            # ========================================
            # SIGNAL & CONFIDENCE
            # ========================================
            "signal": {
                "term": "Trading Signal",
                "definition": "Rekomendasi bot untuk BUY, SELL, atau HOLD berdasarkan analisis teknikal dan sentimen.",
                "types": {
                    "STRONG_BUY": "Sinyal beli sangat kuat (confidence ≥ 75%)",
                    "BUY": "Sinyal beli (confidence 55-74%)",
                    "HOLD": "Tidak ada sinyal kuat, tunggu konfirmasi",
                    "SELL": "Sinyal jual (confidence 55-74%)",
                    "STRONG_SELL": "Sinyal jual sangat kuat (confidence ≥ 75%)"
                },
                "example": "Signal: STRONG_BUY, Confidence: 85% → Rekomendasi beli dengan keyakinan tinggi",
                "category": "signal"
            },
            "confidence": {
                "term": "Confidence Score",
                "definition": "Skor 0-100% yang menunjukkan seberapa yakin bot dengan sinyal tradingnya.",
                "interpretation": {
                    "≥ 75%": "High confidence - sinyal kuat",
                    "55-74%": "Medium confidence - sinyal moderate",
                    "< 55%": "Low confidence - sinyal lemah, tidak di-trade"
                },
                "calculation": "Berdasarkan weighted average dari semua indikator teknikal dan sentimen",
                "example": "Confidence 85% → 85% indikator mendukung sinyal BUY",
                "category": "signal"
            },
            "risk_reward": {
                "term": "Risk/Reward Ratio",
                "definition": "Perbandingan antara potensi loss (risk) dan potensi profit (reward).",
                "formula": "Risk/Reward = Reward Distance / Risk Distance",
                "interpretation": {
                    "1:2": "Untuk setiap $1 risiko, target profit $2 (GOOD)",
                    "1:3": "Untuk setiap $1 risiko, target profit $3 (VERY GOOD)",
                    "< 1:1": "Risk lebih besar dari reward (BAD)"
                },
                "example": "SL distance $1,400, TP distance $2,800 → Risk/Reward 1:2",
                "category": "risk"
            },

            # ========================================
            # SENTIMENT ANALYSIS
            # ========================================
            "sentiment": {
                "term": "Sentiment Analysis",
                "definition": "Analisis berita dan media sosial menggunakan AI untuk mengukur sentimen pasar.",
                "score": {
                    "+1.0": "Sangat bullish (sangat positif)",
                    "+0.5": "Moderately bullish",
                    "0.0": "Netral",
                    "-0.5": "Moderately bearish",
                    "-1.0": "Sangat bearish (sangat negatif)"
                },
                "impact": "Sentimen berita mempengaruhi 10-30% dari keputusan trading bot",
                "example": "Sentiment score +0.65 → Berita cenderung positif, mendukung sinyal beli",
                "category": "sentiment"
            },
            "bullish": {
                "term": "Bullish",
                "definition": "Kondisi market yang optimis, mengharapkan harga naik. Berasal dari cara banteng menyerang (menanduk ke atas).",
                "indicators": [
                    "RSI < 30 (oversold)",
                    "MACD bullish crossover",
                    "Price > EMA",
                    "Volume tinggi + harga naik",
                    "Sentimen positif"
                ],
                "example": "Market bullish → Ekspektasi harga akan naik",
                "category": "sentiment"
            },
            "bearish": {
                "term": "Bearish",
                "definition": "Kondisi market yang pesimis, mengharapkan harga turun. Berasal dari cara beruang menyerang (menampar ke bawah).",
                "indicators": [
                    "RSI > 70 (overbought)",
                    "MACD bearish crossover",
                    "Price < EMA",
                    "Volume tinggi + harga turun",
                    "Sentimen negatif"
                ],
                "example": "Market bearish → Ekspektasi harga akan turun",
                "category": "sentiment"
            },

            # ========================================
            # RISK MANAGEMENT
            # ========================================
            "risk_management": {
                "term": "Risk Management",
                "definition": "Strategi untuk mengelola dan membatasi risiko dalam trading.",
                "bot_rules": [
                    "Max 2% risiko per trade",
                    "Max 5 posisi terbuka bersamaan",
                    "Max 20% portfolio per posisi",
                    "Daily loss limit 5%",
                    "Min confidence 55% untuk trade"
                ],
                "importance": "SANGAT PENTING untuk mencegah kerugian besar",
                "example": "Risk management aktif → Max loss per trade hanya 2% dari portfolio",
                "category": "risk"
            },
            "position_sizing": {
                "term": "Position Sizing",
                "definition": "Menentukan jumlah modal yang digunakan untuk satu trade berdasarkan risk tolerance.",
                "bot_logic": {
                    "Confidence ≥ 75%": "Position size 10% dari portfolio",
                    "Confidence 60-74%": "Position size 5% dari portfolio",
                    "Confidence < 60%": "Position size 2% dari portfolio"
                },
                "example": "Portfolio $10,000, confidence 80% → Position size $1,000 (10%)",
                "category": "risk"
            },
            "daily_loss_limit": {
                "term": "Daily Loss Limit",
                "definition": "Batas kerugian harian. Jika tercapai, bot stop trading sampai hari berikutnya.",
                "bot_setting": "5% dari initial balance ($500 dari $10,000)",
                "purpose": "Mencegah emotional trading dan kerugian beruntun",
                "example": "Daily loss limit $500 → Jika loss hari ini sudah $500, bot stop trading",
                "category": "risk"
            },

            # ========================================
            # MARKET CONDITIONS
            # ========================================
            "overbought": {
                "term": "Overbought",
                "definition": "Kondisi dimana harga sudah naik terlalu banyak dan cepat, potensi koreksi turun.",
                "indicators": [
                    "RSI > 70",
                    "Price > Upper Bollinger Band",
                    "Volume sangat tinggi"
                ],
                "action": "Pertimbangkan untuk take profit atau jangan entry baru",
                "example": "RSI = 78 → Market overbought, potensi koreksi",
                "category": "market"
            },
            "oversold": {
                "term": "Oversold",
                "definition": "Kondisi dimana harga sudah turun terlalu banyak dan cepat, potensi rebound naik.",
                "indicators": [
                    "RSI < 30",
                    "Price < Lower Bollinger Band",
                    "Volume sangat tinggi"
                ],
                "action": "Pertimbangkan untuk entry (buy the dip)",
                "example": "RSI = 25 → Market oversold, potensi rebound",
                "category": "market"
            },
            "breakout": {
                "term": "Breakout",
                "definition": "Ketika harga menembus level support atau resistance dengan volume tinggi.",
                "types": {
                    "Breakout resistance": "Bullish signal - harga naik lebih tinggi",
                    "Breakdown support": "Bearish signal - harga turun lebih rendah"
                },
                "confirmation": "Butuh volume tinggi untuk konfirmasi breakout valid",
                "example": "BTC breakout resistance $70,000 dengan volume 2x → Bullish breakout confirmed",
                "category": "market"
            },
            "consolidation": {
                "term": "Consolidation",
                "definition": "Fase dimana harga bergerak sideways (datar) dalam range tertentu sebelum breakout.",
                "characteristics": [
                    "Bollinger Bands menyempit",
                    "Volume rendah",
                    "Tidak ada trend jelas"
                ],
                "action": "Tunggu breakout, jangan entry saat consolidation",
                "example": "BTC consolidation $65,000-$67,000 → Tunggu breakout ke atas atau bawah",
                "category": "market"
            },

            # ========================================
            # TRADING FEES
            # ========================================
            "trading_fee": {
                "term": "Trading Fee",
                "definition": "Biaya yang dikenakan exchange untuk setiap transaksi trading.",
                "bot_simulation": "0.1% per trade (seperti Binance)",
                "impact": "Dihitung 2x: saat entry dan exit",
                "example": "Position $1,000 → Fee entry $1 + Fee exit $1 = Total fee $2",
                "category": "trading"
            },

            # ========================================
            # PAPER TRADING
            # ========================================
            "paper_trading": {
                "term": "Paper Trading",
                "definition": "Simulasi trading dengan uang virtual. Tidak ada risiko kehilangan uang nyata.",
                "benefits": [
                    "Belajar tanpa risiko",
                    "Test strategy",
                    "Build confidence",
                    "Understand market"
                ],
                "bot_setting": "Initial balance $10,000 (virtual)",
                "example": "Paper trading dengan $10,000 virtual → Belajar trading tanpa risiko",
                "category": "general"
            },

            # ========================================
            # PERFORMANCE METRICS
            # ========================================
            "win_rate": {
                "term": "Win Rate",
                "definition": "Persentase trade yang profit dari total trade.",
                "formula": "Win Rate = (Winning Trades / Total Trades) × 100%",
                "interpretation": {
                    "> 60%": "Good win rate",
                    "50-60%": "Average win rate",
                    "< 50%": "Poor win rate"
                },
                "example": "Win rate 70% → 7 dari 10 trade profit",
                "category": "performance"
            },
            "profit_factor": {
                "term": "Profit Factor",
                "definition": "Rasio antara total profit dan total loss. Mengukur efektivitas strategy.",
                "formula": "Profit Factor = Total Profit / Total Loss",
                "interpretation": {
                    "> 2.0": "Excellent strategy",
                    "1.5-2.0": "Good strategy",
                    "1.0-1.5": "Average strategy",
                    "< 1.0": "Losing strategy"
                },
                "example": "Profit factor 2.5 → Untuk setiap $1 loss, profit $2.50",
                "category": "performance"
            },
            "sharpe_ratio": {
                "term": "Sharpe Ratio",
                "definition": "Mengukur return yang disesuaikan dengan risiko. Semakin tinggi, semakin baik.",
                "interpretation": {
                    "> 2.0": "Excellent risk-adjusted return",
                    "1.0-2.0": "Good risk-adjusted return",
                    "< 1.0": "Poor risk-adjusted return"
                },
                "example": "Sharpe ratio 1.8 → Return yang baik relatif terhadap risiko",
                "category": "performance"
            },

            # ========================================
            # GENERAL TERMS
            # ========================================
            "dyor": {
                "term": "DYOR (Do Your Own Research)",
                "definition": "Prinsip penting dalam trading: selalu lakukan riset mandiri sebelum mengambil keputusan.",
                "importance": "Bot memberikan analisis, tapi keputusan final tetap di tangan Anda",
                "example": "DYOR → Jangan blindly follow bot, pahami analisisnya",
                "category": "general"
            },
            "fomo": {
                "term": "FOMO (Fear Of Missing Out)",
                "definition": "Rasa takut ketinggalan opportunity, sering menyebabkan entry di harga tinggi.",
                "danger": "Penyebab utama loss bagi trader pemula",
                "advice": "Jangan FOMO, tunggu signal yang jelas dari bot",
                "example": "Harga naik cepat → Jangan FOMO entry, tunggu pullback atau signal baru",
                "category": "psychology"
            },
            "hodl": {
                "term": "HODL (Hold On for Dear Life)",
                "definition": "Strategi hold aset dalam jangka panjang tanpa peduli fluktuasi jangka pendek.",
                "origin": "Typo dari 'HOLD' yang menjadi meme di crypto community",
                "example": "HODL BTC → Hold untuk jangka panjang, tidak panic sell saat downturn",
                "category": "strategy"
            },
        }

    def get_term(self, term: str) -> Optional[Dict]:
        """
        Ambil definisi istilah dari kamus
        
        Args:
            term: Istilah yang dicari (case-insensitive)
        
        Returns:
            Dictionary dengan definisi atau None jika tidak ditemukan
        """
        term_lower = term.lower().strip()
        
        # Direct match
        if term_lower in self.terms:
            return self.terms[term_lower]
        
        # Partial match
        for key, value in self.terms.items():
            if term_lower in key or term_lower in value["term"].lower():
                return value
        
        return None

    def search_terms(self, query: str) -> list:
        """
        Cari istilah berdasarkan query
        
        Args:
            query: Search query
        
        Returns:
            List of matching terms
        """
        query_lower = query.lower()
        results = []
        
        for key, value in self.terms.items():
            if (query_lower in key or 
                query_lower in value["term"].lower() or 
                query_lower in value["definition"].lower()):
                results.append(value)
        
        return results

    def get_terms_by_category(self, category: str) -> list:
        """
        Ambil semua istilah dalam kategori tertentu
        
        Args:
            category: Kategori (technical, trading, risk, sentiment, market, performance, general, psychology, strategy)
        
        Returns:
            List of terms in category
        """
        return [
            value for value in self.terms.values()
            if value.get("category") == category
        ]

    def format_term_explanation(self, term_data: Dict) -> str:
        """
        Format penjelasan istilah untuk ditampilkan
        
        Args:
            term_data: Dictionary dengan data istilah
        
        Returns:
            Formatted string
        """
        lines = []
        lines.append(f"📖 {term_data['term']}")
        lines.append(f"   {term_data['definition']}")
        
        if "interpretation" in term_data:
            lines.append("\n   Interpretasi:")
            for key, value in term_data["interpretation"].items():
                lines.append(f"     • {key}: {value}")
        
        if "components" in term_data:
            lines.append("\n   Komponen:")
            for key, value in term_data["components"].items():
                lines.append(f"     • {key}: {value}")
        
        if "example" in term_data:
            lines.append(f"\n   💡 Contoh: {term_data['example']}")
        
        if "category" in term_data:
            lines.append(f"\n   🏷️  Kategori: {term_data['category']}")
        
        return "\n".join(lines)
