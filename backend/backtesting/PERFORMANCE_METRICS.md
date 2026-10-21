# Performance Metrics Guide

## Overview

Backtesting engine calculates comprehensive performance metrics to evaluate strategy effectiveness. This guide explains each metric, how it's calculated, and how to interpret the results.

---

## Return Metrics

### Total Return

**Definition**: Absolute profit/loss in USD

**Formula**: 
```
Total Return = Final Balance - Initial Balance
```

**Example**:
```
Initial Balance: $10,000
Final Balance: $12,534.50
Total Return: $2,534.50
```

**Interpretation**:
- Positive: Strategy is profitable
- Negative: Strategy is losing money
- Compare with initial balance to understand scale

---

### Total Return %

**Definition**: Percentage return on initial investment

**Formula**:
```
Total Return % = ((Final Balance - Initial Balance) / Initial Balance) × 100
```

**Example**:
```
Initial: $10,000
Final: $12,534.50
Return %: ((12,534.50 - 10,000) / 10,000) × 100 = 25.35%
```

**Interpretation**:
- Allows comparison across different initial balances
- > 20% per year: Good performance
- < 0%: Losing strategy

---

### Annualized Return

**Definition**: Yearly return rate, normalized for comparison

**Formula**:
```
Annualized Return = ((1 + Total Return %) ^ (365 / Days)) - 1
```

**Example**:
```
Total Return: 25.35% over 365 days
Annualized: 25.35%
```

**Interpretation**:
- Standardizes returns for different time periods
- Compare with benchmark (e.g., S&P 500 ~10% annually)
- > 15% annually: Excellent
- 10-15%: Good
- < 10%: Average

---

### CAGR (Compound Annual Growth Rate)

**Definition**: Geometric progression ratio providing constant rate of return

**Formula**:
```
CAGR = ((Final Value / Initial Value) ^ (1 / Years)) - 1
```

**Example**:
```
Initial: $10,000
Final: $12,534.50
Years: 1
CAGR: ((12,534.50 / 10,000) ^ 1) - 1 = 25.35%
```

**Interpretation**:
- More accurate than simple annualized return
- Accounts for compounding effect
- Use for multi-year comparisons

---

## Risk Metrics

### Max Drawdown

**Definition**: Largest peak-to-trough decline in portfolio value

**Formula**:
```
Drawdown = (Current Value - Peak Value) / Peak Value × 100
Max Drawdown = Minimum of all drawdowns
```

**Example**:
```
Peak: $12,000
Trough: $10,800
Drawdown: (10,800 - 12,000) / 12,000 × 100 = -10%
```

**Interpretation**:
- Measures worst-case loss
- Lower is better
- < 10%: Conservative
- 10-20%: Moderate
- 20-30%: Aggressive
- > 30%: Very risky

---

### Max Drawdown %

**Definition**: Maximum drawdown as percentage

**Formula**:
```
Max Drawdown % = (Max Drawdown / Peak Value) × 100
```

**Example**:
```
Max Drawdown: -$1,200
Peak Value: $12,000
Max Drawdown %: (-1,200 / 12,000) × 100 = -10%
```

**Interpretation**:
- Standardized measure for comparison
- Use with recovery time to assess risk

---

### Volatility

**Definition**: Standard deviation of returns

**Formula**:
```
Volatility = StdDev(Daily Returns) × √252
```

**Example**:
```
Daily returns std dev: 1.5%
Annualized volatility: 1.5% × √252 = 23.81%
```

**Interpretation**:
- Measures price fluctuation
- Higher volatility = higher risk
- < 15%: Low volatility
- 15-25%: Moderate
- > 25%: High volatility

---

### Downside Risk

**Definition**: Standard deviation of negative returns only

**Formula**:
```
Downside Risk = √(Σ(min(Return - MAR, 0)²) / N)
where MAR = Minimum Acceptable Return (usually 0)
```

**Interpretation**:
- Focuses only on harmful volatility
- More relevant than total volatility for risk assessment
- Lower is better

---

## Risk-Adjusted Metrics

