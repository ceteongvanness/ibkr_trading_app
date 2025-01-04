import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import os

class EmailSender:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        sender_email = os.getenv('TRADING_EMAIL')
        sender_password = os.getenv('TRADING_EMAIL_PASSWORD')
        
        if not sender_email or not sender_password:
            raise ValueError("Email credentials not found in environment variables")
            
        self.sender_email: str = sender_email
        self.sender_password: str = sender_password

    def send_report(self, recipient_email: str, report_paths: List[Path], trading_summary: Dict) -> bool:
        """Send trading report via email"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email  # Now self.sender_email is definitely str
            msg['To'] = recipient_email
            msg['Subject'] = f"Trading Report - {datetime.now().strftime('%Y-%m-%d')}"

            # Create email body with trading summary
            body = self._create_email_body(trading_summary)
            msg.attach(MIMEText(body, 'html'))

            # Attach reports
            for report_path in report_paths:
                if report_path.exists():
                    with open(report_path, 'rb') as file:
                        attachment = MIMEApplication(file.read(), _subtype="csv")
                        attachment.add_header(
                            'Content-Disposition', 
                            'attachment', 
                            filename=report_path.name
                        )
                        msg.attach(attachment)

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            return True

        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False

    def _create_email_body(self, trading_summary: Dict) -> str:
        """Create HTML email body with trading summary"""
        return f"""
        <html>
        <body>
            <h2>Trading Report Summary</h2>
            <p>Date: {datetime.now().strftime('%Y-%m-%d')}</p>
            
            <h3>Trading Summary:</h3>
            <ul>
                <li>Total Trades: {trading_summary.get('total_trades', 0)}</li>
                <li>SPX Base Price: ${trading_summary.get('spx_base_price', 0):.2f}</li>
                <li>SPX Final Price: ${trading_summary.get('spx_final_price', 0):.2f}</li>
                <li>Total SPX Drop: {trading_summary.get('total_spx_drop', 0):.2f}%</li>
            </ul>

            <h3>Trading Details:</h3>
            <ul>
                <li>Symbol: {trading_summary.get('symbol', 'N/A')}</li>
                <li>Entry Price: ${trading_summary.get('entry_price', 0):.2f}</li>
                <li>Trading Mode: {trading_summary.get('trading_mode', 'N/A')}</li>
            </ul>

            <p>Please find the detailed reports attached.</p>
            
            <p>Best regards,<br>IBKR Trading Bot</p>
        </body>
        </html>
        """