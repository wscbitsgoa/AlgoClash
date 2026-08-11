# 📚 System Architecture & Module Documentation

This document outlines the core modules, mathematical foundations, data streams, and API specifications for the trading event backend engine[cite: 1]. Every team member is responsible for maintaining their designated component[cite: 1].

---

## 👥 Module 1: Market Dynamics Engine
**Owner:** Member 1[cite: 1]  
**Primary Responsibility:** Synthetic price generation, baseline volatility, and sector drift[cite: 1].

### Overview
The market engine generates prices for 15 stocks across 3 sectors using a modified Geometric Brownian Motion (GBM) stochastic differential equation[cite: 1]. 

### Math & Formulas
For stock i at tick t+1, the price P_{i, t+1} is computed as:

P_{i, t+1} = max(1.0, P_{i, t} * (1 + Drift + Volatility * Z_t + SectorDrift_t + Shock_i))

Where:
* P_{i, t}: Current stock price[cite: 1].
* Drift: Annualized trend parameter.
* Volatility: Volatility parameter.
* Z_t: Standard Gaussian random variable ~ N(0, 1).
* SectorDrift_t: Macro push applied to all stocks within a given sector[cite: 1].
* Shock_i: Direct price override passed from Member 5's shock engine[cite: 1].

---

## ⚡ Module 2: Instant Execution Engine
**Owner:** Member 2[cite: 1]  
**Primary Responsibility:** High-speed order execution, balance tracking, and account validation[cite: 1].

### Overview
Because there is no order book matching lag, trades are processed in O(1) constant time[cite: 1]. The system validates account balances against real-time market prices (P_current) and updates in-memory states instantly[cite: 1].

### Core Logic & Mathematical Invariants
Net Worth = Cash Balance + Sum(Holdings_k * P_{current, k})

* BUY Constraints: Quantity * P_current <= Cash Balance
* SELL Constraints: Quantity <= Holdings_symbol (for long positions)

---

## 📊 Module 3: Visualizer & Live Data Stream
**Owner:** Member 3[cite: 1]  
**Primary Responsibility:** Real-time chart streaming, ticker UI, and leaderboard sorting[cite: 1].

### Overview
Renders a live dashboard (using Streamlit/Plotly) that auto-refreshes every tick[cite: 1]. It broadcasts stock prices and projects real-time participant performance on venue screens[cite: 1].

### Leaderboard Sorting Algorithm
Participants are ranked strictly by total liquid Net Worth:
Rank = SortDescending(Users, key = Cash + PortfolioValue)

---

## 📈 Module 4: Index Math & Cross-Asset Streams
**Owner:** Member 4[cite: 1]  
**Primary Responsibility:** Basket ETF pricing calculations and cross-asset synchronization[cite: 1].

### Overview
Calculates real-time pricing for synthetic index ETFs (INDEX_TECH and INDEX_MAIN) as an aggregate of underlying equities[cite: 1].

### Mathematical Formulas

1. Tech Sector Index (INDEX_TECH):
Weighted average of Tech Sector equities (STK_1 through STK_5)[cite: 1]:
INDEX_TECH_t = Sum(w_i * P_{i, t}) where Sum(w_i) = 1

2. Broad Market Index (INDEX_MAIN):
Weighted average of top 10 liquid stocks (STK_1 through STK_10)[cite: 1]:
INDEX_MAIN_t = (1 / 10) * Sum(P_{i, t})

---

## 💥 Module 5: Market Shock & Administrative Overrides
**Owner:** Member 5[cite: 1]  
**Primary Responsibility:** Manual event injection, rally/crash triggers, and volatility multipliers[cite: 1].

### Overview
Provides secure admin endpoints allowing event organizers to inject manual economic shocks (rallies or crashes) across individual stocks, entire sectors, or the entire market[cite: 1].

### Shock Injection Endpoint Specification
POST /admin/trigger-shock
Content-Type: application/json

Request Payload:
{
  "admin_key": "SUPER_SECRET_ADMIN_KEY",
  "target": "TECH",
  "direction": "CRASH",
  "magnitude_pct": 0.20
}

Parameter Definitions:
* admin_key (string): Authentication key for organizers[cite: 1].
* target (string): 'ALL', 'TECH', 'FINANCE', 'ENERGY', or specific symbol (e.g., 'STK_1')[cite: 1].
* direction (string): 'CRASH' (forces negative drop) or 'RALLY' (forces positive jump)[cite: 1].
* magnitude_pct (float): Percentage movement as a decimal (e.g., 0.20 = 20% price move)[cite: 1].

---
