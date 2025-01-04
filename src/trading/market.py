from typing import Optional
from ib_insync import IB, Stock, Index
from src.exceptions.trading_exceptions import MarketDataException

class MarketData:
    def __init__(self):
        self.ib = IB()

    def connect(self, port: int, host: str = "127.0.0.1", client_id: int = 1) -> bool:
        """Connect to IBKR"""
        try:
            self.ib.connect(host, port, clientId=client_id)
            return True
        except Exception as e:
            raise MarketDataException(f"Connection failed: {str(e)}")

    def disconnect(self):
        """Disconnect from IBKR"""
        if self.ib.isConnected():
            self.ib.disconnect()

    def is_connected(self) -> bool:
        """Check if connected to IBKR"""
        return self.ib.isConnected()

    def get_market_price(self, symbol: str) -> Optional[float]:
        """Get current market price for a symbol"""
        try:
            # Determine if symbol is SPX
            if symbol == "SPX":
                contract = Index(symbol, "CBOE", "USD")
            else:
                contract = Stock(symbol, "SMART", "USD")

            self.ib.qualifyContracts(contract)
            
            # Request market data
            ticker = self.ib.reqMktData(contract)
            self.ib.sleep(2)  # Wait for data
            
            if ticker.last:
                return ticker.last
            elif ticker.close:
                return ticker.close
            return None
            
        except Exception as e:
            raise MarketDataException(f"Failed to get market price: {str(e)}")

    def is_price_reasonable(self, symbol: str, price: float) -> bool:
        """Check if price is within reasonable range"""
        try:
            contract = Stock(symbol, "SMART", "USD")
            self.ib.qualifyContracts(contract)
            
            # Get historical data
            bars = self.ib.reqHistoricalData(
                contract,
                endDateTime="",
                durationStr="1 D",
                barSizeSetting="1 day",
                whatToShow="TRADES",
                useRTH=True
            )
            
            if not bars:
                return False
                
            previous_close = bars[-1].close
            price_diff_percentage = abs(price - previous_close) / previous_close * 100
            
            return price_diff_percentage <= 10
            
        except Exception as e:
            raise MarketDataException(f"Failed to check price: {str(e)}")

    def sleep(self, seconds: int):
        """Sleep while keeping connection alive"""
        self.ib.sleep(seconds)