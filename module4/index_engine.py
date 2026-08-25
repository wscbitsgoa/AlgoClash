from typing import Dict, List, Callable, Optional, Union
import numpy as np
import pandas as pd


class IndexEngine:
    # Initializes the index engine with stock symbols and weights.
    def __init__(
        self,
        tech_symbols: Optional[List[str]] = None,
        main_symbols: Optional[List[str]] = None,
        tech_weights: Optional[Dict[str, float]] = None,
    ):
        self.tech_symbols = tech_symbols or ["STK_1", "STK_2", "STK_3", "STK_4", "STK_5"]
        self.main_symbols = main_symbols or [f"STK_{i}" for i in range(1, 11)]

        if tech_weights is None:
            equal_w = 1.0 / len(self.tech_symbols)
            self.tech_weights = {sym: equal_w for sym in self.tech_symbols}
        else:
            self.tech_weights = tech_weights

        self.tech_weights_array = np.array([self.tech_weights[sym] for sym in self.tech_symbols], dtype=np.float64)

        self.latest_index_prices: Dict[str, float] = {
            "INDEX_TECH": 0.0,
            "INDEX_MAIN": 0.0,
        }

        self.history_df = pd.DataFrame(columns=["INDEX_TECH", "INDEX_MAIN"])

        self._subscribers: List[Callable[[Dict[str, float]], None]] = []

    # Calculates the weighted tech sector index price.
    def calculate_index_tech(self, current_prices: Dict[str, float]) -> float:
        prices_array = np.array([current_prices[sym] for sym in self.tech_symbols], dtype=np.float64)
        tech_index = float(np.dot(self.tech_weights_array, prices_array))
        return tech_index

    # Calculates the equal-weighted broad market index price.
    def calculate_index_main(self, current_prices: Dict[str, float]) -> float:
        prices_array = np.array([current_prices[sym] for sym in self.main_symbols], dtype=np.float64)
        main_index = float(np.mean(prices_array))
        return main_index

    # Registers a callback subscriber for index price updates.
    def register_subscriber(self, callback_fn: Callable[[Dict[str, float]], None]) -> None:
        if callback_fn not in self._subscribers:
            self._subscribers.append(callback_fn)

    # Notifies registered subscribers with updated index prices.
    def notify_subscribers(self, index_prices: Dict[str, float]) -> None:
        for callback in self._subscribers:
            callback(index_prices)

    # Processes a price tick by updating indices, history, and subscribers.
    def on_price_tick(self, tick_prices: Dict[str, float]) -> Dict[str, float]:
        tech_price = self.calculate_index_tech(tick_prices)
        main_price = self.calculate_index_main(tick_prices)

        self.latest_index_prices = {
            "INDEX_TECH": tech_price,
            "INDEX_MAIN": main_price,
        }

        new_row = pd.DataFrame([self.latest_index_prices])
        self.history_df = pd.concat([self.history_df, new_row], ignore_index=True)

        self.notify_subscribers(self.latest_index_prices)

        return self.latest_index_prices

    # Returns summary statistics of historical index prices.
    def get_historical_summary(self) -> pd.DataFrame:
        if self.history_df.empty:
            return pd.DataFrame()
        return self.history_df.describe()


if __name__ == "__main__":
    print("AlgoClash - Module 4 Engine (NumPy & Pandas Version) Loaded.")
