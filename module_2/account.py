class Account:
    def __init__(self,user_id: str, starting_cash: float=10000.0):
        self.user_id=user_id
        self.cash=starting_cash
        self.holdings={}
    def net_worth(self, current_prices: dict) ->float:
        holdings_value=0
        for symbol, quantity in self.holdings.items():
            price = current_prices[symbol]
            holdings_value+=quantity*price
        return self.cash+holdings_value
    

