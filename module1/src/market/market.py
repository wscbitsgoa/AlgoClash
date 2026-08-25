from typing import Dict, Optional

import numpy as np

from .config import MarketConfig
from .stock import Stock


class Market:
    """
    Synthetic market containing 15 stocks across 3 sectors.

    Responsible for:
    - stock creation
    - price generation
    - baseline volatility
    - sector drift
    - accepting external shocks
    """


    DEFAULT_SECTORS = {
        "TECH": ["STK_1", "STK_2", "STK_3", "STK_4", "STK_5"],
        "FINANCE": ["STK_6", "STK_7", "STK_8", "STK_9", "STK_10"],
        "ENERGY": ["STK_11", "STK_12", "STK_13", "STK_14", "STK_15"],
    }

    def __init__(
        self,
        config: Optional[MarketConfig] = None,
        seed: Optional[int] = None,
    ):
        self.config = config or MarketConfig()

        # NumPy random number generator.
        # Providing a seed makes simulations reproducible.
        self.rng = np.random.default_rng(seed)

        self.stocks: Dict[str, Stock] = {}

        self.tick = 0

        self._create_stocks()

    def _create_stocks(self) -> None:
        """
        Create the 15 stocks across the 3 sectors.
        """

        for sector, symbols in self.DEFAULT_SECTORS.items():
            for symbol in symbols:
                self.stocks[symbol] = Stock(
                    symbol=symbol,
                    sector=sector,
                    price=self.config.initial_price,
                    drift=self.config.drift,
                    volatility=self.config.volatility,
                )

    def get_stock(self, symbol: str) -> Stock:
        """
        Return a stock by symbol.
        """

        if symbol not in self.stocks:
            raise KeyError(f"Unknown stock symbol: {symbol}")

        return self.stocks[symbol]

    def get_prices(self) -> Dict[str, float]:
        """
        Return the current price of every stock.
        """

        return {
            symbol: stock.price
            for symbol, stock in self.stocks.items()
        }

    def get_sector_prices(self, sector: str) -> Dict[str, float]:
        """
        Return prices for all stocks belonging to a sector.
        """

        if sector not in self.DEFAULT_SECTORS:
            raise KeyError(f"Unknown sector: {sector}")

        return {
            symbol: self.stocks[symbol].price
            for symbol in self.DEFAULT_SECTORS[sector]
        }

    def update(
        self,
        shocks: Optional[Dict[str, float]] = None,
        sector_drifts: Optional[Dict[str, float]] = None,
    ) -> Dict[str, float]:
        """
        Advance the market by one tick.

        Parameters
        ----------
        shocks:
            External shocks supplied by Module 5.

            Example:
                {
                    "STK_1": -0.20
                }

            or:

                {
                    "TECH": -0.20
                }

            or:

                {
                    "ALL": -0.20
                }

        sector_drifts:
            Optional sector-level drift overrides.

            Example:
                {
                    "TECH": 0.005
                }

        Returns
        -------
        Dict[str, float]
            Updated prices.
        """

        shocks = shocks or {}

        if sector_drifts is None:
            sector_drifts = self.config.sector_drifts

        self.tick += 1

        for symbol, stock in self.stocks.items():

            # Generate Z ~ N(0, 1)
            random_shock = self.rng.normal(0.0, 1.0)

            # Get sector-level drift.
            sector_drift = sector_drifts.get(
                stock.sector,
                0.0,
            )

            # Determine external shock.
            external_shock = self._get_external_shock(
                symbol=symbol,
                sector=stock.sector,
                shocks=shocks,
            )

            stock.update_price(
                random_shock=random_shock,
                sector_drift=sector_drift,
                external_shock=external_shock,
            )

        return self.get_prices()

    @staticmethod
    def _get_external_shock(
        symbol: str,
        sector: str,
        shocks: Dict[str, float],
    ) -> float:
        """
        Determine which external shock applies to a stock.

        Priority:

        1. Specific stock shock
        2. Sector shock
        3. ALL-market shock
        4. No shock
        """

        if symbol in shocks:
            return shocks[symbol]

        if sector in shocks:
            return shocks[sector]

        if "ALL" in shocks:
            return shocks["ALL"]

        return 0.0

    def reset(self) -> None:
        """
        Reset all stocks to their initial prices.
        """

        for stock in self.stocks.values():
            stock.price = self.config.initial_price

        self.tick = 0