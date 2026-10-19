"""
Explanation Generator
Mengubah data signal teknis menjadi narasi edukatif yang mudah dipahami pemula
"""
from typing import Dict, List
from datetime import datetime
from .trading_dictionary import TradingDictionary


class ExplanationGenerator:
    """Menghasilkan penjelasan naratif dari data trading"""

    def __init__(self):
        self.dictionary = TradingDictionary()

    def generate_trade_explanation(self, signal: Dict) -> str:
        """
        Menghasilkan penjelasan lengkap untuk satu keputusan trading
        Format: Narasi yang ramah pemula dengan analogi
        """
        symbol = signal["symbol"]
        action = signal["signal"]
        confidence = signal["confidence"]
        price = signal["latest_price"]
        reasons = signal["reasons"]
        actions = signal["suggested_actions"]

        # === 1. Opening Statement ===
        opening = self._generate_opening(symbol, action, confidence)

        # === 2. Market Context ===
        context = self._generate_market_context(signal)

        # === 3. Reason Breakdown ===
        reason_explanation = self._explain_reasons(signal["component_scores"])

        # === 4. Action Plan ===
        action_plan = self._generate_action_plan(actions, symbol)

        # === 5. Risk Warning ===
        risk_warning = self._generate_risk_education(confidence)

        # === 6. Learning Point ===
        learning_point = self._generate_learning_point(signal)

        # Gabungkan semua
        full_explanation = f"""
{opening}

📊 **KONTEKS PASAR**
{context}

🔍 **ANALISIS DETAIL**
{reason_explanation}

💡 **RENCANA AKSI**
{action_plan}

⚠️ **EDUKASI RISIKO**
{risk_warning}

📚 **POIN PEMBELAJARAN**
{learning_point}
"""
        return full_explanation.strip()

    def _generate_opening(self, symbol: str, action: str, confidence: float) -> str:
        """Generate pembuka yang menarik"""
        action_emoji = {
            "STRONG_BUY": "🟢🟢",
            "BUY": "🟢",
            "NEUTRAL": "⚪",
            "SELL": "🔴",
            "STRONG_SELL": "🔴🔴",
        }.get(action, "⚪")

        action_text = {
            "STRONG_BUY": "sinyal BELI KUAT",
            "BUY": "sinyal BELI",
            "NEUTRAL": "sinyal NETRAL (tahan dulu)",
            "SELL": "sinyal JUAL",
            "STRONG_SELL": "sinyal JUAL KUAT",
        }.get(action, "sinyal tidak jelas")

        confidence_level = (
            "sangat yakin" if confidence >= 75 
            else "cukup yakin" if confidence >= 60 
            else "ragu-ragu"
        )

        return f"""
{action_emoji} **{symbol}**: AI mendeteksi {action_text} dengan tingkat keyakinan {confidence:.1f}% ({confidence_level}).

Sebelum mengambil keputusan, mari kita pahami **MENGAPA** AI memberikan sinyal ini. Penjelasan di bawah akan membantu Anda belajar, bukan hanya mengikuti secara buta."""

    def _generate_market_context(self, signal: Dict) -> str:
        """Generate konteks pasar"""
        price = signal["latest_price"]
        sentiment = signal["sentiment_label"]
        sentiment_score = signal["sentiment_score"]
        tech_score = signal["technical_score"]

        sentiment_emoji = {
            "POSITIVE": "😊",
            "NEGATIVE": "😟",
            "NEUTRAL": "😐",
        }.get(sentiment, "😐")

        # Tentukan kondisi pasar
        if tech_score > 50 and sentiment_score > 0.2:
            market_condition = "🌞 **Pasar sedang optimis** - indikator teknikal dan sentimen berita sama-sama positif. Ini kondisi ideal untuk posisi long."
        elif tech_score < -50 and sentiment_score < -0.2:
            market_condition = "🌧️ **Pasar sedang pesimis** - indikator teknikal dan sentimen berita sama-sama negatif. Hati-hati dengan posisi long."
        elif abs(tech_score) < 30 and abs(sentiment_score) < 0.2:
            market_condition = "☁️ **Pasar sedang bingung** - tidak ada arah yang jelas. Lebih baik tunggu konfirmasi."
        else:
            market_condition = "🌤️ **Pasar sedang transisi** - ada perbedaan antara teknikal dan sentimen. Perlu analisis lebih hati-hati."

        return f"""
💰 Harga saat ini: **${price:,.2f}**

{sentiment_emoji} Sentimen berita: **{sentiment}** (skor: {sentiment_score:+.3f})
📈 Skor teknikal: **{tech_score:+.2f}** (skala -100 sampai +100)

{market_condition}"""

    def _explain_reasons(self, component_scores: Dict) -> str:
        """Menjelaskan setiap komponen dengan bahasa sederhana"""
        explanations = []

        for indicator, data in component_scores.items():
            score = data["score"]
            signal = data["signal"]
            weight = data["weight"]

            # Skip jika skor tidak signifikan
            if abs(score) < 20 and indicator != "sentiment":
                continue

            # Tentukan emoji dan penjelasan
            if score > 50:
                emoji = "🟢"
                strength = "sangat mendukung"
            elif score > 20:
                emoji = "🟡"
                strength = "sedikit mendukung"
            elif score < -50:
                emoji = "🔴"
                strength = "sangat menentang"
            elif score < -20:
                emoji = "🟠"
                strength = "sedikit menentang"
            else:
                emoji = "⚪"
                strength = "netral"

            # Ambil penjelasan dari kamus
            term = self.dictionary.get_term(indicator)
            if term:
                simple_explanation = term["simple"]
            else:
                simple_explanation = f"Indikator {indicator}"

            # Format untuk sentiment
            if indicator == "sentiment":
                label = data.get("label", "NEUTRAL")
                explanation = f"{emoji} **SENTIMEN** (bobot {weight*100:.0f}%): {strength}\n   → Berita pasar cenderung {label.lower()}"
            else:
                explanation = f"{emoji} **{indicator.upper()}** (bobot {weight*100:.0f}%): {strength}\n   → Skor: {score:+.0f} | {signal}"

            explanations.append(explanation)

        # Tambahkan penjelasan bobot
        weight_note = "\n\n💡 **Catatan**: Bobot menunjukkan seberapa besar pengaruh setiap indikator terhadap keputusan final. MACD & EMA punya bobot terbesar (25%) karena paling reliable untuk tren."

        return "\n\n".join(explanations) + weight_note

    def _generate_action_plan(self, actions: Dict, symbol: str) -> str:
        """Generate rencana aksi yang jelas"""
        if actions["action"] == "HOLD":
            return f"""
🛑 **TIDAK ADA AKSI** - Tunggu konfirmasi lebih lanjut.

{actions['reason']}

🎯 **Saran**: Pantau terus {symbol}. Jika muncul sinyal baru dengan confidence > 60%, pertimbangkan untuk entry."""

        # Hitung nilai dalam USD (asumsi position size)
        entry = actions["entry"]
        sl = actions["stop_loss"]
        tp = actions["take_profit"]
        sl_pct = actions["sl_distance_percent"]
        tp_pct = actions["tp_distance_percent"]
        rr = actions["risk_reward_ratio"]
        pos_size = actions["position_size_percent"]

        direction = "NAIK" if actions["action"] == "OPEN_LONG" else "TURUN"

        return f"""
✅ **ACTION**: {actions['action'].replace('_', ' ')}

📍 Entry: **${entry:,.2f}**
🛑 Stop-Loss: **${sl:,.2f}** (-{sl_pct:.2f}%)
🎯 Take-Profit: **${tp:,.2f}** (+{tp_pct:.2f}%)
⚖️ Risk/Reward: **1:{rr}**
💼 Position Size: **{pos_size}%** dari portfolio

📖 **Penjelasan**:
Jika harga bergerak {direction}, kita target profit {tp_pct:.2f}%. Jika berlawanan, kita batasi loss di {sl_pct:.2f}%. Dengan rasio 1:{rr}, kita hanya perlu benar {100/(1+rr):.0f}% dari trade untuk tetap profit.

🛡️ **Risk Management**: Position size hanya {pos_size}% karena confidence {actions.get('confidence', 0):.0f}%. Jika confidence lebih tinggi, size bisa lebih besar."""

    def _generate_risk_education(self, confidence: float) -> str:
        """Generate edukasi risiko berdasarkan confidence"""
        if confidence < 60:
            return f"""
🔴 **CONFIDENCE RENDAH ({confidence:.0f}%)**

Ini artinya AI **tidak yakin** dengan keputusannya. Indikator-indikator memberikan sinyal yang bertentangan.

**Saran untuk pemula**:
• ❌ JANGAN entry dengan confidence < 60%
• 👀 Gunakan ini sebagai bahan belajar, bukan aksi
• 📚 Pahami mengapa indikator bertentangan

Ingat: Lebih baik kehilangan peluang daripada kehilangan uang!"""

        elif confidence < 75:
            return f"""
🟡 **CONFIDENCE SEDANG ({confidence:.0f}%)**

AI cukup yakin, tapi masih ada ketidakpastian.

**Saran untuk pemula**:
• ✅ Boleh entry dengan position size KECIL (2-5%)
• 🛑 WAJIB pasang stop-loss
• 👀 Monitor posisi dengan ketat

Trading bukan tentang selalu benar, tapi tentang mengelola risiko!"""

        else:
            return f"""
🟢 **CONFIDENCE TINGGI ({confidence:.0f}%)**

AI sangat yakin dengan keputusannya. Banyak indikator yang sejalan.

**Saran untuk pemula**:
• ✅ Boleh entry dengan position size NORMAL (5-10%)
• 🛑 TETAP pasang stop-loss (tidak ada yang 100% pasti!)
• 📊 Monitor performa untuk belajar

⚠️ **PERINGATAN**: Meskipun confidence tinggi, pasar bisa berubah tiba-tiba karena berita tak terduga. Selalu siap dengan rencana exit!"""

    def _generate_learning_point(self, signal: Dict) -> str:
        """Generate poin pembelajaran dari signal"""
        # Tentukan fokus pembelajaran berdasarkan kondisi
        tech_score = signal["technical_score"]
        sentiment_score = signal["sentiment_score"]

        learning_points = []

        # Belajar tentang indikator dominan
        strongest_indicator = max(
            signal["component_scores"].items(),
            key=lambda x: abs(x[1]["score"])
        )[0]

        term = self.dictionary.get_term(strongest_indicator)
        if term:
            learning_points.append(
                f"📚 **Pelajari {term['name']}**: {term['simple']}"
            )

        # Belajar tentang sentimen
        if abs(sentiment_score) > 0.3:
            learning_points.append(
                "📰 **Sentimen pasar penting**: Berita bisa menggerakkan harga lebih cepat daripada teknikal. Selalu pantau berita sebelum entry."
            )

        # Belajar tentang risk management
        learning_points.append(
            "🛡️ **Risk management adalah kunci**: Trader profesional fokus pada 'berapa yang bisa saya rugi?' BUKAN 'berapa yang bisa saya untung?'"
        )

        # Belajar tentang DYOR
        learning_points.append(
            "🔍 **DYOR (Do Your Own Research)**: Jangan pernah trade hanya karena kata AI, influencer, atau teman. Selalu verifikasi sendiri!"
        )

        return "\n\n".join(learning_points)

    def generate_quick_summary(self, signal: Dict) -> str:
        """Generate ringkasan singkat untuk notifikasi"""
        emoji = {
            "STRONG_BUY": "🟢🟢",
            "BUY": "🟢",
            "NEUTRAL": "⚪",
            "SELL": "🔴",
            "STRONG_SELL": "🔴🔴",
        }.get(signal["signal"], "⚪")

        return (
            f"{emoji} {signal['symbol']}: {signal['signal']} "
            f"(Confidence: {signal['confidence']:.0f}%)\n"
            f"💰 ${signal['latest_price']:,.2f} | "
            f"📈 Tech: {signal['technical_score']:+.1f} | "
            f"📰 Sent: {signal['sentiment_label']}"
        )
