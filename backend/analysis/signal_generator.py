"""
Signal Generator
Menggabungkan analisis teknikal + sentimen menjadi trading signal
dengan confidence score dan penjelasan yang mudah dipahami
"""
from typing import Dict, List, Optional
from datetime import datetime
from loguru import logger


class SignalGenerator:
    """Menghasilkan trading signal dari analisis teknikal dan sentimen"""

    # Bobot relatif setiap komponen dalam keputusan final
    WEIGHTS = {
        "rsi": 0.15,
        "macd": 0.25,
        "ema": 0.25,
        "bollinger": 0.15,
        "volume": 0.10,
        "sentiment": 0.10,
    }

    # Threshold confidence untuk eksekusi
    THRESHOLDS = {
        "strong_buy": 75,
        "buy": 55,
        "neutral": 45,
        "sell": 55,
        "strong_sell": 75,
    }

    def generate_signal(
        self,
        symbol: str,
        timeframe: str,
        technical_analysis: Dict,
        sentiment_analysis: Dict,
    ) -> Dict:
        """
        Menghasilkan trading signal lengkap
        
        Args:
            symbol: Trading pair (misal: "BTC/USDT")
            timeframe: Timeframe analisis (misal: "1h")
            technical_analysis: Output dari TechnicalAnalyzer.calculate_all()
            sentiment_analysis: Output dari SentimentAnalyzer.analyze_news_batch()
            
        Returns:
            Dict lengkap dengan signal, confidence, reasons, dan suggested actions
        """
        interpretation = technical_analysis["interpretation"]
        indicators = technical_analysis["indicators"]

        # === 1. Hitung Technical Score ===
        tech_scores = {
            "rsi": interpretation["rsi"]["score"],
            "macd": interpretation["macd"]["score"],
            "ema": interpretation["ema"]["score"],
            "bollinger": interpretation["bollinger"]["score"],
            "volume": interpretation["volume"]["score"],
        }

        # Weighted average technical score
        weighted_tech_score = sum(
            tech_scores[k] * self.WEIGHTS[k]
            for k in ["rsi", "macd", "ema", "bollinger", "volume"]
        )

        # === 2. Hitung Sentiment Score ===
        sentiment_score = sentiment_analysis["overall_score"]  # -1 sampai +1
        sentiment_impact = self._get_sentiment_impact(sentiment_score)
        
        # Konversi sentiment ke skala -100 sampai +100
        sentiment_scaled = sentiment_score * 100 * sentiment_impact["weight"]

        # === 3. Gabungkan jadi Final Score ===
        # Technical = 90% bobot, Sentiment = 10% bobot
        final_score = (weighted_tech_score * 0.9) + (sentiment_scaled * 0.1)

        # === 4. Tentukan Signal ===
        signal, confidence = self._score_to_signal(final_score)

        # === 5. Kumpulkan Alasan ===
        reasons = self._collect_reasons(interpretation, sentiment_analysis)

        # === 6. Hitung Suggested Actions (Entry, SL, TP) ===
        suggested_actions = self._calculate_suggested_actions(
            signal=signal,
            price=technical_analysis["latest_price"],
            atr=indicators["atr"]["value"],
            confidence=confidence,
        )

        # === 7. Bangun Output Lengkap ===
        result = {
            "symbol": symbol,
            "timeframe": timeframe,
            "timestamp": datetime.now().isoformat(),
            "signal": signal,
            "confidence": round(confidence, 1),
            "final_score": round(final_score, 2),
            "latest_price": technical_analysis["latest_price"],
            "technical_score": round(weighted_tech_score, 2),
            "sentiment_score": round(sentiment_score, 3),
            "sentiment_label": sentiment_analysis["overall_label"],
            "component_scores": {
                "rsi": {
                    "score": tech_scores["rsi"],
                    "signal": interpretation["rsi"]["signal"],
                    "weight": self.WEIGHTS["rsi"],
                },
                "macd": {
                    "score": tech_scores["macd"],
                    "signal": interpretation["macd"]["signal"],
                    "weight": self.WEIGHTS["macd"],
                },
                "ema": {
                    "score": tech_scores["ema"],
                    "signal": interpretation["ema"]["signal"],
                    "weight": self.WEIGHTS["ema"],
                },
                "bollinger": {
                    "score": tech_scores["bollinger"],
                    "signal": interpretation["bollinger"]["signal"],
                    "weight": self.WEIGHTS["bollinger"],
                },
                "volume": {
                    "score": tech_scores["volume"],
                    "signal": interpretation["volume"]["signal"],
                    "weight": self.WEIGHTS["volume"],
                },
                "sentiment": {
                    "score": round(sentiment_score, 3),
                    "label": sentiment_analysis["overall_label"],
                    "impact": sentiment_impact["impact"],
                    "weight": self.WEIGHTS["sentiment"],
                },
            },
            "reasons": reasons,
            "suggested_actions": suggested_actions,
            "risk_warning": self._generate_risk_warning(signal, confidence),
        }

        return result

    def _score_to_signal(self, score: float) -> tuple:
        """
        Konversi final score (-100 sampai +100) ke signal + confidence
        
        Returns:
            (signal: str, confidence: float 0-100)
        """
        abs_score = abs(score)

        if score >= 60:
            return "STRONG_BUY", min(abs_score, 100)
        elif score >= 30:
            return "BUY", min(abs_score, 100)
        elif score <= -60:
            return "STRONG_SELL", min(abs_score, 100)
        elif score <= -30:
            return "SELL", min(abs_score, 100)
        else:
            return "NEUTRAL", 100 - abs_score  # Confidence tinggi untuk HOLD

    def _get_sentiment_impact(self, score: float) -> Dict:
        """Determinasi dampak sentimen"""
        abs_score = abs(score)
        if abs_score < 0.15:
            return {"impact": "LOW", "weight": 0.1}
        elif abs_score < 0.4:
            return {"impact": "MODERATE", "weight": 0.25}
        elif abs_score < 0.7:
            return {"impact": "HIGH", "weight": 0.4}
        else:
            return {"impact": "VERY_HIGH", "weight": 0.5}

    def _collect_reasons(
        self, interpretation: Dict, sentiment_analysis: Dict
    ) -> List[str]:
        """Mengumpulkan alasan utama untuk signal"""
        reasons = []

        # Ambil alasan dari setiap indikator yang punya skor signifikan
        for indicator_name in ["rsi", "macd", "ema", "bollinger", "volume"]:
            data = interpretation.get(indicator_name, {})
            score = data.get("score", 0)
            if abs(score) >= 40:  # Hanya ambil yang signifikan
                reasons.append(f"[{indicator_name.upper()}] {data['reason']}")

        # Tambahkan alasan sentimen jika signifikan
        if sentiment_analysis["total_articles"] > 0:
            overall = sentiment_analysis["overall_label"]
            pos = sentiment_analysis["positive_count"]
            neg = sentiment_analysis["negative_count"]
            total = sentiment_analysis["total_articles"]
            reasons.append(
                f"[SENTIMENT] {overall} → {pos} positif, {neg} negatif "
                f"dari {total} artikel berita"
            )

        return reasons[:7]  # Maksimal 7 alasan agar tidak overwhelming

    def _calculate_suggested_actions(
        self, signal: str, price: float, atr: float, confidence: float
    ) -> Dict:
        """
        Menghitung suggested entry, stop-loss, dan take-profit
        Menggunakan ATR untuk menentukan jarak SL/TP yang realistis
        """
        if signal == "NEUTRAL":
            return {
                "action": "HOLD",
                "reason": "Tidak ada sinyal kuat. Tunggu konfirmasi.",
                "entry": None,
                "stop_loss": None,
                "take_profit": None,
                "position_size_percent": 0,
            }

        # Risk/Reward ratio target
        rr_ratio = 2.0  # Target profit 2x jarak stop-loss

        # Position sizing berdasarkan confidence
        # Max 2% risiko per trade (aturan umum)
        if confidence >= 75:
            position_size_percent = 10  # 10% dari portfolio
        elif confidence >= 60:
            position_size_percent = 5
        else:
            position_size_percent = 2

        # Hitung SL dan TP berdasarkan ATR
        sl_distance = atr * 2  # 2x ATR untuk stop-loss
        tp_distance = sl_distance * rr_ratio  # 2x jarak SL untuk TP

        if signal in ["BUY", "STRONG_BUY"]:
            entry = price
            stop_loss = price - sl_distance
            take_profit = price + tp_distance
            action = "OPEN_LONG"
        else:  # SELL, STRONG_SELL
            entry = price
            stop_loss = price + sl_distance
            take_profit = price - tp_distance
            action = "OPEN_SHORT"

        return {
            "action": action,
            "entry": round(entry, 4),
            "stop_loss": round(stop_loss, 4),
            "take_profit": round(take_profit, 4),
            "risk_reward_ratio": rr_ratio,
            "position_size_percent": position_size_percent,
            "max_risk_percent": 2.0,  # Max 2% dari portfolio
            "sl_distance_percent": round((sl_distance / price) * 100, 2),
            "tp_distance_percent": round((tp_distance / price) * 100, 2),
        }

    def _generate_risk_warning(self, signal: str, confidence: float) -> str:
        """Generate peringatan risiko berdasarkan kondisi"""
        warnings = []

        if confidence < 60:
            warnings.append("Confidence rendah → pertimbangkan untuk tidak entry")

        if signal in ["STRONG_BUY", "STRONG_SELL"]:
            warnings.append(
                "Sinyal sangat kuat → pastikan bukan fake breakout/pump & dump"
            )

        warnings.append(
            "⚠️  Ini adalah analisis otomatis, BUKAN saran keuangan. "
            "Selalu lakukan riset mandiri (DYOR)."
        )

        return " | ".join(warnings)
