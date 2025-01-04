from typing import Optional
import sys
from trading.market import MarketData
from trading.order import OrderManager
from utils.logger import setup_logger
from utils.reporter import Reporter
from utils.screenshotter import Screenshotter
from exceptions.trading_exceptions import TradingException
from config import TradingConfig

class TradingApp:
    def __init__(self):
        self.logger = setup_logger("trading_app")
        self.config = TradingConfig()
        self.market = MarketData()
        self.order_manager = OrderManager()
        self.reporter = Reporter()
        self.screenshotter = Screenshotter()
        self.spx_base_price: Optional[float] = None

    def connect_to_server(self, port: int) -> bool:
        """Connect to IBKR server"""
        try:
            success = self.market.connect(port)
            if success:
                self.logger.info(f"Connected to IBKR on port {port}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Connection error: {str(e)}")
            return False

    def check_connection(self) -> bool:
        """Verify connection status"""
        return self.market.is_connected()

    def monitor_spx(self) -> float:
        """Monitor SPX price and calculate drop percentage"""
        if self.spx_base_price is None:
            self.spx_base_price = self.market.get_market_price("SPX")
            self.logger.info(f"SPX base price set: ${self.spx_base_price}")
        
        current_price = self.market.get_market_price("SPX")
        if current_price and self.spx_base_price:
            drop = ((self.spx_base_price - current_price) / self.spx_base_price) * 100
            self.logger.info(f"SPX Drop: {drop:.2f}%")
            return drop
        return 0.0

    def execute_trade(self, symbol: str, drop_level: int) -> bool:
        """Execute trade based on SPX drop level"""
        try:
            # Check account balance
            if not self.order_manager.check_sufficient_funds():
                self.logger.warning("Insufficient funds for trade")
                return False

            # Get current price
            price = self.market.get_market_price(symbol)
            if not price:
                self.logger.error("Could not get current price")
                return False

            # Execute order
            success = self.order_manager.place_buy_order(symbol, 1, price)
            if success:
                # Take screenshot
                screenshot_path = self.screenshotter.capture(symbol)
                
                # Record transaction
                self.reporter.record_transaction(
                    symbol=symbol,
                    price=price,
                    quantity=1,
                    spx_drop=drop_level,
                    screenshot_path=screenshot_path
                )
                return True
            
            return False

        except TradingException as e:
            self.logger.error(f"Trading error: {str(e)}")
            return False

    def run(self):
        """Main trading loop"""
        try:
            # Get trading mode
            print("\nSelect trading mode:")
            print("1. Live Trading (Port 7496)")
            print("2. Paper Trading (Port 7497)")
            
            while True:
                mode = input("Enter choice (1 or 2): ")
                if mode in ['1', '2']:
                    break
                print("Invalid choice. Please enter 1 or 2.")
            
            port = 7496 if mode == "1" else 7497
            
            # Connect to server
            if not self.connect_to_server(port):
                self.logger.error("Failed to connect to IBKR")
                return
            
            # Get symbol
            symbol = input("\nEnter stock symbol (e.g., MSFT): ").upper()
            
            # Main monitoring loop
            while True:
                try:
                    # Monitor SPX
                    spx_drop = self.monitor_spx()
                    
                    # Check trading conditions
                    if spx_drop >= 40:
                        print(f"SPX dropped {spx_drop:.2f}%. Executing 40% strategy...")
                        self.execute_trade(symbol, 40)
                        break
                    elif spx_drop >= 30:
                        print(f"SPX dropped {spx_drop:.2f}%. Executing 30% strategy...")
                        self.execute_trade(symbol, 30)
                        break
                    elif spx_drop >= 20:
                        print(f"SPX dropped {spx_drop:.2f}%. Executing 20% strategy...")
                        self.execute_trade(symbol, 20)
                        break
                    elif spx_drop >= 10:
                        print(f"SPX dropped {spx_drop:.2f}%. Executing 10% strategy...")
                        self.execute_trade(symbol, 10)
                        break
                    
                    # Wait before next check
                    self.market.sleep(60)
                    
                    # Ask to continue
                    if input("\nContinue monitoring? (y/n): ").lower() != 'y':
                        break
                
                except KeyboardInterrupt:
                    print("\nMonitoring interrupted by user")
                    break
                    
        except Exception as e:
            self.logger.error(f"Application error: {str(e)}")
        
        finally:
            self.market.disconnect()
            self.reporter.generate_report()

def main():
    app = TradingApp()
    app.run()

if __name__ == "__main__":
    main()