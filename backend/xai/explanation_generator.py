"""
Explanation Generator
Generate narasi penjelasan dari signal trading dalam bahasa manusia
"""
from typing import Dict, List
from loguru import logger


class ExplanationGenerator:
    """
    Menggenerate penjelasan naratif dari signal trading
    
    Mengubah data teknis menjadi bahasa manusia yang mudah dipahami pemula
    """

    def __init__(self):
        """Initialize explanation generator"""
        logger.info("📝 Explanation Generator initialized")

    def generate_explanation(self, signal: Dict) -> str:
        """
        Generate penjelasan lengkap dari signal
        
        Args:
            signal: Output dari SignalGenerator
        
        Returns:
            Narasi penjelasan dalam bahasa manusia
        """
        lines = []
        
        # Header
        lines.append("=" * 70)
        lines.append("🤖 PENJELASAN KEPUTUSAN BOT")
        lines.append("=" * 70)
        lines.append("")
        
        # Summary
        lines.append(self._generate_summary(signal))
        lines.append("")
        
        # Detailed explanation
        lines.append(self._generate_detailed_explanation(signal))
        lines.append("")
        
        # Risk explanation
        lines.append(self._generate_risk_explanation(signal))
        lines.append("")
        
        # Educational notes
        lines.append(self._generate_educational_notes(signal))
        lines.append("")
        
        lines.append("=" * 70)
        
        return "\n".join(lines)

    def _generate_summary(self, signal: Dict) -> str:
        """Generate ringkasan keputusan"""
        symbol = signal["symbol"]
        action = signal["signal"]
        confidence = signal["confidence"]
        score = signal["final_score"]
        
        # Determine action verb
        if action in ["STRONG_BUY", "BUY"]:
            action_verb = "MEREKOMENDASIKAN BELI"
            emoji = "🟢"
        elif action in ["STRONG_SELL", "SELL"]:
            action_verb = "MEREKOMENDASIKAN JUAL"
            emoji = "🔴"
        else:
            action_verb = "TIDAK ADA REKOMENDASI"
            emoji = "⚪"
        
        lines = []
        lines.append(f"{emoji} Bot {action_verb} {symbol}")
        lines.append(f"   Confidence: {confidence:.1f}% | Score: {score:+.2f}")
        
        return "\n".join(lines)

    def _generate_detailed_explanation(self, signal: Dict) -> str:
        """Generate penjelasan detail"""
        lines = []
        lines.append("📊 ANALISIS DETAIL:")
        lines.append("")
        
        # Technical analysis
        lines.append("   1️⃣  ANALISIS TEKNIKAL:")
        interpretation = signal.get("interpretation", {})
        
        for indicator, data in interpretation.items():
            indicator_name = indicator.upper()
            signal_type = data.get("signal", "NEUTRAL")
            score = data.get("score", 0)
            reason = data.get("reason", "")
            
            # Emoji based on signal
            if score > 40:
                emoji = "🟢"
            elif score < -40:
                emoji = "🔴"
            else:
                emoji = "⚪"
            
            lines.append(f"      {emoji} {indicator_name}: {signal_type}")
            lines.append(f"         → {reason}")
        
        lines.append("")
        
        # Sentiment analysis
        lines.append("   2️⃣  ANALISIS SENTIMEN:")
        sentiment = signal.get("sentiment", {})
        sentiment_score = sentiment.get("overall_score", 0)
        sentiment_label = sentiment.get("overall_label", "NEUTRAL")
        pos_count = sentiment.get("positive_count", 0)
        neg_count = sentiment.get("negative_count", 0)
        total = sentiment.get("total_articles", 0)
        
        if sentiment_label == "POSITIVE":
            emoji = "🟢"
            sentiment_text = "positif"
        elif sentiment_label == "NEGATIVE":
            emoji = "🔴"
            sentiment_text = "negatif"
        else:
            emoji = "⚪"
            sentiment_text = "netral"
        
        lines.append(f"      {emoji} Sentimen berita: {sentiment_text} (score: {sentiment_score:+.3f})")
        lines.append(f"         → {pos_count} berita positif, {neg_count} berita negatif dari {total} artikel")
        
        return "\n".join(lines)

    def _generate_risk_explanation(self, signal: Dict) -> str:
        """Generate penjelasan risk management"""
        lines = []
        lines.append("🛡️  RISK MANAGEMENT:")
        lines.append("")
        
        suggested_actions = signal.get("suggested_actions", {})
        
        if suggested_actions.get("action") == "HOLD":
            lines.append("   ⏸️  Tidak ada trade yang direkomendasikan")
            lines.append("      → Tunggu signal yang lebih jelas")
            return "\n".join(lines)
        
        entry = suggested_actions.get("entry", 0)
        sl = suggested_actions.get("stop_loss", 0)
        tp = suggested_actions.get("take_profit", 0)
        position_size = suggested_actions.get("position_size_percent", 0)
        rr_ratio = suggested_actions.get("risk_reward_ratio", 0)
        
        # Calculate distances
        sl_distance = abs(entry - sl)
        tp_distance = abs(tp - entry)
        sl_percent = (sl_distance / entry) * 100 if entry > 0 else 0
        tp_percent = (tp_distance / entry) * 100 if entry > 0 else 0
        
        lines.append(f"   💰 Entry Price: ${entry:,.2f}")
        lines.append(f"   🛑 Stop Loss: ${sl:,.2f} (-{sl_percent:.2f}%)")
        lines.append(f"      → Jika harga turun ke ${sl:,.2f}, posisi otomatis ditutup")
        lines.append(f"      → Maksimal loss: {sl_percent:.2f}% dari entry")
        lines.append("")
        lines.append(f"   🎯 Take Profit: ${tp:,.2f} (+{tp_percent:.2f}%)")
        lines.append(f"      → Jika harga naik ke ${tp:,.2f}, posisi otomatis ditutup")
        lines.append(f"      → Target profit: {tp_percent:.2f}% dari entry")
        lines.append("")
        lines.append(f"   📊 Risk/Reward Ratio: 1:{rr_ratio:.1f}")
        lines.append(f"      → Untuk setiap $1 risiko, target profit ${rr_ratio:.1f}")
        lines.append("")
        lines.append(f"   💼 Position Size: {position_size:.1f}% dari portfolio")
        lines.append(f"      → Max risk per trade: 2% dari portfolio")
        
        return "\n".join(lines)

    def _generate_educational_notes(self, signal: Dict) -> str:
        """Generate catatan edukasi untuk pemula"""
        lines = []
        lines.append("📚 CATATAN EDUKASI:")
        lines.append("")
        
        action = signal["signal"]
        confidence = signal["confidence"]
        
        # Explanation based on action
        if action in ["STRONG_BUY", "BUY"]:
            lines.append("   💡 Mengapa bot merekomendasikan BELI?")
            lines.append("      → Indikator teknikal menunjukkan kondisi bullish")
            lines.append("      → Sentimen berita cenderung positif")
            lines.append("      → Ada potensi harga naik dalam jangka pendek")
            lines.append("")
            lines.append("   ⚠️  Penting untuk diingat:")
            lines.append("      → Trading selalu memiliki risiko")
            lines.append("      → Stop-loss WAJIB digunakan untuk membatasi kerugian")
            lines.append("      → Jangan invest uang yang tidak siap Anda rugikan")
            lines.append("      → DYOR (Do Your Own Research) sebelum trading")
        
        elif action in ["STRONG_SELL", "SELL"]:
            lines.append("   💡 Mengapa bot merekomendasikan JUAL?")
            lines.append("      → Indikator teknikal menunjukkan kondisi bearish")
            lines.append("      → Sentimen berita cenderung negatif")
            lines.append("      → Ada potensi harga turun dalam jangka pendek")
            lines.append("")
            lines.append("   ⚠️  Penting untuk diingat:")
            lines.append("      → Short selling memiliki risiko unlimited loss")
            lines.append("      → Stop-loss WAJIB digunakan")
            lines.append("      → Pertimbangkan untuk tidak trading jika tidak yakin")
        
        else:  # HOLD
            lines.append("   💡 Mengapa bot TIDAK merekomendasikan trade?")
            lines.append("      → Indikator teknikal tidak menunjukkan sinyal kuat")
            lines.append("      → Market mungkin sedang consolidation (sideways)")
            lines.append("      → Lebih baik menunggu signal yang lebih jelas")
            lines.append("")
            lines.append("   ⚠️  Penting untuk diingat:")
            lines.append("      → Tidak trading juga merupakan keputusan yang baik")
            lines.append("      → Kesabaran adalah kunci dalam trading")
            lines.append("      → Jangan FOMO (Fear Of Missing Out)")
        
        lines.append("")
        lines.append("   📖 Istilah penting:")
        lines.append("      • RSI = Relative Strength Index (momentum indicator)")
        lines.append("      • MACD = Moving Average Convergence Divergence (trend indicator)")
        lines.append("      • EMA = Exponential Moving Average (trend following)")
        lines.append("      • Bollinger Bands = Volatility indicator")
        lines.append("      • ATR = Average True Range (volatility measurement)")
        
        return "\n".join(lines)

    def generate_simple_explanation(self, signal: Dict) -> str:
        """
        Generate penjelasan sederhana (1 paragraf)
        
        Args:
            signal: Output dari SignalGenerator
        
        Returns:
            Penjelasan sederhana
        """
        symbol = signal["symbol"]
        action = signal["signal"]
        confidence = signal["confidence"]
        
        if action in ["STRONG_BUY", "BUY"]:
            return (
                f"Bot merekomendasikan BELI {symbol} dengan confidence {confidence:.1f}%. "
                f"Indikator teknikal dan sentimen berita menunjukkan kondisi bullish. "
                f"Risk management aktif dengan stop-loss dan take-profit otomatis."
            )
        elif action in ["STRONG_SELL", "SELL"]:
            return (
                f"Bot merekomendasikan JUAL {symbol} dengan confidence {confidence:.1f}%. "
                f"Indikator teknikal dan sentimen berita menunjukkan kondisi bearish. "
                f"Risk management aktif dengan stop-loss dan take-profit otomatis."
            )
        else:
            return (
                f"Bot TIDAK merekomendasikan trade untuk {symbol}. "
                f"Indikator teknikal tidak menunjukkan sinyal kuat. "
                f"Lebih baik menunggu kondisi market yang lebih jelas."
            )

    def generate_reason_summary(self, signal: Dict) -> str:
        """
        Generate ringkasan alasan dalam format bullet points
        
        Args:
            signal: Output dari SignalGenerator
        
        Returns:
            Ringkasan alasan
        """
        reasons = signal.get("reasons", [])
        
        if not reasons:
            return "Tidak ada alasan spesifik"
        
        lines = ["📋 Alasan utama:"]
        for i, reason in enumerate(reasons, 1):
            lines.append(f"   {i}. {reason}")
        
        return "\n".join(lines)
