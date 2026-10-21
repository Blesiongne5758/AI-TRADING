"""
Custom Strategies Framework
Framework untuk membuat dan menjalankan custom trading strategies
"""
import pandas as pd
from typing import Dict, List, Optional, Callable
from datetime import datetime
from loguru import logger
from abc import ABC, abstractmethod


class BaseStrategy(ABC):
    """Base class untuk semua trading strategies"""

    def __init__(self, name: str, params: Dict = None):
        self.name = name
        self.params = params or {}
        self.description = ""

    @abstractmethod
    def generate_signal(self, df: pd.DataFrame, index: int) -> Dict:
        """
        Generate trading signal
        
        Args:
            df: DataFrame dengan OHLCV data
            index: Current candle index
            
        Returns:
            Dictionary dengan signal:
            {
                "action": "BUY" | "SELL" | "HOLD",
                "confidence": float (0-100),
                "stop_loss": float,
                "take_profit": float,
                "reason": str
            }
        """
        pass

    def validate_data(self, df: pd.DataFrame) -> bool:
        """Validate jika data cukup untuk strategy"""
        return len(df) >= 50  # Minimum 50 candles


class RSIMACDStrategy(BaseStrategy):
    """Strategy berdasarkan RSI dan MACD crossover"""

    def __init__(self, params: Dict = None):
        super().__init__("RSI + MACD Crossover", params)
        self.description = "Buy when RSI < 30 and MACD crosses above signal line"
        
        # Default parameters
        self.rsi_period = self.params.get('rsi_period', 14)
        self.rsi_oversold = self.params.get('rsi_oversold', 30)
        self.rsi_overbought = self.params.get('rsi_overbought', 70)
        self.macd_fast = self.params.get('macd_fast', 12)
        self.macd_slow = self.params.get('macd_slow', 26)
        self.macd_signal = self.params.get('macd_signal', 9)

    def generate_signal(self, df: pd.DataFrame, index: int) -> Dict:
        """Generate signal berdasarkan RSI dan MACD"""
        try:
            # Calculate RSI
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))

            # Calculate MACD
            ema_fast = df['close'].ewm(span=self.macd_fast, adjust=False).mean()
            ema_slow = df['close'].ewm(span=self.macd_slow, adjust=False).mean()
            macd_line = ema_fast - ema_slow
            signal_line = macd_line.ewm(span=self.macd_signal, adjust=False).mean()
            macd_histogram = macd_line - signal_line

            current_rsi = rsi.iloc[index]
            current_macd = macd_line.iloc[index]
            current_signal = signal_line.iloc[index]
            prev_macd = macd_line.iloc[index - 1]
            prev_signal = signal_line.iloc[index - 1]

            # Buy signal: RSI oversold + MACD bullish crossover
            if current_rsi < self.rsi_oversold and current_macd > current_signal and prev_macd <= prev_signal:
                return {
                    "action": "BUY",
                    "confidence": 75,
                    "stop_loss": df['close'].iloc[index] * 0.98,
                    "take_profit": df['close'].iloc[index] * 1.04,
                    "reason": f"RSI oversold ({current_rsi:.1f}) + MACD bullish crossover"
                }

            # Sell signal: RSI overbought + MACD bearish crossover
            elif current_rsi > self.rsi_overbought and current_macd < current_signal and prev_macd >= prev_signal:
                return {
                    "action": "SELL",
                    "confidence": 75,
                    "stop_loss": df['close'].iloc[index] * 1.02,
                    "take_profit": df['close'].iloc[index] * 0.96,
                    "reason": f"RSI overbought ({current_rsi:.1f}) + MACD bearish crossover"
                }

            else:
                return {
                    "action": "HOLD",
                    "confidence": 50,
                    "stop_loss": 0,
                    "take_profit": 0,
                    "reason": "No signal"
                }

        except Exception as e:
            logger.error(f"Error in RSI+MACD strategy: {e}")
            return {"action": "HOLD", "confidence": 0, "stop_loss": 0, "take_profit": 0, "reason": "Error"}


