from typing import Optional
from ib_insync import IB, Stock, Index
from src.exceptions.trading_exceptions import MarketDataException
import time
import logging

logger = logging.getLogger(__name__)

class MarketData:
    def __init__(self):
        self.ib = IB()
        self.connection_timeout = 30  # 30 seconds timeout
        self.retry_interval = 5      # 5 seconds between retries
        self.max_retries = 3        # Maximum number of connection attempts

    def connect(self, port: int, host: str = "127.0.0.1", client_id: int = 1) -> bool:
        """Connect to IBKR with retries"""
        for attempt in range(self.max_retries):
            try:
                # Try to disconnect if there's an existing connection
                if self.ib.isConnected():
                    self.ib.disconnect()
                    time.sleep(1)  # Wait a bit before reconnecting
                
                # Attempt connection with timeout
                self.ib.connect(
                    host=host,
                    port=port,
                    clientId=client_id,
                    timeout=self.connection_timeout
                )
                
                # Wait for connection to stabilize
                time.sleep(1)
                
                # Enable delayed market data
                self.ib.reqMarketDataType(3)  # 3 = Delayed data
                logger.info("Enabled delayed market data")
                
                # Verify connection
                if self.ib.isConnected():
                    print(f"Successfully connected to IBKR on port {port}")
                    return True
                    
            except Exception as e:
                print(f"Connection attempt {attempt + 1} failed: {str(e)}")
                if attempt < self.max_retries - 1:  # Don't sleep on last attempt
                    print(f"Retrying in {self.retry_interval} seconds...")
                    time.sleep(self.retry_interval)
                    
        raise MarketDataException("Failed to connect after all retry attempts")

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
            if not self.is_connected():
                raise MarketDataException("Not connected to IBKR")

            # Create contract based on symbol type
            if symbol == "SPX":
                contract = Index('SPX', 'CBOE', 'USD')
                logger.info("Created SPX index contract")
            else:
                contract = Stock(symbol, "SMART", "USD")
                logger.info(f"Created stock contract for {symbol}")

            self.ib.qualifyContracts(contract)
            
            # Request market data with timeout
            ticker = self.ib.reqMktData(contract)
            timeout_time = time.time() + 10  # 10 seconds timeout
            
            while time.time() < timeout_time:
                self.ib.sleep(0.1)  # Small sleep to prevent CPU spinning
                
                # For indices, try last price first, then close
                if symbol == "SPX":
                    if ticker.last:
                        logger.info(f"Got last price for SPX: {ticker.last}")
                        return ticker.last
                    elif ticker.close:
                        logger.info(f"Got close price for SPX: {ticker.close}")
                        return ticker.close
                # For stocks, try different price types
                else:
                    price = (ticker.last or ticker.close or 
                            ticker.bid or ticker.ask or ticker.high or ticker.low)
                    if price:
                        logger.info(f"Got price for {symbol}: {price}")
                        return price
            
            raise MarketDataException(f"Timeout waiting for market data for {symbol}")
            
        except Exception as e:
            raise MarketDataException(f"Failed to get market price: {str(e)}")

    def sleep(self, seconds: int):
        """Sleep while keeping connection alive"""
        self.ib.sleep(seconds)