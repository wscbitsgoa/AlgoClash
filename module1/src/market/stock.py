from dataclasses import dataclass


@dataclass
class Stock:
    """
    Represents one synthetic stock in the market.
    """

    symbol: str
    sector: str
    price: float
    drift: float
    volatility: float

    def __post_init__(self):
        if self.price <= 0:
            raise ValueError("Stock price must be positive.")

        if self.volatility < 0:
            raise ValueError("Volatility cannot be negative.")

    def update_price(
        self,
        random_shock: float,
        sector_drift: float = 0.0,
        external_shock: float = 0.0,
    ) -> float:
        """
        Update the stock price according to the Module 1 model.

        P(t+1) =
            max(
                1,
                P(t) * (
                    1
                    + Drift
                    + Volatility * Z
                    + SectorDrift
                    + Shock
                )
            )

        Parameters
        ----------
        random_shock:
            Z ~ N(0, 1)

        sector_drift:
            Macro movement affecting the stock's sector.

        external_shock:
            Event-driven price movement supplied by Module 5.

        Returns
        -------
        float
            The new stock price.
        """

        price_multiplier = (
            1.0
            + self.drift
            + self.volatility * random_shock
            + sector_drift
            + external_shock
        )

        new_price = self.price * price_multiplier

        # README specifies a minimum price of 1.0.
        self.price = max(1.0, new_price)

        return self.price