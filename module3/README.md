# Module 3: Visualizer & Live Data Stream

Owner: Member 3  
Primary Responsibility: Real-time chart streaming, ticker UI, and leaderboard sorting[cite: 1].

---

## Overview

Module 3 acts as the primary presentation and streaming layer for the AlgoClash trading engine. Implemented in `visualizer.py` using Streamlit and Plotly, it receives real-time market data ticks and user states to render live price movements and track participant performance[cite: 1].

---

## Core Components & API

The implementation is encapsulated within the `VisualizerModule` class:

### 1. Leaderboard Sorting (`calculate_leaderboard`)
* **Function:** `calculate_leaderboard(users: List[Dict], current_prices: Dict[str, float]) -> pd.DataFrame`
* **Algorithm:** Participants are ranked strictly in descending order of total liquid Net Worth[cite: 1]:
  $$\text{Net Worth} = \text{Cash Balance} + \sum_{k} (\text{Holdings}_k \times P_{\text{current}, k})$$
[cite: 1]
* **Output:** A structured, ranked pandas DataFrame with 1-based index standings.

### 2. Live Tickers (`render_tickers`)
* **Function:** `render_tickers(current_prices: Dict[str, float])`
* **Description:** Dynamically divides the top header into metric cards showing the current tick price for each tracked stock and sector index.

### 3. Real-Time Price Streaming (`render_chart`)
* **Function:** `render_chart(price_history_df: pd.DataFrame)`
* **Description:** Streams interactive multi-asset line charts using Plotly Express to plot historical ticks against price levels for equities and indices.

### 4. Leaderboard UI (`render_leaderboard`)
* **Function:** `render_leaderboard(leaderboard_df: pd.DataFrame)`
* **Description:** Renders the computed standings table on the venue screen layout.

---

## Dependencies

```text
streamlit>=1.30.0
pandas>=2.0.0
plotly>=5.18.0