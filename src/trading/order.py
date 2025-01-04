from typing import Optional, Dict, List
from ib_insync import IB, Stock, MarketOrder, AccountValue
from src.exceptions.trading_exceptions import OrderException

class OrderManager:
    def __init__(self):
        self.ib = IB()

    def check_sufficient_funds(self) -> bool:
        """Check if account has sufficient funds (50% reserve)"""
        try:
            # Explicitly type the account_summary
            account_summary: List[AccountValue] = self.ib.reqAccountSummary() or []
                
            for summary in account_summary:
                if summary.tag == "NetLiquidation":
                    total_funds = float(summary.value)
                    # Ensure we keep 50% in reserve
                    return total_funds * 0.5 >= 0
            return False
            
        except Exception as e:
            raise OrderException(f"Failed to check funds: {str(e)}")

    def get_available_funds(self) -> Optional[float]:
        """Get available funds for trading"""
        try:
            # Explicitly type the account_summary
            account_summary: List[AccountValue] = self.ib.reqAccountSummary() or []
                
            for summary in account_summary:
                if summary.tag == "NetLiquidation":
                    total_funds = float(summary.value)
                    return total_funds * 0.5  # Return available funds (50% of total)
            return None
            
        except Exception as e:
            raise OrderException(f"Failed to get available funds: {str(e)}")

    def place_buy_order(self, symbol: str, quantity: int, price: float) -> bool:
        """Place a buy order"""
        try:
            # Check available funds
            available_funds = self.get_available_funds()
            if not available_funds or available_funds < price * quantity:
                return False

            # Create contract and order
            contract = Stock(symbol, "SMART", "USD")
            self.ib.qualifyContracts(contract)
            order = MarketOrder("BUY", quantity)
            
            # Place order
            trade = self.ib.placeOrder(contract, order)
            self.ib.sleep(1)  # Wait for order processing
            
            # Check order status
            if trade.orderStatus.status == "Filled":
                return True
            return False
            
        except Exception as e:
            raise OrderException(f"Failed to place order: {str(e)}")

    def get_positions(self) -> Dict[str, float]:
        """Get current positions"""
        try:
            positions: Dict[str, float] = {}
            for position in self.ib.positions() or []:
                symbol = position.contract.symbol
                quantity = position.position
                positions[symbol] = quantity
            return positions
            
        except Exception as e:
            raise OrderException(f"Failed to get positions: {str(e)}")