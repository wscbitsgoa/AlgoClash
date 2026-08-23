import streamlit as st
import pandas as pd
import plotly.express as px
from typing import List, Dict

class VisualizerModule:
    """
    Module 3: Visualizer & Live Data Stream
    Responsibilities:
      - Leaderboard sorting by liquid Net Worth
      - Ticker UI metrics
      - Real-time chart streaming
    """

    @staticmethod
    def calculate_leaderboard(users: List[Dict], current_prices: Dict[str, float]) -> pd.DataFrame:
        """
        Rank = SortDescending(Users, key = Cash + Portfolio Value)
        Net Worth = Cash Balance + Sum(Holdings_k * P_{current, k})
        """
        leaderboard = []
        for user in users:
            cash = float(user.get("cash", 0.0))
            holdings = user.get("holdings", {})
            portfolio_val = sum(qty * current_prices.get(symbol, 0.0) for symbol, qty in holdings.items())
            net_worth = cash + portfolio_val

            leaderboard.append({
                "User": user.get("username", "Unknown"),
                "Cash": cash,
                "Portfolio Value": portfolio_val,
                "Net Worth": net_worth
            })

        df = pd.DataFrame(leaderboard)
        if not df.empty:
            df = df.sort_values(by="Net Worth", ascending=False).reset_index(drop=True)
            df.index += 1  # 1-based rank
        return df

    @staticmethod
    def render_tickers(current_prices: Dict[str, float]):
        """Renders the top ticker UI display."""
        cols = st.columns(len(current_prices))
        for col, (symbol, price) in zip(cols, current_prices.items()):
            col.metric(label=symbol, value=f"${price:.2f}")

    @staticmethod
    def render_chart(price_history_df: pd.DataFrame):
        """Streams real-time line charts for stock/index prices."""
        fig = px.line(
            price_history_df,
            x="tick",
            y="price",
            color="symbol",
            title="Real-Time Price Stream"
        )
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def render_leaderboard(leaderboard_df: pd.DataFrame):
        """Displays the sorted participant standings."""
        st.subheader("Leaderboard")
        st.dataframe(leaderboard_df, use_container_width=True)