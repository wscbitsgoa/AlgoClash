import pytest

from src.market.config import MarketConfig
from src.market.market import Market
from src.market.stock import Stock


def test_market_contains_15_stocks():
    market = Market(seed=42)

    assert len(market.stocks) == 15


def test_market_contains_three_sectors():
    market = Market(seed=42)

    sectors = {
        stock.sector
        for stock in market.stocks.values()
    }

    assert sectors == {
        "TECH",
        "FINANCE",
        "ENERGY",
    }


def test_each_sector_contains_five_stocks():
    market = Market(seed=42)

    for sector in ["TECH", "FINANCE", "ENERGY"]:
        stocks = market.get_sector_prices(sector)

        assert len(stocks) == 5


def test_initial_prices_are_correct():
    config = MarketConfig(initial_price=100.0)
    market = Market(config=config, seed=42)

    for stock in market.stocks.values():
        assert stock.price == 100.0


def test_price_never_falls_below_one():
    stock = Stock(
        symbol="TEST",
        sector="TECH",
        price=100.0,
        drift=0.0,
        volatility=100.0,
    )

    stock.update_price(
        random_shock=-100.0,
        sector_drift=0.0,
        external_shock=0.0,
    )

    assert stock.price >= 1.0


def test_market_price_changes():
    market = Market(seed=42)

    before = market.get_prices()

    market.update()

    after = market.get_prices()

    assert before != after


def test_zero_volatility_and_zero_drift_produces_constant_price():
    config = MarketConfig(
        initial_price=100.0,
        drift=0.0,
        volatility=0.0,
    )

    market = Market(
        config=config,
        seed=42,
    )

    before = market.get_prices()

    market.update()

    after = market.get_prices()

    assert before == after


def test_positive_sector_drift_increases_price():
    config = MarketConfig(
        initial_price=100.0,
        drift=0.0,
        volatility=0.0,
        sector_drifts={
            "TECH": 0.10,
            "FINANCE": 0.0,
            "ENERGY": 0.0,
        },
    )

    market = Market(
        config=config,
        seed=42,
    )

    market.update()

    for symbol in [
        "STK_1",
        "STK_2",
        "STK_3",
        "STK_4",
        "STK_5",
    ]:
        assert market.get_stock(symbol).price == pytest.approx(110.0)

    for symbol in [
        "STK_6",
        "STK_7",
        "STK_8",
        "STK_9",
        "STK_10",
        "STK_11",
        "STK_12",
        "STK_13",
        "STK_14",
        "STK_15",
    ]:
        assert market.get_stock(symbol).price == pytest.approx(100.0)


def test_stock_specific_shock():
    config = MarketConfig(
        initial_price=100.0,
        drift=0.0,
        volatility=0.0,
    )

    market = Market(
        config=config,
        seed=42,
    )

    market.update(
        shocks={
            "STK_1": -0.20
        }
    )

    assert market.get_stock("STK_1").price == pytest.approx(80.0)

    assert market.get_stock("STK_2").price == pytest.approx(100.0)


def test_sector_shock():
    config = MarketConfig(
        initial_price=100.0,
        drift=0.0,
        volatility=0.0,
    )

    market = Market(
        config=config,
        seed=42,
    )

    market.update(
        shocks={
            "TECH": -0.20
        }
    )

    for symbol in [
        "STK_1",
        "STK_2",
        "STK_3",
        "STK_4",
        "STK_5",
    ]:
        assert market.get_stock(symbol).price == pytest.approx(80.0)

    assert market.get_stock("STK_6").price == pytest.approx(100.0)


def test_market_wide_shock():
    config = MarketConfig(
        initial_price=100.0,
        drift=0.0,
        volatility=0.0,
    )

    market = Market(
        config=config,
        seed=42,
    )

    market.update(
        shocks={
            "ALL": -0.20
        }
    )

    for stock in market.stocks.values():
        assert stock.price == pytest.approx(80.0)


def test_reproducible_simulation_with_seed():
    market_a = Market(seed=123)
    market_b = Market(seed=123)

    for _ in range(10):
        prices_a = market_a.update()
        prices_b = market_b.update()

        assert prices_a == prices_b


def test_reset():
    market = Market(seed=42)

    market.update()

    market.reset()

    assert market.tick == 0

    for stock in market.stocks.values():
        assert stock.price == 100.0