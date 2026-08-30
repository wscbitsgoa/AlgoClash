class OrderResult:
    def __init__(self, success: bool, message: str):
        self.success=success
        self.message=message

from account import Account

def execute_order(account: Account, symbol: str, quantity: int, side: str, current_prices: dict)-> OrderResult:
    if symbol not in current_prices:
        return OrderResult(False, f"Unknown symbol : {symbol}")
    if quantity<=0:
        return OrderResult(False, f"Quantity must be positive")
    price=current_prices[symbol]

    if side=="BUY":
        cost= quantity*price
        if cost>account.cash:
            return OrderResult(False,"Insufficient cash balance")
        account.cash-=cost
        account.holdings[symbol]=account.holdings.get(symbol,0)+quantity
        return OrderResult(True, f"Bought {quantity} {symbol} @ {price: .2f}")
    elif side=="SELL":
        held=account.holdings.get(symbol,0)
        if quantity>held:
            return OrderResult(False,"Insufficient Holdings")
        account.cash+= quantity*price
        account.holdings[symbol]=held-quantity
        return OrderResult(True, f"Sold {quantity} {symbol} @ {price: .2f}")
    else:
        return OrderResult(False,f"Invalid Side: {side}")




