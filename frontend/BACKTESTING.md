# Frontend Backtesting Documentation

## Overview

Frontend backtesting interface menyediakan UI yang intuitif untuk:
- Configure dan run backtests
- Edit custom strategies
- Visualize results dengan charts dan tables
- Compare multiple strategies
- Optimize parameters

## Components

### 1. BacktestPanel.jsx

**Location**: `frontend/src/components/BacktestPanel.jsx`

**Purpose**: Configuration panel untuk running backtest

**Features**:
- Symbol selection (BTC/USDT, ETH/USDT, dll)
- Timeframe selection (1m, 5m, 15m, 1h, 4h, 1d)
- Date range picker
- Strategy selection dengan dynamic parameters
- Initial balance configuration
- Commission settings
- Real-time validation

**Props**:
```javascript
{
  onBacktestComplete: (result) => void  // Callback saat backtest selesai
}
```

**Usage**:
```jsx
import BacktestPanel from './components/BacktestPanel';

function App() {
  const handleBacktestComplete = (result) => {
    console.log('Backtest completed:', result);
    // Update UI dengan results
  };

  return <BacktestPanel onBacktestComplete={handleBacktestComplete} />;
}
```

**State Management**:
```javascript
{
  symbol: 'BTC/USDT',
  timeframe: '1h',
  startDate: '2024-01-01',
  endDate: '2024-12-31',
  strategy: 'rsi_macd',
  strategyParams: {
    rsi_period: 14,
    rsi_oversold: 30,
    rsi_overbought: 70
  },
  initialBalance: 10000,
  commission: 0.1,
  isRunning: false,
  error: ''
}
```

**API Integration**:
```javascript
// Fetch available strategies
GET /api/backtest/strategies

// Run backtest
POST /api/backtest/run
{
  symbol, timeframe, start_date, end_date,
  strategy, strategy_params, initial_balance, commission
}
```

---

### 2. StrategyEditor.jsx

**Location**: `frontend/src/components/StrategyEditor.jsx`

**Purpose**: Visual editor untuk custom strategies

**Features**:
- Create new custom strategies
- Edit existing strategies
- Add/remove conditions
- Set condition parameters (indicator, operator, value, logic)
- Save strategies ke backend
- Delete strategies

**Props**:
```javascript
{
  onStrategySaved: (strategy) => void  // Callback saat strategy tersimpan
}
```

**Usage**:
```jsx
import StrategyEditor from './components/StrategyEditor';

function App() {
  const handleStrategySaved = (strategy) => {
    console.log('Strategy saved:', strategy);
    // Refresh strategy list
  };

  return <StrategyEditor onStrategySaved={handleStrategySaved} />;
}
```

**Condition Structure**:
```javascript
{
  id: 1234567890,
  indicator: 'rsi',        // rsi, macd, ema, sma, bollinger, volume, price
  operator: 'less_than',   // less_than, greater_than, equals, crosses_above, crosses_below
  value: 30,
  logic: 'AND'             // AND, OR
}
```

**Available Indicators**:
- `rsi`: Relative Strength Index
- `macd`: Moving Average Convergence Divergence
- `ema`: Exponential Moving Average
- `sma`: Simple Moving Average
- `bollinger`: Bollinger Bands
- `volume`: Trading Volume
- `price`: Price action

**Available Operators**:
- `less_than`: < (value)
- `greater_than`: > (value)
- `equals`: = (value)
- `crosses_above`: Crosses above (value)
- `crosses_below`: Crosses below (value)

**API Integration**:
```javascript
// Fetch custom strategies
GET /api/backtest/custom-strategies

// Create strategy
POST /api/backtest/custom-strategies
{
  name: 'My Strategy',
  description: 'Custom RSI strategy',
  conditions: [...]
}

// Update strategy
PUT /api/backtest/custom-strategies/{id}
{
  name: 'Updated Strategy',
  description: 'Updated description',
  conditions: [...]
}

// Delete strategy
DELETE /api/backtest/custom-strategies/{id}
```

---

### 3. BacktestResults.jsx

**Location**: `frontend/src/components/BacktestResults.jsx`

**Purpose**: Comprehensive results visualization

**Features**:
- Summary metrics cards (Return, Risk, Trades)
- Equity curve chart (Area chart)
- Drawdown chart (Area chart)
- Trade history table
- Performance statistics
- Visual indicators (color-coded)

**Props**:
```javascript
{
  result: {
    // Backtest result object dari API
  }
}
```

**Usage**:
```jsx
import BacktestResults from './components/BacktestResults';

function App() {
  const [result, setResult] = useState(null);

  return <BacktestResults result={result} />;
}
```

