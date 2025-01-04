from typing import Optional
import sys
import os
from datetime import datetime
from .trading.market import MarketData
from .trading.order import OrderManager
from .utils.logger import setup_logger
from .utils.reporter import Reporter
from .utils.screenshotter import Screenshotter
from .utils.trading_hours import TradingHours
from .utils.email_sender import EmailSender
from .exceptions.trading_exceptions import TradingException

class TradingApp:
    def __init__(self):
        self.logger = setup_logger("trading_app")
        self.market = MarketData()
        self.order_manager = OrderManager()
        self.reporter = Reporter()
        self.screenshotter = Screenshotter()
        self.trading_hours = TradingHours()
        self.email_sender = EmailSender()
        self.spx_base_price: Optional[float] = None
        self.trading_summary = {
            'total_trades': 0,
            'spx_base_price': None,
            'spx_final_price': None,
            'total_spx_drop': 0,
            'symbol': None,
            'entry_price': None,
            'trading_mode': None
        }

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
            self.trading_summary['spx_base_price'] = self.spx_base_price
            self.logger.info(f"SPX base price set: ${self.spx_base_price}")
        
        current_price = self.market.get_market_price("SPX")
        if current_price and self.spx_base_price:
            drop = ((self.spx_base_price - current_price) / self.spx_base_price) * 100
            self.logger.info(f"SPX Drop: {drop:.2f}%")
            return drop
        return 0.0

    def handle_market_closed(self) -> bool:
        """Handle market closed situation. Returns True if should continue, False if should exit"""
        wait_time = self.trading_hours.time_until_market_open()
        hours = wait_time // 3600
        minutes = (wait_time % 3600) // 60
        
        print(f"\nMarket is currently closed.")
        print(f"Time until market opens: {hours} hours and {minutes} minutes")
        print("\nOptions:")
        print("1. Wait for market to open")
        print("2. Exit application")
        
        while True:
            choice = input("\nEnter your choice (1 or 2): ")
            if choice == "1":
                self.logger.info(f"Waiting {hours} hours and {minutes} minutes until market opens")
                return True
            elif choice == "2":
                self.logger.info("User chose to exit during market closed period")
                return False
            else:
                print("Invalid choice. Please enter 1 or 2.")

    def send_trading_report(self) -> None:
        """Generate and send trading report via email"""
        try:
            # Update final SPX price
            current_spx = self.market.get_market_price("SPX")
            if current_spx and self.spx_base_price:
                self.trading_summary['spx_final_price'] = current_spx
                self.trading_summary['total_spx_drop'] = (
                    (self.spx_base_price - current_spx) / self.spx_base_price * 100
                )

            # Generate reports
            report_paths = self.reporter.generate_report()
            
            # Get recipient email from environment variable
            recipient_email = os.getenv('TRADING_REPORT_EMAIL')
            if not recipient_email:
                self.logger.error("No recipient email configured")
                return

            # Send email with report
            if self.email_sender.send_report(recipient_email, report_paths, self.trading_summary):
                self.logger.info(f"Trading report sent to {recipient_email}")
            else:
                self.logger.error("Failed to send trading report")
                
        except Exception as e:
            self.logger.error(f"Error sending trading report: {str(e)}")

    def execute_trade(self, symbol: str, drop_level: int) -> bool:
        """Execute trade based on SPX drop level"""
        try:
            # Check if market is open
            if not self.trading_hours.is_market_open():
                self.logger.warning("Cannot execute trade - Market is closed")
                return False

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
                # Update trading summary
                self.trading_summary['total_trades'] += 1
                self.trading_summary['entry_price'] = price
                self.trading_summary['symbol'] = symbol
                
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
            self.trading_summary['trading_mode'] = 'Live' if mode == '1' else 'Paper'
            
            # Connect to server
            if not self.connect_to_server(port):
                self.logger.error("Failed to connect to IBKR")
                return
            
            # Get symbol
            symbol = input("\nEnter stock symbol (e.g., MSFT): ").upper()
            self.trading_summary['symbol'] = symbol
            
            # Main monitoring loop
            while True:
                try:
                    # Check if market is open
                    if not self.trading_hours.is_market_open():
                        # Send report when market closes
                        self.send_trading_report()
                        if not self.handle_market_closed():
                            print("\nExiting application due to closed market.")
                            break
                        self.market.sleep(min(self.trading_hours.time_until_market_open(), 3600))
                        continue

                    # Monitor SPX
                    spx_drop = self.monitor_spx()
                    
                    # Check trading conditions
                    if spx_drop >= 40:
                        print(f"SPX dropped {spx_drop:.2f}%. Executing 40% strategy...")
                        if self.execute_trade(symbol, 40):
                            self.logger.info("Successfully executed 40% drop strategy")
                        break
                    elif spx_drop >= 30:
                        print(f"SPX dropped {spx_drop:.2f}%. Executing 30% strategy...")
                        if self.execute_trade(symbol, 30):
                            self.logger.info("Successfully executed 30% drop strategy")
                        break
                    elif spx_drop >= 20:
                        print(f"SPX dropped {spx_drop:.2f}%. Executing 20% strategy...")
                        if self.execute_trade(symbol, 20):
                            self.logger.info("Successfully executed 20% drop strategy")
                        break
                    elif spx_drop >= 10:
                        print(f"SPX dropped {spx_drop:.2f}%. Executing 10% strategy...")
                        if self.execute_trade(symbol, 10):
                            self.logger.info("Successfully executed 10% drop strategy")
                        break
                    
                    # Calculate time until market close
                    time_to_close = self.trading_hours.time_until_market_close()
                    if time_to_close <= 0:
                        print("\nMarket is closing. Ending monitoring session.")
                        # Send final report
                        self.send_trading_report()
                        break

                    # Wait before next check
                    wait_time = min(60, time_to_close)  # Wait 1 minute or until market close
                    self.market.sleep(wait_time)
                    
                    # Ask to continue
                    if input("\nContinue monitoring? (y/n): ").lower() != 'y':
                        # Send report before exiting
                        self.send_trading_report()
                        break
                
                except KeyboardInterrupt:
                    print("\nMonitoring interrupted by user")
                    # Send report on manual exit
                    self.send_trading_report()
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