class EMACrossStrategy(BaseStrategy):
    """Strategy berdasarkan EMA crossover"""

    def __init__(self, params: Dict = None):
        super().__init__("EMA Crossover", params)
        self.description = "Buy when fast EMA crosses above slow EMA"
        
        # Default parameters
        self.fast_ema = self.params.get('fast_ema', 20)
        self.slow_ema = self.params.get('slow_ema', 50)

    def generate_signal(self, df: pd.DataFrame, index: int) -> Dict:
        """Generate signal berdasarkan EMA crossover"""
        try:
            # Calculate EMAs
            fast_ema = df['close'].ewm(span=self.fast_ema, adjust=False).mean()
            slow_ema = df['close'].ewm(span=self.slow_ema, adjust=False).mean()

            current_fast = fast_ema.iloc[index]
            current_slow = slow_ema.iloc[index]
            prev_fast = fast_ema.iloc[index - 1]
            prev_slow = slow_ema.iloc[index - 1]

            # Buy signal: Fast EMA crosses above slow EMA
            if current_fast > current_slow and prev_fast <= prev_slow:
                return {
                    "action": "BUY",
                    "confidence": 70,
                    "stop_loss": df['close'].iloc[index] * 0.97,
                    "take_profit": df['close'].iloc[index] * 1.05,
                    "reason": f"EMA {self.fast_ema} crossed above EMA {self.slow_ema}"
                }

            # Sell signal: Fast EMA crosses below slow EMA
            elif current_fast < current_slow and prev_fast >= prev_slow:
                return {
                    "action": "SELL",
                    "confidence": 70,
                    "stop_loss": df['close'].iloc[index] * 1.03,
                    "take_profit": df['close'].iloc[index] * 0.95,
                    "reason": f"EMA {self.fast_ema} crossed below EMA {self.slow_ema}"
                }

            else:
                return {
                    "action": "HOLD",
                    "confidence": 50,
                    "stop_loss": 0,
                    "take_profit": 0,
                    "reason": "No crossover"
                }

        except Exception as e:
            logger.error(f"Error in EMA Cross strategy: {e}")
            return {"action": "HOLD", "confidence": 0, "stop_loss": 0, "take_profit": 0, "reason": "Error"}


class BollingerBandStrategy(BaseStrategy):
    """Strategy berdasarkan Bollinger Bands"""

    def __init__(self, params: Dict = None):
        super().__init__("Bollinger Bands", params)
        self.description = "Buy when price touches lower band, sell when touches upper band"
        
        # Default parameters
        self.bb_period = self.params.get('bb_period', 20)
        self.bb_std = self.params.get('bb_std', 2)

    def generate_signal(self, df: pd.DataFrame, index: int) -> Dict:
        """Generate signal berdasarkan Bollinger Bands"""
        try:
            # Calculate Bollinger Bands
            middle = df['close'].rolling(window=self.bb_period).mean()
            std = df['close'].rolling(window=self.bb_period).std()
            upper = middle + (std * self.bb_std)
            lower = middle - (std * self.bb_std)

            current_price = df['close'].iloc[index]
            current_upper = upper.iloc[index]
            current_lower = lower.iloc[index]
            current_middle = middle.iloc[index]

            # Buy signal: Price touches or breaks lower band
            if current_price <= current_lower:
                return {
                    "action": "BUY",
                    "confidence": 65,
                    "stop_loss": current_lower * 0.99,
                    "take_profit": current_middle,
                    "reason": f"Price touched lower Bollinger Band"
                }

            # Sell signal: Price touches or breaks upper band
            elif current_price >= current_upper:
                return {
                    "action": "SELL",
                    "confidence": 65,
                    "stop_loss": current_upper * 1.01,
                    "take_profit": current_middle,
                    "reason": f"Price touched upper Bollinger Band"
                }

            else:
                return {
                    "action": "HOLD",
                    "confidence": 50,
                    "stop_loss": 0,
                    "take_profit": 0,
                    "reason": "Price within bands"
                }

        except Exception as e:
            logger.error(f"Error in Bollinger Bands strategy: {e}")
            return {"action": "HOLD", "confidence": 0, "stop_loss": 0, "take_profit": 0, "reason": "Error"}


class CombinedStrategy(BaseStrategy):
    """Strategy yang menggabungkan multiple indicators"""

    def __init__(self, params: Dict = None):
        super().__init__("Combined Strategy", params)
        self.description = "Combines RSI, MACD, and EMA for stronger signals"
        
        # Default parameters
        self.rsi_period = self.params.get('rsi_period', 14)
        self.rsi_oversold = self.params.get('rsi_oversold', 35)
        self.rsi_overbought = self.params.get('rsi_overbought', 65)
        self.ema_fast = self.params.get('ema_fast', 20)
        self.ema_slow = self.params.get('ema_slow', 50)

    def generate_signal(self, df: pd.DataFrame, index: int) -> Dict:
        """Generate signal berdasarkan kombinasi indicators"""
        try:
            # Calculate RSI
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))

            # Calculate EMAs
            ema_fast = df['close'].ewm(span=self.ema_fast, adjust=False).mean()
            ema_slow = df['close'].ewm(span=self.ema_slow, adjust=False).mean()

            current_rsi = rsi.iloc[index]
            current_ema_fast = ema_fast.iloc[index]
            current_ema_slow = ema_slow.iloc[index]
            current_price = df['close'].iloc[index]

            # Strong buy: RSI oversold + Price above EMAs + Fast EMA > Slow EMA
            if (current_rsi < self.rsi_oversold and 
                current_price > current_ema_fast > current_ema_slow):
                return {
                    "action": "BUY",
                    "confidence": 85,
                    "stop_loss": current_price * 0.97,
                    "take_profit": current_price * 1.06,
                    "reason": f"RSI oversold ({current_rsi:.1f}) + Uptrend confirmed"
                }

            # Strong sell: RSI overbought + Price below EMAs + Fast EMA < Slow EMA
            elif (current_rsi > self.rsi_overbought and 
                  current_price < current_ema_fast < current_ema_slow):
                return {
                    "action": "SELL",
                    "confidence": 85,
                    "stop_loss": current_price * 1.03,
                    "take_profit": current_price * 0.94,
                    "reason": f"RSI overbought ({current_rsi:.1f}) + Downtrend confirmed"
                }

            # Weak buy: RSI neutral + Fast EMA > Slow EMA
            elif current_ema_fast > current_ema_slow:
                return {
                    "action": "BUY",
                    "confidence": 60,
                    "stop_loss": current_price * 0.98,
                    "take_profit": current_price * 1.04,
                    "reason": "Uptrend (EMA crossover)"
                }

            # Weak sell: RSI neutral + Fast EMA < Slow EMA
            elif current_ema_fast < current_ema_slow:
                return {
                    "action": "SELL",
                    "confidence": 60,
                    "stop_loss": current_price * 1.02,
                    "take_profit": current_price * 0.96,
                    "reason": "Downtrend (EMA crossover)"
                }

            else:
                return {
                    "action": "HOLD",
                    "confidence": 50,
                    "stop_loss": 0,
                    "take_profit": 0,
                    "reason": "No clear signal"
                }

        except Exception as e:
            logger.error(f"Error in Combined strategy: {e}")
            return {"action": "HOLD", "confidence": 0, "stop_loss": 0, "take_profit": 0, "reason": "Error"}


