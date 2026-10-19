"""
Chat Agent
Interface tanya-jawab untuk trader pemula
Menggunakan pattern matching + konteks dari database
"""
import re
from typing import Dict, List, Optional
from loguru import logger
from data_collector.database import DatabaseManager
from .trading_dictionary import TradingDictionary
from .explanation_generator import ExplanationGenerator
from .context_builder import ContextBuilder


class ChatAgent:
    """Chat agent untuk menjawab pertanyaan trader pemula"""

    def __init__(self, db: DatabaseManager):
        self.db = db
        self.dictionary = TradingDictionary()
        self.explainer = ExplanationGenerator()
        self.context_builder = ContextBuilder(db)

        # Pattern matching untuk intent detection
        self.intents = self._build_intents()

    def _build_intents(self) -> Dict:
        """Membangun pattern untuk mendeteksi intent user"""
        return {
            "greeting": {
                "patterns": [
                    r"\b(halo|hai|hi|hello|hey|pagi|siang|sore|malam)\b",
                ],
                "response": self._handle_greeting,
            },
            "explain_indicator": {
                "patterns": [
                    r"(apa itu|jelaskan|artinya|maksudnya)\s+(rsi|macd|ema|bollinger|atr|volume)",
                    r"(rsi|macd|ema|bollinger|atr|volume)\s+(itu apa|artinya apa|maksudnya apa)",
                ],
                "response": self._handle_explain_indicator,
            },
            "explain_concept": {
                "patterns": [
                    r"(apa itu|jelaskan|artinya)\s+(long|short|stop.?loss|take.?profit|confidence|drawdown|position.?sizing|risk.?reward|win.?rate|profit.?factor|slippage)",
                    r"(long|short|stop.?loss|take.?profit|confidence|drawdown)\s+(itu apa|artinya)",
                ],
                "response": self._handle_explain_concept,
            },
            "why_trade": {
                "patterns": [
                    r"kenapa\s+(bot|ai|kamu)\s+(jual|beli|hold|open|close)\s+(\w+)",
                    r"mengapa\s+(bot|ai)\s+(jual|beli)\s+(\w+)",
                    r"alasan\s+(jual|beli)\s+(\w+)",
                ],
                "response": self._handle_why_trade,
            },
            "portfolio_status": {
                "patterns": [
                    r"(status|kondisi|bagaimana)\s+(portfolio|portofolio|akun|saldo)",
                    r"(berapa|cek)\s+(saldo|profit|loss|pnl)",
                    r"portfolio\s+(saya|ku|gue)",
                ],
                "response": self._handle_portfolio_status,
            },
            "market_condition": {
                "patterns": [
                    r"(bagaimana|gimana)\s+(kondisi|pasar|market)\s+(\w+)?",
                    r"(btc|eth|sol|bnb|xrp)\s+(bagaimana|gimana)",
                    r"market\s+(hari ini|sekarang|saat ini)",
                ],
                "response": self._handle_market_condition,
            },
            "recent_trades": {
                "patterns": [
                    r"(trade|transaksi)\s+(terakhir|recent|last)",
                    r"riwayat\s+(trade|transaksi)",
                    r"history\s+(trade|transaksi)",
                ],
                "response": self._handle_recent_trades,
            },
            "help": {
                "patterns": [
                    r"\b(help|bantuan|bantu|cara pakai|tutorial)\b",
                    r"apa\s+(yang|bisa)\s+(bisa|bisa kamu|bisa anda)\s+(lakukan|bantu)",
                ],
                "response": self._handle_help,
            },
            "thanks": {
                "patterns": [
                    r"\b(thanks|terima kasih|thx|makasih)\b",
                ],
                "response": self._handle_thanks,
            },
        }

    async def process_message(self, user_message: str) -> str:
        """
        Memproses pesan user dan menghasilkan respons
        
        Args:
            user_message: Pesan dari user
            
        Returns:
            Respons dalam bentuk teks
        """
        user_message = user_message.lower().strip()
        logger.info(f"💬 User message: {user_message}")

        # 1. Deteksi intent
        intent, match = self._detect_intent(user_message)

        if intent:
            logger.info(f"🎯 Intent detected: {intent}")
            handler = self.intents[intent]["response"]
            response = await handler(match, user_message)
        else:
            # 2. Jika tidak ada intent, coba cari di kamus
            response = await self._handle_unknown(user_message)

        logger.info(f"💬 Response generated ({len(response)} chars)")
        return response

    def _detect_intent(self, message: str) -> tuple:
        """Mendeteksi intent dari pesan"""
        for intent_name, intent_data in self.intents.items():
            for pattern in intent_data["patterns"]:
                match = re.search(pattern, message, re.IGNORECASE)
                if match:
                    return intent_name, match
        return None, None

    async def _handle_greeting(self, match, message: str) -> str:
        """Handle greeting"""
        return """
👋 **Halo! Saya AI Trading Assistant**

Saya di sini untuk membantu Anda memahami trading dan keputusan yang diambil oleh bot.

💡 **Yang bisa saya bantu:**
• Jelaskan istilah trading (RSI, MACD, dll)
• Jelaskan kenapa bot melakukan trade tertentu
• Cek status portfolio Anda
• Analisis kondisi market
• Dan banyak lagi!

Coba tanya: *"Apa itu RSI?"* atau *"Kenapa bot beli BTC?"*
"""

    async def _handle_explain_indicator(self, match, message: str) -> str:
        """Handle pertanyaan tentang indikator"""
        indicator = match.group(2) if match.lastindex >= 2 else match.group(1)
        term = self.dictionary.get_term(indicator)

        if term:
            return self.dictionary.format_explanation(term, level="full")
        else:
            return f"❌ Maaf, saya tidak menemukan informasi tentang '{indicator}'. Coba tanya tentang: RSI, MACD, EMA, Bollinger Bands, ATR, atau Volume."

    async def _handle_explain_concept(self, match, message: str) -> str:
        """Handle pertanyaan tentang konsep trading"""
        concept = match.group(2) if match.lastindex >= 2 else match.group(1)
        
        # Normalisasi istilah
        concept_map = {
            "stop loss": "stop_loss",
            "stoploss": "stop_loss",
            "take profit": "take_profit",
            "takeprofit": "take_profit",
            "position sizing": "position_sizing",
            "risk reward": "risk_reward_ratio",
            "win rate": "win_rate",
            "profit factor": "profit_factor",
        }
        
        concept_key = concept_map.get(concept, concept)
        term = self.dictionary.get_term(concept_key)

        if term:
            return self.dictionary.format_explanation(term, level="full")
        else:
            return f"❌ Maaf, saya tidak menemukan informasi tentang '{concept}'. Coba tanya tentang: long, short, stop-loss, take-profit, confidence, drawdown, position sizing, risk/reward, win rate, profit factor, atau slippage."

    async def _handle_why_trade(self, match, message: str) -> str:
        """Handle pertanyaan kenapa bot melakukan trade"""
        action = match.group(2)
        symbol = match.group(3).upper() if match.lastindex >= 3 else None

        if not symbol:
            # Coba ekstrak simbol dari message
            symbols = ["BTC", "ETH", "SOL", "BNB", "XRP"]
            for s in symbols:
                if s in message.upper():
                    symbol = s + "/USDT"
                    break

        if not symbol:
            return "❓ Bisa tolong sebutkan simbolnya? Contoh: *'Kenapa bot beli BTC?'*"

        # Pastikan format simbol benar
        if "/" not in symbol:
            symbol = symbol + "/USDT"

        # Ambil signal context
        signal_context = await self.context_builder.build_signal_context(symbol)

        return f"""
🤔 **Mengapa bot melakukan {action.upper()} pada {symbol}?**

{signal_context}

💡 **Kesimpulan**:
Bot menganalisis kombinasi indikator teknikal dan sentimen berita. Jika mayoritas indikator sejalan (misalnya RSI oversold + MACD bullish crossover + sentimen positif), bot akan memberikan sinyal {action.upper()}.

📚 **Tips**: Selalu cek confidence score. Jika < 60%, pertimbangkan untuk tidak mengikuti sinyal. DYOR!
"""

    async def _handle_portfolio_status(self, match, message: str) -> str:
        """Handle pertanyaan tentang portfolio"""
        context = await self.context_builder.build_portfolio_context()
        return f"💼 **Status Portfolio Anda:**\n{context}"

    async def _handle_market_condition(self, match, message: str) -> str:
        """Handle pertanyaan tentang kondisi market"""
        # Cek apakah ada simbol spesifik
        symbols = ["BTC", "ETH", "SOL", "BNB", "XRP"]
        symbol = None
        for s in symbols:
            if s in message.upper():
                symbol = s + "/USDT"
                break

        context = await self.context_builder.build_market_context(symbol)
        return f"📊 **Kondisi Market:**\n{context}"

    async def _handle_recent_trades(self, match, message: str) -> str:
        """Handle pertanyaan tentang trade terakhir"""
        trades = await self.context_builder.get_recent_trades(limit=5)
        return f"📜 **Riwayat Trade:**\n{trades}"

    async def _handle_help(self, match, message: str) -> str:
        """Handle permintaan bantuan"""
        return """
📚 **Panduan Penggunaan AI Trading Assistant**

Saya bisa membantu Anda dengan berbagai pertanyaan seputar trading:

🔍 **Jelaskan Istilah**
• *"Apa itu RSI?"*
• *"Jelaskan MACD"*
• *"Artinya stop-loss?"*

🤔 **Pahami Keputusan Bot**
• *"Kenapa bot beli BTC?"*
• *"Mengapa bot jual ETH?"*
• *"Alasan bot hold SOL?"*

💼 **Cek Portfolio**
• *"Status portfolio saya"*
• *"Berapa profit saya?"*
• *"Trade terakhir"*

📊 **Analisis Market**
• *"Bagaimana kondisi BTC?"*
• *"Market hari ini gimana?"*

📖 **Belajar Trading**
• *"Apa itu long vs short?"*
• *"Jelaskan risk/reward ratio"*
• *"Cara baca win rate"*

💡 **Tips**: Gunakan bahasa santai, saya akan mengerti! 😊
"""

    async def _handle_thanks(self, match, message: str) -> str:
        """Handle ucapan terima kasih"""
        return "😊 Sama-sama! Senang bisa membantu. Jangan ragu untuk bertanya lagi kapan saja. Selamat trading dan ingat: **DYOR!** 🚀"

    async def _handle_unknown(self, message: str) -> str:
        """Handle pesan yang tidak dikenali"""
        # Coba cari di kamus
        search_results = self.dictionary.search(message)

        if search_results:
            term = search_results[0]
            return (
                f"🤔 Saya tidak yakin apa yang Anda maksud, tapi mungkin Anda bertanya tentang **{term['name']}**?\n\n"
                f"{self.dictionary.format_explanation(term, level='simple')}\n\n"
                f"Jika bukan ini yang Anda maksud, coba tanya dengan cara lain atau ketik *'help'* untuk melihat daftar pertanyaan yang bisa saya jawab."
            )

        return """
🤔 Maaf, saya belum mengerti pertanyaan Anda.

💡 **Coba tanya:**
• *"Apa itu RSI?"*
• *"Kenapa bot beli BTC?"*
• *"Status portfolio"*
• *"Help"* untuk daftar lengkap

Atau jelaskan dengan kata kunci yang berbeda! 😊
"""
