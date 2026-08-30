# Module 2: Instant Execution Engine

**Owner:** Member 2
**Part of:** Trading Event Backend Engine

## Overview

This module handles order execution, balance tracking, and account validation for the trading simulation. Since there is no order book matching, all trades are processed instantly (O(1)) against the current market price supplied by [Module 1: Market Dynamics Engine](../market-dynamics-engine).

The module validates every BUY/SELL order against the account's cash and holdings, updates state in memory, and exposes net worth calculations used by the leaderboard (Module 3).

## Files

| File | Purpose |
|---|---|
| `account.py` | Defines the `Account` class — holds a user's cash balance and stock holdings, and computes net worth. |
| `execution_engine.py` | Defines `execute_order()` — validates and executes BUY/SELL orders against an `Account`, and `OrderResult`, a small result object returned by every call. |
| `test_execution_engine.py` | Automated tests covering successful trades and every rejection case (insufficient cash, insufficient holdings, unknown symbol). |

## Core Logic

**Net Worth**
```
Net Worth = Cash Balance + Σ(Holdings_k * P_current,k)
```

**BUY constraint**
```
Quantity * P_current <= Cash Balance
```

**SELL constraint**
```
Quantity <= Holdings_symbol
```

## Usage

```python
from account import Account
from execution_engine import execute_order

# Create an account (default starting cash: $10,000)
alice = Account("alice")

# Current prices — normally supplied by market_engine.get_current_prices()
prices = {"STK_1": 50.0}

# Place an order
result = execute_order(alice, "STK_1", 10, "BUY", prices)

print(result.success)   # True
print(result.message)   # "Bought 10 STK_1 @ 50.00"
print(alice.cash)       # 9500.0
print(alice.holdings)   # {"STK_1": 10}
```

### Checking net worth

```python
prices = {"STK_1": 55.0}
print(alice.net_worth(prices))  # 9500 + (10 * 55) = 10050.0
```

## Integration with Module 1

`execute_order()` accepts `current_prices` as a plain dictionary (`{"STK_1": 102.34, ...}`), so it can be wired up to Module 1's live price feed with a single import — no changes needed to the internal logic:

```python
from market_engine import get_current_prices

prices = get_current_prices()
result = execute_order(alice, "STK_1", 10, "BUY", prices)
```

Tests continue to pass a static dict directly, so they run independently of Module 1.

## Setup

```bash
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install pytest
```

## Running Tests

```bash
pytest
```

Expected output: all tests pass, covering:
- Successful BUY and SELL orders
- Rejected orders (insufficient cash, insufficient holdings, unknown symbol)

## Notes for Other Modules

- **Module 3 (Leaderboard):** call `account.net_worth(current_prices)` on each `Account` to rank participants.
- **Module 4 (Index Math):** can read `account.holdings` directly if aggregate holdings data is needed.
- **Module 5 (Admin Shocks):** no direct dependency — shocks affect prices upstream in Module 1, which this module already consumes transparently.