### Sharpe Ratio

**Definition**: Return per unit of total risk

**Formula**:
```
Sharpe Ratio = (Return - Risk-Free Rate) / Standard Deviation
```

**Example**:
```
Return: 25.35%
Risk-Free Rate: 2%
Standard Deviation: 15%
Sharpe: (25.35% - 2%) / 15% = 1.56
```

**Interpretation**:
- Measures risk-adjusted performance
- > 3.0: Excellent
- 2.0-3.0: Very good
- 1.0-2.0: Good
- 0.0-1.0: Acceptable
- < 0.0: Poor (worse than risk-free)

**Use Case**: Compare strategies with different risk levels

---

### Sortino Ratio

**Definition**: Return per unit of downside risk

**Formula**:
```
Sortino Ratio = (Return - Risk-Free Rate) / Downside Deviation
```

**Example**:
```
Return: 25.35%
Risk-Free Rate: 2%
Downside Deviation: 10%
Sortino: (25.35% - 2%) / 10% = 2.34
```

**Interpretation**:
- Similar to Sharpe but only penalizes downside volatility
- Higher than Sharpe indicates good upside capture
- > 3.0: Excellent
- 2.0-3.0: Very good
- 1.0-2.0: Good

**Use Case**: When you care more about downside risk than upside volatility

---

### Calmar Ratio

**Definition**: Annualized return divided by max drawdown

**Formula**:
```
Calmar Ratio = Annualized Return / |Max Drawdown|
```

**Example**:
```
Annualized Return: 25.35%
Max Drawdown: -10%
Calmar: 25.35% / 10% = 2.54
```

**Interpretation**:
- Measures return per unit of drawdown risk
- > 3.0: Excellent
- 2.0-3.0: Very good
- 1.0-2.0: Good
- < 1.0: Poor

**Use Case**: Assess risk-adjusted performance focusing on drawdowns

---

## Trade Statistics

### Total Trades

**Definition**: Number of trades executed

**Interpretation**:
- More trades = more data for statistical significance
- Minimum 30 trades for reliable statistics
- Very high frequency may indicate overtrading

---

### Winning Trades

**Definition**: Number of profitable trades

**Formula**:
```
Winning Trades = Count of trades where PnL > 0
```

---

### Losing Trades

**Definition**: Number of losing trades

**Formula**:
```
Losing Trades = Count of trades where PnL < 0
```

---

### Win Rate

**Definition**: Percentage of profitable trades

**Formula**:
```
Win Rate = (Winning Trades / Total Trades) × 100
```

**Example**:
```
Winning: 32
Total: 47
Win Rate: (32 / 47) × 100 = 68.09%
```

**Interpretation**:
- > 60%: Excellent
- 50-60%: Good
- 40-50%: Average
- < 40%: Poor

**Note**: High win rate doesn't guarantee profitability if losses are larger than wins

---

### Average Win

**Definition**: Average profit per winning trade

**Formula**:
```
Average Win = Σ(Winning Trade PnL) / Winning Trades
```

**Example**:
```
Total winning PnL: $5,936
Winning trades: 32
Average Win: $5,936 / 32 = $185.50
```

**Interpretation**:
- Compare with average loss
- Larger average win than average loss = good risk/reward

---

### Average Loss

**Definition**: Average loss per losing trade

**Formula**:
```
Average Loss = Σ(Losing Trade PnL) / Losing Trades
```

**Example**:
```
Total losing PnL: -$1,428
Losing trades: 15
Average Loss:- $1,428 15 = -$95.20
```

**Interpretation**:
- Should be smaller than average win
- Indicates risk management effectiveness

---

### Largest Win

**Definition**: Biggest single trade profit

**Interpretation**:
- Indicates potential upside
- Compare with average win to check for outliers

---

### Largest Loss

**Definition**: Biggest single trade loss

**Interpretation**:
- Indicates potential downside risk
- Compare with stop-loss settings
- Should be within acceptable risk limits

---

### Profit Factor

**Definition**: Ratio of gross profit to gross loss