**Result Structure**:
```javascript
{
  id: 'bt_20241215_143022_BTC_USDT',
  status: 'completed',
  symbol: 'BTC/USDT',
  timeframe: '1h',
  strategy: 'rsi_macd',
  start_date: '2024-01-01',
  end_date: '2024-12-31',
  initial_balance: 10000,
  final_balance: 12534.50,
  total_return: 2534.50,
  total_return_pct: 25.35,
  max_drawdown: -845.20,
  max_drawdown_pct: -8.45,
  sharpe_ratio: 2.45,
  win_rate: 68.09,
  total_trades: 47,
  winning_trades: 32,
  losing_trades: 15,
  avg_win: 185.50,
  avg_loss: -95.20,
  profit_factor: 2.35,
  equity_curve: [
    { timestamp: '2024-01-01T00:00:00', balance: 10000, drawdown: 0 },
    { timestamp: '2024-01-02T00:00:00', balance: 10150, drawdown: -1.5 },
    // ... more data points
  ],
  trades: [
    {
      type: 'BUY',
      entry_price: 42000,
      exit_price: 43500,
      pnl: 1500,
      pnl_pct: 3.57,
      entry_time: '2024-01-15T10:00:00',
      exit_time: '2024-01-20T14:00:00',
      duration: '5d 4h'
    },
    // ... more trades
  ]
}
```

**Charts**:
- **Equity Curve**: Area chart showing portfolio value over time
- **Drawdown**: Area chart showing drawdown percentage over time
- **Trade Distribution**: Histogram of trade P&L

**Color Coding**:
- 🟢 Green: Positive values (profit, wins)
- 🔴 Red: Negative values (loss, drawdown)
- 🔵 Blue: Neutral/informational
- 🟣 Purple: Custom strategies

---

### 4. Backtest.jsx (Page)

**Location**: `frontend/src/pages/Backtest.jsx`

**Purpose**: Main page yang menggabungkan semua components

**Features**:
- Tab navigation (Backtest, Strategy Editor, Results)
- State management
- API integration
- Error handling
- Loading states

**Tabs**:
```javascript
[
  { id: 'backtest', label: 'Backtest', icon: BarChart3 },
  { id: 'strategies', label: 'Strategy Editor', icon: Code },
  { id: 'results', label: 'Results', icon: TrendingUp }
]
```

**State Management**:
```javascript
{
  activeTab: 'backtest',
  backtestResult: null,
  customStrategies: []
}
```

**Usage**:
```jsx
import Backtest from './pages/Backtest';

// In App.jsx or router
<Route path="/backtest" element={<Backtest />} />
```

---

## Styling

### Color Scheme

```javascript
{
  // Background
  bg: 'slate-800',
  bgDark: 'slate-900',
  
  // Borders
  border: 'slate-700',
  borderHover: 'slate-600',
  
  // Text
  text: 'white',
  textMuted: 'slate-400',
  textDim: 'slate-500',
  
  // Accent colors
  blue: 'blue-400',
  green: 'green-400',
  red: 'red-400',
  purple: 'purple-400',
  orange: 'orange-400',
  
  // Status colors
  success: 'green-500',
  warning: 'yellow-500',
  error: 'red-500',
  info: 'blue-500'
}
```

### Component Styles

**Cards**:
```jsx
<div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
  {/* Content */}
</div>
```

**Buttons**:
```jsx
// Primary button
<button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg">
  Run Backtest
</button>

// Secondary button
<button className="bg-slate-700 hover:bg-slate-600 text-white px-6 py-3 rounded-lg">
  Cancel
</button>

// Danger button
<button className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg">
  Delete
</button>
```

**Inputs**:
```jsx
<input 
  type="text"
  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
/>
```

**Selects**:
```jsx
<select className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500">
  <option value="option1">Option 1</option>
  <option value="option2">Option 2</option>
</select>
```

---

## API Integration

### Base URL

```javascript
const API_BASE_URL = 'http://localhost:8000/api/backtest';
```