class StrategyFactory:
    """Factory untuk create strategy instances"""

    AVAILABLE_STRATEGIES = {
        "rsi_macd": RSIMACDStrategy,
        "ema_cross": EMACrossStrategy,
        "bollinger": BollingerBandStrategy,
        "combined": CombinedStrategy,
    }

    @staticmethod
    def create_strategy(strategy_name: str, params: Dict = None) -> BaseStrategy:
        """
        Create strategy instance
        
        Args:
            strategy_name: Name of strategy
            params: Strategy parameters
            
        Returns:
            Strategy instance
        """
        if strategy_name not in StrategyFactory.AVAILABLE_STRATEGIES:
            raise ValueError(f"Unknown strategy: {strategy_name}")

        strategy_class = StrategyFactory.AVAILABLE_STRATEGIES[strategy_name]
        return strategy_class(params)

    @staticmethod
    def list_strategies() -> List[str]:
        """List semua available strategies"""
        return list(StrategyFactory.AVAILABLE_STRATEGIES.keys())

    @staticmethod
    def get_strategy_info(strategy_name: str) -> Dict:
        """Get strategy information"""
        if strategy_name not in StrategyFactory.AVAILABLE_STRATEGIES:
            raise ValueError(f"Unknown strategy: {strategy_name}")

        strategy_class = StrategyFactory.AVAILABLE_STRATEGIES[strategy_name]
        instance = strategy_class()
        
        return {
            "name": instance.name,
            "description": instance.description,
            "default_params": instance.params
        }


class CustomStrategyBuilder:
    """Builder untuk membuat custom strategies"""

    def __init__(self):
        self.conditions = []
        self.name = "Custom Strategy"
        self.description = ""

    def set_name(self, name: str) -> 'CustomStrategyBuilder':
        """Set strategy name"""
        self.name = name
        return self

    def set_description(self, description: str) -> 'CustomStrategyBuilder':
        """Set strategy description"""
        self.description = description
        return self

    def add_condition(self, condition: Callable) -> 'CustomStrategyBuilder':
        """Add condition function"""
        self.conditions.append(condition)
        return self

    def build(self) -> BaseStrategy:
        """Build custom strategy"""
        
        class CustomStrategy(BaseStrategy):
            def __init__(self, name, description, conditions):
                super().__init__(name)
                self.description = description
                self.conditions = conditions

            def generate_signal(self, df: pd.DataFrame, index: int) -> Dict:
                """Generate signal based on custom conditions"""
                try:
                    # Check all conditions
                    for condition in self.conditions:
                        result = condition(df, index)
                        if result and result.get("action") != "HOLD":
                            return result

                    return {
                        "action": "HOLD",
                        "confidence": 50,
                        "stop_loss": 0,
                        "take_profit": 0,
                        "reason": "No condition met"
                    }

                except Exception as e:
                    logger.error(f"Error in custom strategy: {e}")
                    return {
                        "action": "HOLD",
                        "confidence": 0,
                        "stop_loss": 0,
                        "take_profit": 0,
                        "reason": f"Error: {str(e)}"
                    }

        return CustomStrategy(self.name, self.description, self.conditions)


# Example usage
if __name__ == "__main__":
    # List available strategies
    print("Available strategies:")
    for strategy in StrategyFactory.list_strategies():
        info = StrategyFactory.get_strategy_info(strategy)
        print(f"  - {info['name']}: {info['description']}")

    # Create strategy
    strategy = StrategyFactory.create_strategy("rsi_macd", {
        "rsi_period": 14,
        "rsi_oversold": 30,
        "rsi_overbought": 70
    })

    print(f"\nCreated strategy: {strategy.name}")
    print(f"Description: {strategy.description}")