**Formula**:
```
Profit Factor = Gross Profit / Gross Loss
```

**Example**:
```
Gross Profit: $5,936
Gross Loss: $2,526
Profit Factor: 5,936 / 2,526 = 2.35
```

**Interpretation**:
- > 2.0: Excellent
- 1.5-2.0: Good
- 1.0-1.5: Marginal
- < 1.0: Losing strategy

**Use Case**: Overall profitability measure

---

### Expectancy

**Definition**: Expected profit per trade

**Formula**:
```
Expectancy = (Win Rate × Average Win) - (Loss Rate × Average Loss)
```

**Example**:
```
Win Rate: 68.09%
Average Win: $185.50
Loss Rate: 31.91%
Average Loss: $95.20
Expectancy: (0.6809 × 185.50) - (0.3191 × 95.20) = $95.53
```

**Interpretation**:
- Positive: Strategy is profitable on average
- Negative: Strategy loses money on average
- Higher is better

---

### Payoff Ratio

**Definition**: Ratio of average win to average loss

**Formula**:
```
Payoff Ratio = Average Win / |Average Loss|
```

**Example**:
```
Average Win: $185.50
Average Loss: $95.20
Payoff Ratio: 185.50 / 95.20 = 1.95
```

**Interpretation**:
- > 2.0: Excellent risk/reward
- 1.5-2.0: Good
- 1.0-1.5: Average
- < 1.0: Poor (losses larger than wins)

**Use Case**: Assess risk/reward ratio

---

## Advanced Metrics

### Information Ratio

**Definition**: Active return per unit of tracking error

**Formula**:
```
Information Ratio = (Portfolio Return - Benchmark Return) / Tracking Error
```

**Interpretation**:
- Measures manager's ability to generate excess returns
- > 0.5: Good
- > 1.0: Excellent

---

### Beta

**Definition**: Sensitivity to market movements

**Formula**:
```
Beta = Covariance(Portfolio, Market) / Variance(Market)
```

**Interpretation**:
- Beta = 1: Moves with market
- Beta > 1: More volatile than market
- Beta < 1: Less volatile than market

---

### Alpha

**Definition**: Excess return over benchmark

**Formula**:
```
Alpha = Portfolio Return - (Risk-Free Rate + Beta × (Market Return - Risk-Free Rate))
```

**Interpretation**:
- Positive: Outperformance
- Negative: Underperformance
- Measure of manager skill

---

### Tail Ratio

**Definition**: Ratio of right tail to left tail

**Formula**:
```
Tail Ratio = |95th Percentile| / |5th Percentile|
```

**Interpretation**:
- > 1: More upside potential
- < 1: More downside risk
- Measures asymmetry of returns

---

### Skewness

**Definition**: Measure of return distribution asymmetry

**Formula**:
```
Skewness = E[(X - μ)³] / σ³
```

**Interpretation**:
- Positive: Right-skewed (more large gains)
- Negative: Left-skewed (more large losses)
- Zero: Symmetric distribution

---

### Kurtosis

**Definition**: Measure of return distribution "tailedness"

**Formula**:
```
Kurtosis = E[(X - μ)⁴] / σ⁴
```

**Interpretation**:
- > 3: Fat tails (more extreme events)
- = 3: Normal distribution
- < 3: Thin tails (fewer extreme events)

---

## Performance Benchmarks

### By Metric

| Metric | Poor | Average | Good | Excellent |
|--------|------|---------|------|-----------|
| **Annual Return** | < 5% | 5-10% | 10-20% | > 20% |
| **Sharpe Ratio** | < 0.5 | 0.5-1.0 | 1.0-2.0 | > 2.0 |
| **Sortino Ratio** | < 0.5 | 0.5-1.5 | 1.5-2.5 | > 2.5 |
| **Max Drawdown** | > 30% | 20-30% | 10-20% | < 10% |
| **Win Rate** | < 40% | 40-50% | 50-60% | > 60% |
| **Profit Factor** | < 1.0 | 1.0-1.5 | 1.5-2.0 | > 2.0 |
| **Payoff Ratio** | < 1.0 | 1.0-1.5 | 1.5-2.0 | > 2.0 |

