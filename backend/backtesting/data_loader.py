"""
Data Loader - Load historical data for backtesting
"""
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from loguru import logger
from data_collector.database import DatabaseManager


class DataLoader:
    """Load and prepare historical data for backtesting"""

    def __init__(self, db: DatabaseManager):
        self.db = db

    async def load_candles(
        self,
        symbol: str,
        timeframe: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> pd.DataFrame:
        """
        Load candlestick data from database

        Args:
            symbol: Trading pair (e.g., "BTC/USDT")
            timeframe: Timeframe (e.g., "1h")
            start_date: Start date (optional)
            end_date: End date (optional)

        Returns:
            DataFrame with OHLCV data
        """
        try:
            # Get all candles
            candles = await self.db.get_candles(symbol, timeframe, limit=10000)

            if not candles:
                logger.warning(f"No data found for {symbol} {timeframe}")
                return pd.DataFrame()

            # Convert to DataFrame
            df = pd.DataFrame(candles)

            # Convert timestamp to datetime
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            df.set_index("timestamp", inplace=True)

            # Filter by date range if provided
            if start_date:
                df = df[df.index >= start_date]
            if end_date:
                df = df[df.index <= end_date]

            # Sort by timestamp
            df = df.sort_index()

            logger.info(
                f"Loaded {len(df)} candles for {symbol} {timeframe} "
                f"from {df.index[0]} to {df.index[-1]}"
            )

            return df

        except Exception as e:
            logger.error(f"Error loading candles: {e}")
            return pd.DataFrame()

    async def load_news(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Dict]:
        """
        Load news data from database

        Args:
            start_date: Start date (optional)
            end_date: End date (optional)

        Returns:
            List of news articles
        """
        try:
            news = await self.db.get_latest_news(limit=1000)

            if not news:
                logger.warning("No news data found")
                return []

            # Filter by date range if provided
            if start_date or end_date:
                filtered_news = []
                for article in news:
                    pub_date = datetime.fromtimestamp(article["published_date"] / 1000)
                    if start_date and pub_date < start_date:
                        continue
                    if end_date and pub_date > end_date:
                        continue
                    filtered_news.append(article)
                news = filtered_news

            logger.info(f"Loaded {len(news)} news articles")
            return news

        except Exception as e:
            logger.error(f"Error loading news: {e}")
            return []

    def validate_data(self, df: pd.DataFrame) -> bool:
        """
        Validate data quality

        Args:
            df: DataFrame to validate

        Returns:
            True if valid, False otherwise
        """
        if df.empty:
            logger.error("DataFrame is empty")
            return False

        # Check for required columns
        required_cols = ["open", "high", "low", "close", "volume"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            logger.error(f"Missing columns: {missing_cols}")
            return False

        # Check for NaN values
        nan_counts = df[required_cols].isna().sum()
        if nan_counts.any():
            logger.warning(f"NaN values found: {nan_counts[nan_counts > 0].to_dict()}")

        # Check for negative prices
        if (df[required_cols[:-1]] <= 0).any().any():
            logger.error("Negative or zero prices found")
            return False

        # Check for logical consistency (high >= low, high >= open/close, etc.)
        if (df["high"] < df["low"]).any():
            logger.error("High < Low found in data")
            return False

        if (df["high"] < df["open"]).any() or (df["high"] < df["close"]).any():
            logger.error("High < Open/Close found in data")
            return False

        if (df["low"] > df["open"]).any() or (df["low"] > df["close"]).any():
            logger.error("Low > Open/Close found in data")
            return False

        logger.info("Data validation passed")
        return True

    def resample_data(self, df: pd.DataFrame, target_timeframe: str) -> pd.DataFrame:
        """
        Resample data to different timeframe

        Args:
            df: Source DataFrame
            target_timeframe: Target timeframe (e.g., "4h", "1d")

        Returns:
            Resampled DataFrame
        """
        try:
            # Map timeframe to pandas resample rule
            timeframe_map = {
                "1m": "1min",
                "5m": "5min",
                "15m": "15min",
                "1h": "1h",
                "4h": "4h",
                "1d": "1D",
            }

            rule = timeframe_map.get(target_timeframe)
            if not rule:
                logger.error(f"Unsupported timeframe: {target_timeframe}")
                return df

            # Resample
            resampled = df.resample(rule).agg(
                {
                    "open": "first",
                    "high": "max",
                    "low": "min",
                    "close": "last",
                    "volume": "sum",
                }
            )

            # Drop NaN rows
            resampled = resampled.dropna()

            logger.info(
                f"Resampled from {len(df)} to {len(resampled)} candles ({target_timeframe})"
            )

            return resampled

        except Exception as e:
            logger.error(f"Error resampling data: {e}")
            return df
