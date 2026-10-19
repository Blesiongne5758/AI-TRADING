"""
Risk Manager
Validasi risiko sebelum eksekusi trade
"""
from typing import Dict, Optional
from loguru import logger


class RiskManager:
    """Mengelola validasi risiko untuk paper trading"""

    def __init__(
        self,
        max_risk_per_trade: float = 0.02,  # 2% max risk per trade
        max_open_positions: int = 5,
        max_position_size_percent: float = 0.10,  # 10% max position size
        min_confidence_threshold: float = 0.60  # 60% min confidence
    ):
        """
        Initialize risk manager
        
        Args:
            max_risk_per_trade: Max risk per trade (default 2%)
            max_open_positions: Max open positions (default 5)
            max_position_size_percent: Max position size as % of portfolio (default 10%)
            min_confidence_threshold: Min confidence to trade (default 60%)
        """
        self.max_risk_per_trade = max_risk_per_trade
        self.max_open_positions = max_open_positions
        self.max_position_size_percent = max_position_size_percent
        self.min_confidence_threshold = min_confidence_threshold
        
        logger.info(
            f"🛡️  Risk Manager initialized: "
            f"Max risk/trade={max_risk_per_trade:.1%}, "
            f"Max positions={max_open_positions}, "
            f"Max size={max_position_size_percent:.1%}, "
            f"Min confidence={min_confidence_threshold:.1%}"
        )

    def validate_signal(self, signal: Dict, portfolio_summary: Dict) -> Dict:
        """
        Validasi signal sebelum eksekusi
        
        Args:
            signal: Trading signal dari analysis engine
            portfolio_summary: Portfolio summary dari portfolio manager
            
        Returns:
            Dict dengan validation result:
            {
                "valid": bool,
                "reason": str,
                "adjusted_quantity": float or None,
                "adjusted_position_size": float or None
            }
        """
        # Check 1: Confidence threshold
        confidence = signal.get('confidence', 0)
        if confidence < self.min_confidence_threshold * 100:
            return {
                "valid": False,
                "reason": f"Confidence terlalu rendah: {confidence:.1f}% < {self.min_confidence_threshold*100:.1f}%",
                "adjusted_quantity": None,
                "adjusted_position_size": None
            }
        
        # Check 2: Signal type
        signal_type = signal.get('signal', 'NEUTRAL')
        if signal_type not in ['STRONG_BUY', 'BUY', 'STRONG_SELL', 'SELL']:
            return {
                "valid": False,
                "reason": f"Signal type tidak valid untuk trading: {signal_type}",
                "adjusted_quantity": None,
                "adjusted_position_size": None
            }
        
        # Check 3: Max open positions
        current_positions = portfolio_summary.get('open_positions', 0)
        if current_positions >= self.max_open_positions:
            return {
                "valid": False,
                "reason": f"Max open positions tercapai: {current_positions}/{self.max_open_positions}",
                "adjusted_quantity": None,
                "adjusted_position_size": None
            }
        
        # Check 4: Position already exists
        symbol = signal.get('symbol', '')
        positions = portfolio_summary.get('positions', [])
        if any(pos['symbol'] == symbol for pos in positions):
            return {
                "valid": False,
                "reason": f"Posisi untuk {symbol} sudah terbuka",
                "adjusted_quantity": None,
                "adjusted_position_size": None
            }
        
        # Check 5: Calculate position size based on risk
        current_balance = portfolio_summary.get('current_balance', 0)
        suggested_actions = signal.get('suggested_actions', {})
        entry_price = suggested_actions.get('entry', 0)
        stop_loss = suggested_actions.get('stop_loss', 0)
        
        if entry_price <= 0 or stop_loss <= 0:
            return {
                "valid": False,
                "reason": "Entry price atau stop loss tidak valid",
                "adjusted_quantity": None,
                "adjusted_position_size": None
            }
        
        # Calculate risk per unit
        risk_per_unit = abs(entry_price - stop_loss)
        
        # Calculate max risk amount (2% of portfolio)
        max_risk_amount = current_balance * self.max_risk_per_trade
        
        # Calculate quantity based on risk
        quantity_by_risk = max_risk_amount / risk_per_unit if risk_per_unit > 0 else 0
        
        # Calculate max position size (10% of portfolio)
        max_position_value = current_balance * self.max_position_size_percent
        quantity_by_size = max_position_value / entry_price if entry_price > 0 else 0
        
        # Use minimum of both
        adjusted_quantity = min(quantity_by_risk, quantity_by_size)
        adjusted_position_value = adjusted_quantity * entry_price
        adjusted_position_size_percent = (adjusted_position_value / current_balance) * 100 if current_balance > 0 else 0
        
        # Check if position is too small
        if adjusted_position_value < 10:  # Min $10 position
            return {
                "valid": False,
                "reason": f"Position size terlalu kecil: ${adjusted_position_value:.2f}",
                "adjusted_quantity": None,
                "adjusted_position_size": None
            }
        
        logger.info(
            f"✅ Signal validated: {symbol} {signal_type} "
            f"(Confidence: {confidence:.1f}%, "
            f"Position: ${adjusted_position_value:,.2f} / {adjusted_position_size_percent:.1f}%)"
        )
        
        return {
            "valid": True,
            "reason": "Signal valid",
            "adjusted_quantity": adjusted_quantity,
            "adjusted_position_size": adjusted_position_size_percent
        }

    def calculate_position_size(
        self,
        confidence: float,
        current_balance: float,
        entry_price: float,
        stop_loss: float
    ) -> Dict:
        """
        Calculate position size berdasarkan confidence dan risk
        
        Args:
            confidence: Signal confidence (0-100)
            current_balance: Current portfolio balance
            entry_price: Entry price
            stop_loss: Stop loss price
            
        Returns:
            Dict dengan position sizing data
        """
        # Base position size on confidence
        if confidence >= 75:
            base_size_percent = 0.10  # 10%
        elif confidence >= 60:
            base_size_percent = 0.05  # 5%
        else:
            base_size_percent = 0.02  # 2%
        
        # Calculate risk per unit
        risk_per_unit = abs(entry_price - stop_loss)
        
        # Calculate max risk amount
        max_risk_amount = current_balance * self.max_risk_per_trade
        
        # Calculate quantity by risk
        quantity_by_risk = max_risk_amount / risk_per_unit if risk_per_unit > 0 else 0
        
        # Calculate quantity by size
        max_position_value = current_balance * base_size_percent
        quantity_by_size = max_position_value / entry_price if entry_price > 0 else 0
        
        # Use minimum
        adjusted_quantity = min(quantity_by_risk, quantity_by_size)
        position_value = adjusted_quantity * entry_price
        position_size_percent = (position_value / current_balance) * 100 if current_balance > 0 else 0
        
        # Calculate actual risk
        actual_risk = risk_per_unit * adjusted_quantity
        actual_risk_percent = (actual_risk / current_balance) * 100 if current_balance > 0 else 0
        
        return {
            "quantity": adjusted_quantity,
            "position_value": position_value,
            "position_size_percent": position_size_percent,
            "risk_amount": actual_risk,
            "risk_percent": actual_risk_percent,
            "confidence_tier": "HIGH" if confidence >= 75 else "MEDIUM" if confidence >= 60 else "LOW"
        }

    def print_risk_summary(self, portfolio_summary: Dict):
        """Print risk summary"""
        logger.info("\n" + "="*70)
        logger.info("🛡️  RISK MANAGEMENT SUMMARY")
        logger.info("="*70)
        logger.info(f"   Max Risk per Trade: {self.max_risk_per_trade:.1%}")
        logger.info(f"   Max Open Positions: {self.max_open_positions}")
        logger.info(f"   Max Position Size: {self.max_position_size_percent:.1%}")
        logger.info(f"   Min Confidence: {self.min_confidence_threshold:.1%}")
        logger.info(f"\n   Current Open Positions: {portfolio_summary.get('open_positions', 0)}/{self.max_open_positions}")
        logger.info(f"   Current Balance: ${portfolio_summary.get('current_balance', 0):,.2f}")
        logger.info("="*70 + "\n")