### By Strategy Type

**Trend Following**:
- Expected Win Rate: 30-40%
- Expected Payoff Ratio: 2.0-3.0
- Expected Max Drawdown: 15-25%

**Mean Reversion**:
- Expected Win Rate: 60-70%
- Expected Payoff Ratio: 1.0-1.5
- Expected Max Drawdown: 10-15%

**Breakout**:
- Expected Win Rate: 40-50%
- Expected Payoff Ratio: 1.5-2.5
- Expected Max Drawdown: 20-30%

---

## Interpreting Results

### Good Strategy Characteristics

✅ **Positive expectancy** - Strategy makes money on average  
✅ **Sharpe ratio > 1.0** - Good risk-adjusted returns  
✅ **Max drawdown < 20%** - Acceptable risk level  
✅ **Win rate > 50%** - More winners than losers  
✅ **Profit factor > 1.5** - Gross profit exceeds gross loss  
✅ **Payoff ratio > 1.5** - Wins larger than losses  
✅ **Sufficient trades** - At least 30 for statistical significance  

### Red Flags

❌ **Negative expectancy** - Strategy loses money  
❌ **Sharpe ratio < 0** - Worse than risk-free rate  
❌ **Max drawdown > 30%** - Too risky  
❌ **Win rate < 40%** - Too many losing trades  
❌ **Profit factor < 1.0** - Losing strategy  
❌ **Very few trades** - Not enough data  
❌ **Large largest loss** - Poor risk management  

### Context Matters

**Consider**:
- Market conditions (bull vs bear)
- Time period tested
- Asset class characteristics
- Transaction costs
- Slippage
- Strategy complexity

**Compare with**:
- Benchmark performance
- Similar strategies
- Historical averages
- Risk-free rate

---

## Optimization Guidelines

### What to Optimize

1. **Sharpe Ratio** - Best overall measure
2. **Calmar Ratio** - If drawdown is primary concern
3. **Profit Factor** - If overall profitability is key
4. **Win Rate** - If consistency is important

### What NOT to Optimize

❌ **Total Return** - Can lead to overfitting  
❌ **Number of Trades** - More trades ≠ better  
❌ **Average Win** - Ignores losses  
❌ **Largest Win** - Outlier metric  

### Validation

**Always validate with**:
- Out-of-sample testing
- Walk-forward analysis
- Multiple time periods
- Different market conditions
- Monte Carlo simulation

---

## Reporting

### Essential Metrics to Report

1. **Total Return %** - Overall performance
2. **Sharpe Ratio** - Risk-adjusted performance
3. **Max Drawdown %** - Worst-case scenario
4. **Win Rate** - Consistency
5. **Profit Factor** - Profitability
6. **Total Trades** - Statistical significance
7. **Average Trade Duration** - Strategy style

### Optional Metrics

- Sortino Ratio
- Calmar Ratio
- Expectancy
- Payoff Ratio
- Skewness
- Kurtosis

### Visualization

**Essential Charts**:
- Equity curve
- Drawdown chart
- Trade distribution histogram
- Monthly returns heatmap

**Optional Charts**:
- Rolling Sharpe ratio
- Cumulative trades
- Win/loss streaks
- Performance by market condition

---

## Conclusion

Performance metrics provide comprehensive view of strategy effectiveness. Key takeaways:

1. **Use multiple metrics** - No single metric tells whole story
2. **Context matters** - Consider market conditions and strategy type
3. **Validate results** - Use out-of-sample testing
4. **Focus on risk-adjusted returns** - Sharpe, Sortino, Calmar
5. **Ensure statistical significance** - Minimum 30 trades
6. **Monitor drawdowns** - Max drawdown is critical risk measure
7. **Compare with benchmarks** - Relative performance matters

**Remember**: Past performance doesn't guarantee future results. Always use proper risk management and position sizing in live trading.

---

**Last Updated**: 2024-12-15  
**Version**: 1.0.0