### Axios Instance

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});
```

### API Calls

#### Get Strategies
```javascript
const getStrategies = async () => {
  const response = await api.get('/strategies');
  return response.data;
};
```

#### Run Backtest
```javascript
const runBacktest = async (params) => {
  const response = await api.post('/run', params);
  return response.data;
};
```

#### Get Backtest Result
```javascript
const getBacktestResult = async (backtestId) => {
  const response = await api.get(`/results/${backtestId}`);
  return response.data;
};
```

#### List Backtest Results
```javascript
const listBacktestResults = async (limit = 10, offset = 0) => {
  const response = await api.get('/results', {
    params: { limit, offset }
  });
  return response.data;
};
```

#### Delete Backtest Result
```javascript
const deleteBacktestResult = async (backtestId) => {
  const response = await api.delete(`/results/${backtestId}`);
  return response.data;
};
```

#### Optimize Strategy
```javascript
const optimizeStrategy = async (params) => {
  const response = await api.post('/optimize', params);
  return response.data;
};
```

#### Get Custom Strategies
```javascript
const getCustomStrategies = async () => {
  const response = await api.get('/custom-strategies');
  return response.data;
};
```

#### Create Custom Strategy
```javascript
const createCustomStrategy = async (strategy) => {
  const response = await api.post('/custom-strategies', strategy);
  return response.data;
};
```

#### Update Custom Strategy
```javascript
const updateCustomStrategy = async (strategyId, strategy) => {
  const response = await api.put(`/custom-strategies/${strategyId}`, strategy);
  return response.data;
};
```

#### Delete Custom Strategy
```javascript
const deleteCustomStrategy = async (strategyId) => {
  const response = await api.delete(`/custom-strategies/${strategyId}`);
  return response.data;
};
```

---

## Error Handling

### API Errors

```javascript
try {
  const result = await runBacktest(params);
  // Success
} catch (error) {
  if (error.response) {
    // Server responded with error
    console.error('API Error:', error.response.data.detail);
    setError(error.response.data.detail);
  } else if (error.request) {
    // Request made but no response
    console.error('Network Error:', error.request);
    setError('Network error. Please check your connection.');
  } else {
    // Something else happened
    console.error('Error:', error.message);
    setError('An unexpected error occurred.');
  }
}
```

### Validation Errors

```javascript
const validateBacktestParams = (params) => {
  const errors = [];
  
  if (!params.symbol) {
    errors.push('Symbol is required');
  }
  
  if (!params.start_date || !params.end_date) {
    errors.push('Date range is required');
  }
  
  if (new Date(params.start_date) >= new Date(params.end_date)) {
    errors.push('Start date must be before end date');
  }
  
  if (params.initial_balance <= 0) {
    errors.push('Initial balance must be positive');
  }
  
  if (params.commission < 0 || params.commission > 10) {
    errors.push('Commission must be between 0 and 10%');
  }
  
  return errors;
};
```

---

## Loading States

### Spinner Component

```jsx
const LoadingSpinner = () => (
  <div className="flex items-center justify-center py-12">
    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400"></div>
  </div>
);
```

### Button Loading State

```jsx
<button
  disabled={isRunning}
  className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-colors ${
    isRunning
      ? 'bg-slate-700 text-slate-400 cursor-not-allowed'
      : 'bg-blue-600 hover:bg-blue-700 text-white'
  }`}
>
  {isRunning ? (
    <>
      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
      Running Backtest...
    </>
  ) : (
    <>
      <Play className="w-5 h-5" />
      Run Backtest
    </>
  )}
</button>
```

---

## Responsive Design

### Breakpoints

```javascript
{
  sm: '640px',   // Small screens
  md: '768px',   // Medium screens (tablets)
  lg: '1024px',  // Large screens (laptops)
  xl: '1280px',  // Extra large screens (desktops)
  '2xl': '1536px' // 2X large screens
}
```

### Grid Layouts

```jsx
// Mobile: 1 column, Tablet: 2 columns, Desktop: 3 columns
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Cards */}
</div>

// Mobile: 1 column, Desktop: 2 columns
<div className="grid grid-cols-1 md:grid-cols-2 gap-6">
  {/* Sections */}
</div>
```

### Responsive Tables

```jsx
<div className="overflow-x-auto">
  <table className="w-full">
    {/* Table content */}
  </table>
</div>
```

---

## Accessibility

### ARIA Labels

```jsx
<button aria-label="Run backtest">
  <Play className="w-5 h-5" />
  Run Backtest
</button>

<input 
  type="text" 
  aria-label="Strategy name"
  aria-describedby="strategy-name-help"
/>
<p id="strategy-name-help" className="text-sm text-slate-400">
  Enter a unique name for your strategy
</p>
```

### Keyboard Navigation

```jsx
// Tab navigation
<div role="tablist" className="flex gap-2">
  <button 
    role="tab" 
    aria-selected={activeTab === 'backtest'}
    tabIndex={activeTab === 'backtest' ? 0 : -1}
  >
    Backtest
  </button>
</div>
```

### Focus Management

```jsx
// Auto-focus on error
useEffect(() => {
  if (error) {
    errorRef.current?.focus();
  }
}, [error]);
```

---

## Testing

### Component Tests

