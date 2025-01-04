import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Optional
from config import TradingConfig

class Reporter:
    def __init__(self):
        self.config = TradingConfig()
        self.transactions = []

    def record_transaction(
        self,
        symbol: str,
        price: float,
        quantity: int,
        spx_drop: float,
        screenshot_path: Optional[Path] = None
    ):
        """Record a trading transaction"""
        transaction = {
            'date': datetime.now(),
            'symbol': symbol,
            'price': price,
            'quantity': quantity,
            'total_cost': price * quantity,
            'spx_drop_percentage': spx_drop,
            'screenshot_path': str(screenshot_path) if screenshot_path else None
        }
        
        self.transactions.append(transaction)
        self._save_transaction(transaction)
        self.generate_report()

    def _save_transaction(self, transaction: dict):
        """Save individual transaction to CSV"""
        try:
            df = pd.DataFrame([transaction])
            csv_path = self.config.REPORTS_DIR / "transactions.csv"
            
            # Append or create new file
            if csv_path.exists():
                df.to_csv(csv_path, mode='a', header=False, index=False)
            else:
                df.to_csv(csv_path, index=False)
                
        except Exception as e:
            print(f"Error saving transaction: {str(e)}")

    def generate_report(self):
        """Generate HTML and CSV reports"""
        try:
            if not self.transactions:
                return

            # Create DataFrame
            df = pd.DataFrame(self.transactions)
            
            # Generate timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save CSV report
            csv_path = self.config.REPORTS_DIR / f"trading_report_{timestamp}.csv"
            df.to_csv(csv_path, index=False)
            
            # Generate HTML report
            html_content = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f5f5f5; }}
                    tr:nth-child(even) {{ background-color: #f9f9f9; }}
                    h1, h2 {{ color: #333; }}
                    .screenshot {{ max-width: 800px; margin: 10px 0; }}
                </style>
            </head>
            <body>
                <h1>Trading Report</h1>
                <h2>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h2>
                
                <h2>Transaction Summary</h2>
                {df.to_html(classes='table')}
                
                <h2>Screenshots</h2>
                {self._generate_screenshot_html()}
            </body>
            </html>
            """
            
            # Save HTML report
            html_path = self.config.REPORTS_DIR / f"trading_report_{timestamp}.html"
            with open(html_path, 'w') as f:
                f.write(html_content)
                
        except Exception as e:
            print(f"Error generating report: {str(e)}")

    def _generate_screenshot_html(self) -> str:
        """Generate HTML for screenshots"""
        html = ""
        for transaction in self.transactions:
            if transaction.get('screenshot_path'):
                html += f"""
                <div class="screenshot">
                    <h3>{transaction['symbol']} - {transaction['date'].strftime('%Y-%m-%d %H:%M:%S')}</h3>
                    <img src="{transaction['screenshot_path']}" alt="Trading Screenshot">
                </div>
                """
        return html