from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True)
class MarketConfig:
    """
    Configuration for the synthetic market.
    """

    initial_price: float = 100.0
    drift: float = 0.0001
    volatility: float = 0.01

    sector_drifts: Dict[str, float] = field(
        default_factory=lambda: {
            "TECH": 0.0,
            "FINANCE": 0.0,
            "ENERGY": 0.0,
        }
    )

    def __post_init__(self):
        if self.initial_price <= 0:
            raise ValueError("Initial price must be positive.")

        if self.volatility < 0:
            raise ValueError("Volatility cannot be negative.")

        if self.drift < -1:
            raise ValueError("Drift is too negative.")