"""
Pump & Dump Detector
Deteksi pump & dump dari social media dan market data
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from loguru import logger
from collections import Counter


class PumpDumpDetector:
    """
    Pump & dump detection system
    
    Features:
    - Social media hype detection
    - Volume anomaly detection
    - Price spike detection
    - Coordinated activity detection
    - Risk scoring
    """
    
    def __init__(self):
        """Initialize pump & dump detector"""
        self.alerts = []
        
        logger.info("🚨 Pump & Dump Detector initialized")
    
    def analyze_social_media_hype(
        self,
        tweets: List[Dict],
        time_window_minutes: int = 60
    ) -> Dict:
        """
        Analyze social media for pump indicators
        
        Args:
            tweets: List of tweets with sentiment
            time_window_minutes: Time window for analysis
            
        Returns:
            Hype analysis results
        """
        if not tweets:
            return {
                "hype_score": 0.0,
                "hype_level": "LOW",
                "indicators": {},
                "risk": "LOW"
            }
        
        # Filter recent tweets
        now = datetime.now()
        recent_tweets = []
        
        for tweet in tweets:
            created_at = tweet.get("created_at")
            if created_at:
                try:
                    tweet_time = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                    if (now - tweet_time).total_seconds() < time_window_minutes * 60:
                        recent_tweets.append(tweet)
                except:
                    pass
        
        if not recent_tweets:
            return {
                "hype_score": 0.0,
                "hype_level": "LOW",
                "indicators": {},
                "risk": "LOW"
            }
        
        # Analyze indicators
        indicators = {}
        
        # 1. Sentiment spike
        sentiments = [t["sentiment"]["sentiment_score"] for t in recent_tweets if "sentiment" in t]
        if sentiments:
            avg_sentiment = sum(sentiments) / len(sentiments)
            positive_ratio = sum(1 for s in sentiments if s > 0.3) / len(sentiments)
            indicators["sentiment_spike"] = {
                "avg_sentiment": avg_sentiment,
                "positive_ratio": positive_ratio,
                "score": max(0, avg_sentiment * positive_ratio * 100)
            }
        
        # 2. Engagement spike
        engagements = [
            t.get("metrics", {}).get("like_count", 0) +
            t.get("metrics", {}).get("retweet_count", 0) * 3
            for t in recent_tweets
        ]
        if engagements:
            avg_engagement = sum(engagements) / len(engagements)
            high_engagement_count = sum(1 for e in engagements if e > 100)
            indicators["engagement_spike"] = {
                "avg_engagement": avg_engagement,
                "high_engagement_count": high_engagement_count,
                "score": min(100, avg_engagement / 10)
            }
        
        # 3. Hype keywords
        hype_keywords = [
            "moon", "pump", "100x", "gem", "buy now", "rocket",
            "bullish", "breakout", "skyrocket"
        ]
        
        keyword_count = 0
        for tweet in recent_tweets:
            text = tweet.get("text", "").lower()
            keyword_count += sum(1 for kw in hype_keywords if kw in text)
        
        indicators["hype_keywords"] = {
            "count": keyword_count,
            "ratio": keyword_count / len(recent_tweets),
            "score": min(100, keyword_count * 5)
        }
        
        # 4. Coordinated posting
        timestamps = []
        for tweet in recent_tweets:
            created_at = tweet.get("created_at")
            if created_at:
                try:
                    timestamps.append(datetime.fromisoformat(created_at.replace("Z", "+00:00")))
                except:
                    pass
        
        if len(timestamps) > 1:
            timestamps.sort()
            time_diffs = [(timestamps[i+1] - timestamps[i]).total_seconds() 
                         for i in range(len(timestamps)-1)]
            avg_time_diff = sum(time_diffs) / len(time_diffs) if time_diffs else 0
            
            # Coordinated if posts are very close together
            coordinated_score = max(0, 100 - avg_time_diff) if avg_time_diff < 60 else 0
            
            indicators["coordinated_activity"] = {
                "avg_time_diff_seconds": avg_time_diff,
                "score": coordinated_score
            }
        
        # Calculate overall hype score
        scores = [ind["score"] for ind in indicators.values()]
        hype_score = sum(scores) / len(scores) if scores else 0
        
        # Determine hype level
        if hype_score > 70:
            hype_level = "VERY_HIGH"
            risk = "HIGH"
        elif hype_score > 50:
            hype_level = "HIGH"
            risk = "HIGH"
        elif hype_score > 30:
            hype_level = "MODERATE"
            risk = "MEDIUM"
        else:
            hype_level = "LOW"
            risk = "LOW"
        
        return {
            "hype_score": hype_score,
            "hype_level": hype_level,
            "indicators": indicators,
            "risk": risk,
            "tweet_count": len(recent_tweets)
        }
    
    def analyze_volume_anomaly(
        self,
        candles: pd.DataFrame,
        lookback_period: int = 20,
        threshold_multiplier: float = 3.0
    ) -> Dict:
        """
        Detect volume anomalies
        
        Args:
            candles: OHLCV data
            lookback_period: Period for average calculation
            threshold_multiplier: Multiplier for anomaly detection
            
        Returns:
            Volume anomaly analysis
        """
        if len(candles) < lookback_period:
            return {
                "anomaly_detected": False,
                "volume_ratio": 0.0,
                "risk": "LOW"
            }
        
        # Calculate average volume
        avg_volume = candles["volume"].rolling(window=lookback_period).mean().iloc[-1]
        current_volume = candles["volume"].iloc[-1]
        
        # Calculate volume ratio
        volume_ratio = current_volume / avg_volume if avg_volume > 0 else 0
        
        # Detect anomaly
        anomaly_detected = volume_ratio > threshold_multiplier
        
        # Determine risk
        if volume_ratio > 5.0:
            risk = "VERY_HIGH"
        elif volume_ratio > 3.0:
            risk = "HIGH"
        elif volume_ratio > 2.0:
            risk = "MEDIUM"
        else:
            risk = "LOW"
        
        return {
            "anomaly_detected": anomaly_detected,
            "volume_ratio": volume_ratio,
            "current_volume": current_volume,
            "avg_volume": avg_volume,
            "risk": risk
        }
    
    def analyze_price_spike(
        self,
        candles: pd.DataFrame,
        lookback_period: int = 20,
        threshold_percent: float = 10.0
    ) -> Dict:
        """
        Detect price spikes
        
        Args:
            candles: OHLCV data
            lookback_period: Period for average calculation
            threshold_percent: Threshold for spike detection
            
        Returns:
            Price spike analysis
        """
        if len(candles) < lookback_period:
            return {
                "spike_detected": False,
                "price_change_percent": 0.0,
                "risk": "LOW"
            }
        
        # Calculate price change
        past_price = candles["close"].iloc[-lookback_period]
        current_price = candles["close"].iloc[-1]
        price_change_percent = ((current_price - past_price) / past_price) * 100
        
        # Detect spike
        spike_detected = abs(price_change_percent) > threshold_percent
        
        # Determine risk
        if abs(price_change_percent) > 30:
            risk = "VERY_HIGH"
        elif abs(price_change_percent) > 15:
            risk = "HIGH"
        elif abs(price_change_percent) > 10:
            risk = "MEDIUM"
        else:
            risk = "LOW"
        
        return {
            "spike_detected": spike_detected,
            "price_change_percent": price_change_percent,
            "current_price": current_price,
            "past_price": past_price,
            "risk": risk
        }
    
    def detect_pump_and_dump(
        self,
        candles: pd.DataFrame,
        tweets: List[Dict] = None,
        time_window_minutes: int = 60
    ) -> Dict:
        """
        Comprehensive pump & dump detection
        
        Args:
            candles: OHLCV data
            tweets: Social media data (optional)
            time_window_minutes: Time window for analysis
            
        Returns:
            Pump & dump detection results
        """
        logger.info("🔍 Analyzing for pump & dump patterns...")
        
        # Analyze volume
        volume_analysis = self.analyze_volume_anomaly(candles)
        
        # Analyze price
        price_analysis = self.analyze_price_spike(candles)
        
        # Analyze social media
        hype_analysis = {"hype_score": 0, "risk": "LOW"}
        if tweets:
            hype_analysis = self.analyze_social_media_hype(tweets, time_window_minutes)
        
        # Calculate overall risk score
        risk_scores = {
            "LOW": 0,
            "MEDIUM": 1,
            "HIGH": 2,
            "VERY_HIGH": 3
        }
        
        volume_risk = risk_scores.get(volume_analysis["risk"], 0)
        price_risk = risk_scores.get(price_analysis["risk"], 0)
        hype_risk = risk_scores.get(hype_analysis["risk"], 0)
        
        overall_risk_score = (volume_risk + price_risk + hype_risk) / 3
        
        # Determine overall risk
        if overall_risk_score > 2:
            overall_risk = "VERY_HIGH"
            pump_dump_detected = True
        elif overall_risk_score > 1.5:
            overall_risk = "HIGH"
            pump_dump_detected = True
        elif overall_risk_score > 1:
            overall_risk = "MEDIUM"
            pump_dump_detected = volume_analysis["anomaly_detected"] and price_analysis["spike_detected"]
        else:
            overall_risk = "LOW"
            pump_dump_detected = False
        
        result = {
            "pump_dump_detected": pump_dump_detected,
            "overall_risk": overall_risk,
            "risk_score": overall_risk_score,
            "volume_analysis": volume_analysis,
            "price_analysis": price_analysis,
            "hype_analysis": hype_analysis,
            "recommendation": self._get_recommendation(overall_risk, pump_dump_detected)
        }
        
        if pump_dump_detected:
            logger.warning(f"🚨 PUMP & DUMP DETECTED! Risk: {overall_risk}")
            self.alerts.append({
                "timestamp": datetime.now().isoformat(),
                "risk": overall_risk,
                "details": result
            })
        
        return result
    
    def _get_recommendation(self, risk: str, pump_dump_detected: bool) -> str:
        """Get trading recommendation based on analysis"""
        if pump_dump_detected and risk in ["HIGH", "VERY_HIGH"]:
            return "⚠️ AVOID TRADING - High probability of pump & dump. Wait for stabilization."
        elif risk == "HIGH":
            return "⚠️ CAUTION - Elevated risk detected. Reduce position size or wait."
        elif risk == "MEDIUM":
            return "⚡ MODERATE RISK - Proceed with caution. Use tight stop-loss."
        else:
            return "✅ LOW RISK - Normal market conditions. Standard risk management applies."
    
    def get_alerts(self, hours_back: int = 24) -> List[Dict]:
        """
        Get recent alerts
        
        Args:
            hours_back: How many hours back to retrieve
            
        Returns:
            List of alerts
        """
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        recent_alerts = []
        for alert in self.alerts:
            alert_time = datetime.fromisoformat(alert["timestamp"])
            if alert_time > cutoff_time:
                recent_alerts.append(alert)
        
        return recent_alerts


# === USAGE EXAMPLE ===

def example_usage():
    """Example how to use PumpDumpDetector"""
    import pandas as pd
    import numpy as np
    
    # Create sample data
    dates = pd.date_range(end=datetime.now(), periods=100, freq='h')
    
    # Simulate pump & dump pattern
    prices = []
    volumes = []
    
    base_price = 50000
    base_volume = 1000
    
    for i in range(100):
        if i < 80:
            # Normal market
            price = base_price + np.random.normal(0, 100)
            volume = base_volume + np.random.normal(0, 100)
        elif i < 90:
            # Pump phase
            price = base_price * (1 + (i - 80) * 0.05)  # 5% increase per candle
            volume = base_volume * (1 + (i - 80) * 0.5)  # Volume spike
        else:
            # Dump phase
            price = base_price * 1.5 * (1 - (i - 90) * 0.08)  # 8% decrease per candle
            volume = base_volume * 3  # High volume
        
        prices.append(price)
        volumes.append(volume)
    
    candles = pd.DataFrame({
        "timestamp": dates,
        "open": prices,
        "high": [p * 1.01 for p in prices],
        "low": [p * 0.99 for p in prices],
        "close": prices,
        "volume": volumes
    })
    
    # Detect pump & dump
    detector = PumpDumpDetector()
    result = detector.detect_pump_and_dump(candles)
    
    print("\n🚨 Pump & Dump Detection:")
    print(f"   Detected: {result['pump_dump_detected']}")
    print(f"   Overall Risk: {result['overall_risk']}")
    print(f"   Risk Score: {result['risk_score']:.2f}")
    print(f"\n   Volume Analysis:")
    print(f"     Anomaly: {result['volume_analysis']['anomaly_detected']}")
    print(f"     Volume Ratio: {result['volume_analysis']['volume_ratio']:.2f}x")
    print(f"\n   Price Analysis:")
    print(f"     Spike: {result['price_analysis']['spike_detected']}")
    print(f"     Price Change: {result['price_analysis']['price_change_percent']:+.2f}%")
    print(f"\n   Recommendation: {result['recommendation']}")


if __name__ == "__main__":
    example_usage()
