"""
Pump & Dump Detector
Mendeteksi manipulasi market dari kombinasi price, volume, dan social signals
"""
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from loguru import logger
from sklearn.ensemble import IsolationForest
from scipy import stats

from .config import PUMP_DETECTION


class PumpDumpDetector:
    """Deteksi pump & dump menggunakan anomaly detection"""

    def __init__(self):
        self.params = PUMP_DETECTION
        self.anomaly_model = IsolationForest(
            contamination=0.05,  # 5% dianggap anomali
            random_state=42,
        )

    def analyze_symbol(
        self,
        symbol: str,
        price_data: Dict,
        volume_data: List[float],
        social_mentions: List[Dict] = None,
    ) -> Dict:
        """
        Analisis satu simbol untuk deteksi pump/dump
        
        Args:
            symbol: Trading pair
            price_data: {"current": float, "1h_ago": float, "24h_ago": float, "high_24h": float, "low_24h": float}
            volume_data: List volume per jam (24 values)
            social_mentions: List social posts tentang simbol ini
            
        Returns:
            Dict dengan pump_score, dump_score, risk_level, signals
        """
        signals = []
        pump_score = 0.0
        dump_score = 0.0

        # === 1. PRICE SPIKE DETECTION ===
        price_change_1h = (
            (price_data["current"] - price_data["1h_ago"]) / price_data["1h_ago"] * 100
        )
        price_change_24h = (
            (price_data["current"] - price_data["24h_ago"]) / price_data["24h_ago"] * 100
        )

        if price_change_1h > self.params["price_spike_1h_threshold"]:
            pump_score += 30
            signals.append({
                "type": "PRICE_SPIKE_1H",
                "severity": "HIGH",
                "message": f"Price naik {price_change_1h:.1f}% dalam 1 jam (threshold: {self.params['price_spike_1h_threshold']}%)",
            })

        if price_change_24h > self.params["price_spike_24h_threshold"]:
            pump_score += 25
            signals.append({
                "type": "PRICE_SPIKE_24H",
                "severity": "HIGH",
                "message": f"Price naik {price_change_24h:.1f}% dalam 24 jam",
            })

        if price_change_1h < -self.params["price_spike_1h_threshold"]:
            dump_score += 30
            signals.append({
                "type": "PRICE_DROP_1H",
                "severity": "HIGH",
                "message": f"Price turun {abs(price_change_1h):.1f}% dalam 1 jam",
            })

        # === 2. VOLUME ANOMALY DETECTION ===
        if len(volume_data) >= 12:
            recent_volume = np.mean(volume_data[-3:])  # 3 jam terakhir
            avg_volume = np.mean(volume_data[:-3])  # sisanya

            if avg_volume > 0:
                volume_ratio = recent_volume / avg_volume

                if volume_ratio > self.params["volume_spike_threshold"]:
                    if price_change_1h > 5:  # Volume spike + price naik
                        pump_score += 25
                        signals.append({
                            "type": "VOLUME_PUMP",
                            "severity": "HIGH",
                            "message": f"Volume {volume_ratio:.1f}x rata-rata + price naik → POTENSI PUMP",
                        })
                    elif price_change_1h < -5:  # Volume spike + price turun
                        dump_score += 25
                        signals.append({
                            "type": "VOLUME_DUMP",
                            "severity": "HIGH",
                            "message": f"Volume {volume_ratio:.1f}x rata-rata + price turun → POTENSI DUMP",
                        })
                    else:
                        signals.append({
                            "type": "VOLUME_ANOMALY",
                            "severity": "MEDIUM",
                            "message": f"Volume spike {volume_ratio:.1f}x tanpa arah jelas",
                        })

        # === 3. SOCIAL MEDIA ANOMALY ===
        if social_mentions:
            mention_count = len(social_mentions)
            
            # Hitung engagement score
            total_engagement = sum(
                m.get("engagement_score", 0) or m.get("score", 0) or 0
                for m in social_mentions
            )

            if mention_count > self.params["min_social_mentions"]:
                if price_change_1h > 5:
                    pump_score += 20
                    signals.append({
                        "type": "SOCIAL_PUMP",
                        "severity": "HIGH",
                        "message": f"{mention_count} social mentions + price naik → FOMO detected",
                    })
                elif price_change_1h < -5:
                    dump_score += 20
                    signals.append({
                        "type": "SOCIAL_DUMP",
                        "severity": "HIGH",
                        "message": f"{mention_count} social mentions + price turun → PANIC detected",
                    })

            # Deteksi coordinated pump (banyak akun post hal serupa)
            if self._detect_coordinated_activity(social_mentions):
                pump_score += 15
                signals.append({
                    "type": "COORDINATED_ACTIVITY",
                    "severity": "HIGH",
                    "message": "Aktivitas terkoordinasi terdeteksi (potensi pump group)",
                })

        # === 4. STATISTICAL ANOMALY (Z-Score) ===
        if len(volume_data) >= 24:
            z_score = stats.zscore(volume_data)[-1]
            if abs(z_score) > 3:
                signals.append({
                    "type": "STATISTICAL_ANOMALY",
                    "severity": "MEDIUM",
                    "message": f"Z-score volume: {z_score:.2f} (statistical anomaly)",
                })
                if z_score > 3 and price_change_1h > 0:
                    pump_score += 10
                elif z_score > 3 and price_change_1h < 0:
                    dump_score += 10

        # === NORMALIZE SCORES ===
        pump_score = min(pump_score, 100)
        dump_score = min(dump_score, 100)

        # === DETERMINE RISK LEVEL ===
        max_score = max(pump_score, dump_score)
        if max_score >= 70:
            risk_level = "CRITICAL"
        elif max_score >= 50:
            risk_level = "HIGH"
        elif max_score >= 30:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        # === DETERMINE PATTERN ===
        if pump_score > 50 and dump_score < 30:
            pattern = "PUMP_DETECTED"
        elif dump_score > 50 and pump_score < 30:
            pattern = "DUMP_DETECTED"
        elif pump_score > 40 and dump_score > 40:
            pattern = "PUMP_AND_DUMP"
        else:
            pattern = "NORMAL"

        return {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "pump_score": round(pump_score, 1),
            "dump_score": round(dump_score, 1),
            "risk_level": risk_level,
            "pattern": pattern,
            "signals": signals,
            "metrics": {
                "price_change_1h": round(price_change_1h, 2),
                "price_change_24h": round(price_change_24h, 2),
                "social_mentions": len(social_mentions) if social_mentions else 0,
            },
            "recommendation": self._get_recommendation(pattern, risk_level),
        }

    def _detect_coordinated_activity(self, mentions: List[Dict]) -> bool:
        """
        Deteksi aktivitas terkoordinasi
        (banyak post dengan konten serupa dalam waktu singkat)
        """
        if len(mentions) < 10:
            return False

        # Hitung kemiripan teks sederhana (Jaccard similarity)
        texts = [m.get("text", "").lower().split() for m in mentions]
        
        # Cari cluster post yang mirip
        similar_count = 0
        for i in range(len(texts)):
            for j in range(i+1, min(i+5, len(texts))):
                set_i, set_j = set(texts[i]), set(texts[j])
                if len(set_i) > 5 and len(set_j) > 5:
                    intersection = len(set_i & set_j)
                    union = len(set_i | set_j)
                    similarity = intersection / union if union > 0 else 0
                    if similarity > 0.5:
                        similar_count += 1

        # Jika banyak post yang mirip → coordinated
        return similar_count > len(mentions) * 0.3

    def _get_recommendation(self, pattern: str, risk_level: str) -> str:
        """Generate rekomendasi berdasarkan pattern"""
        if pattern == "PUMP_DETECTED":
            if risk_level == "CRITICAL":
                return (
                    "🚨 CRITICAL PUMP DETECTED! Jangan FOMO! "
                    "Kemungkinan besar ini pump & dump. "
                    "Tunggu koreksi atau hindari sama sekali."
                )
            return (
                "⚠️ Pump terdeteksi. Hati-hati entry di harga tinggi. "
                "Tunggu koreksi atau gunakan stop-loss ketat."
            )
        elif pattern == "DUMP_DETECTED":
            if risk_level == "CRITICAL":
                return (
                    "🚨 CRITICAL DUMP DETECTED! Jangan catch the falling knife! "
                    "Tunggu stabilisasi sebelum entry."
                )
            return (
                "⚠️ Dump terdeteksi. Hindari entry sampai ada konfirmasi reversal."
            )
        elif pattern == "PUMP_AND_DUMP":
            return (
                "🚨 POLA PUMP & DUMP TERDETEKSI! "
                "Sangat berisiko. JANGAN TRADE simbol ini sampai pola selesai."
            )
        else:
            return "✅ Tidak ada anomali terdeteksi. Pola normal."

    def batch_analyze(
        self,
        symbols_data: List[Dict],
    ) -> List[Dict]:
        """Analisis batch simbol"""
        results = []
        for data in symbols_data:
            try:
                result = self.analyze_symbol(
                    symbol=data["symbol"],
                    price_data=data["price_data"],
                    volume_data=data.get("volume_data", []),
                    social_mentions=data.get("social_mentions"),
                )
                results.append(result)
            except Exception as e:
                logger.error(f"Error analyzing {data.get('symbol')}: {e}")

        # Sort by risk level
        risk_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        results.sort(key=lambda x: risk_order.get(x["risk_level"], 4))

        return results