```javascript
import { render, screen, fireEvent } from '@testing-library/react';
import BacktestPanel from './BacktestPanel';

describe('BacktestPanel', () => {
  it('renders without crashing', () => {
    render(<BacktestPanel onBacktestComplete={() => {}} />);
    expect(screen.getByText('Backtest Configuration')).toBeInTheDocument();
  });

  it('allows selecting symbol', () => {
    render(<BacktestPanel onBacktestComplete={() => {}} />);
    const select = screen.getByLabelText('Symbol');
    fireEvent.change(select, { target: { value: 'ETH/USDT' } });
    expect(select.value).toBe('ETH/USDT');
  });

  it('disables button when running', () => {
    render(<BacktestPanel onBacktestComplete={() => {}} />);
    const button = screen.getByRole('button', { name: /run backtest/i });
    fireEvent.click(button);
    expect(button).toBeDisabled();
  });
});
```

### Integration Tests

```javascript
import { rest } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  rest.post('/api/backtest/run', (req, res, ctx) => {
    return res(
      ctx.json({
        id: 'bt_test',
        status: 'completed',
        total_return_pct: 25.35
      })
    );
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

test('submits backtest request', async () => {
  render(<BacktestPanel onBacktestComplete={() => {}} />);
  
  fireEvent.click(screen.getByRole('button', { name: /run backtest/i }));
  
  expect(await screen.findByText(/completed/i)).toBeInTheDocument();
});
```

---

## Performance Optimization

### Memoization

```javascript
import { useMemo } from 'react';

const BacktestResults = ({ result }) => {
  const formattedData = useMemo(() => {
    return result.equity_curve.map(point => ({
      ...point,
      balance: formatCurrency(point.balance)
    }));
  }, [result.equity_curve]);

  return <Chart data={formattedData} />;
};
```

### Lazy Loading

```javascript
import { lazy, Suspense } from 'react';

const BacktestResults = lazy(() => import('./components/BacktestResults'));

function Backtest() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <BacktestResults result={result} />
    </Suspense>
  );
}
```

### Virtual Scrolling

```javascript
import { FixedSizeList } from 'react-window';

<FixedSizeList
  height={600}
  itemCount={trades.length}
  itemSize={50}
>
  {({ index, style }) => (
    <div style={style}>
      <TradeRow trade={trades[index]} />
    </div>
  )}
</FixedSizeList>
```

---

## Deployment

### Build

```bash
cd frontend
npm run build
```

Output: `frontend/dist/`

### Environment Variables

```bash
# .env.production
VITE_API_URL=https://api.yourdomain.com
```

### Serve

```bash
# Using serve
npx serve dist

# Using nginx
# Configure nginx to serve dist/ folder
```

---

## Troubleshooting

### Issue: CORS errors

**Solution**: Ensure backend has CORS enabled:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: Charts not rendering

**Solution**: Check Recharts installation:
```bash
npm install recharts
```

### Issue: Strategies not loading

**Solution**: Verify API endpoint:
```bash
curl http://localhost:8000/api/backtest/strategies
```

### Issue: Backtest takes too long

**Solution**: 
- Reduce date range
- Use larger timeframe (1d instead of 1h)
- Optimize backend performance

---

## Best Practices

### 1. Error Boundaries

```jsx
class ErrorBoundary extends React.Component {
  state = { hasError: false };

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return <h1>Something went wrong.</h1>;
    }
    return this.props.children;
  }
}

<ErrorBoundary>
  <Backtest />
</ErrorBoundary>
```

### 2. Loading States

```jsx
const [isLoading, setIsLoading] = useState(false);

const handleBacktest = async () => {
  setIsLoading(true);
  try {
    await runBacktest(params);
  } finally {
    setIsLoading(false);
  }
};
```

### 3. Debouncing

```javascript
import { useDebounce } from 'use-debounce';

const [searchTerm, setSearchTerm] = useState('');
const [debouncedSearchTerm] = useDebounce(searchTerm, 500);

useEffect(() => {
  if (debouncedSearchTerm) {
    searchStrategies(debouncedSearchTerm);
  }
}, [debouncedSearchTerm]);
```

### 4. Caching

```javascript
import { useQuery } from 'react-query';

const { data: strategies } = useQuery('strategies', getStrategies, {
  staleTime: 5 * 60 * 1000,  // 5 minutes
  cacheTime: 10 * 60 * 1000  // 10 minutes
});
```

---

## Future Enhancements

### Planned Features

1. **Real-time Updates**: WebSocket untuk live backtest progress
2. **Strategy Comparison**: Side-by-side comparison multiple strategies
3. **Advanced Charts**: Candlestick charts dengan trade markers
4. **Export Results**: Download results sebagai CSV/PDF
5. **Strategy Templates**: Pre-built strategy templates
6. **Collaborative Editing**: Share dan collaborate on strategies
7. **Mobile App**: React Native mobile app
8. **Dark/Light Theme**: Theme toggle

---

## Support

For issues or questions:
- Check documentation
- Review example code
- Open issue on GitHub

---

**Version**: 1.0.0  
**Last Updated**: 2024-12-15  
**React Version**: 18.2.0  
**Dependencies**: See `package.json`
