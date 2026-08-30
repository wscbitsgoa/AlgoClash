from account import Account
from execution_engine import execute_order

def test_buy_success():
    alice = Account("alice")
    prices = {"STK_1": 50}

    result = execute_order(alice, "STK_1", 10, "BUY", prices)

    assert result.success
    assert alice.cash == 9500
    assert alice.holdings["STK_1"] == 10

def test_buy_insufficient_cash():
    alice = Account("alice", starting_cash=100)
    prices = {"STK_1": 50}

    result = execute_order(alice, "STK_1", 10, "BUY", prices)

    assert not result.success
    assert alice.cash == 100  # unchanged

def test_sell_insufficient_holdings():
    alice = Account("alice")
    prices = {"STK_1": 50}

    result = execute_order(alice, "STK_1", 5, "SELL", prices)

    assert not result.success

def test_unknown_symbol():
    alice = Account("alice")
    prices = {"STK_1": 50}

    result = execute_order(alice, "STK_2", 5, "SELL", prices)

    assert not result.success
    assert "Unknown symbol" in result.message