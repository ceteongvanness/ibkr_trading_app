import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, TypedDict, NamedTuple
import os
import logging

logger = logging.getLogger(__name__)

class TradingSummaryRequired(TypedDict, total=True):
    # Required fields
    total_trades: int
    trading_mode: str
    symbol: str

class TradingSummary(TradingSummaryRequired, total=False):
    # Optional fields
    spx_base_price: Optional[float]
    spx_final_price: Optional[float]
    total_spx_drop: Optional[float]
    entry_price: Optional[float]

class SmtpConfig(NamedTuple):
    server: str = "smtp.gmail.com"
    port: int = 587

class EmailSender:
    def __init__(self, raise_on_missing_credentials: bool = False) -> None:
        self.smtp_config = SmtpConfig()
        self.trading_records_dir = Path("trading_records")
        
        # Initialize credentials
        sender_email = os.getenv('TRADING_EMAIL')
        sender_password = os.getenv('TRADING_EMAIL_PASSWORD')

        # Check if both credentials are present
        if not sender_email or not sender_password:
            msg = ("Email credentials not found. Set TRADING_EMAIL and TRADING_EMAIL_PASSWORD "
                  "environment variables to enable email reporting.")
            if raise_on_missing_credentials:
                raise ValueError(msg)
            logger.warning(msg)
            self.is_configured = False
            self.sender_email = None
            self.sender_password = None
        else:
            self.is_configured = True
            self.sender_email = sender_email
            self.sender_password = sender_password

    def _format_float(self, value: Optional[float], default: float = 0.0) -> str:
        """Format float value with proper handling of None"""
        if value is None:
            value = default
        return f"${value:.2f}"

    def _format_percentage(self, value: Optional[float], default: float = 0.0) -> str:
        """Format percentage with proper handling of None"""
        if value is None:
            value = default
        return f"{value:.2f}%"

    def _attach_trading_records(self, msg: MIMEMultipart) -> None:
        """Attach all files from trading_records directory"""
        # Attach files from screenshots directory
        screenshots_dir = self.trading_records_dir / "screenshots"
        if screenshots_dir.exists():
            for file_path in screenshots_dir.glob("*.*"):
                if file_path.name == '.gitkeep':
                    continue
                try:
                    with open(file_path, 'rb') as file:
                        attachment = MIMEApplication(file.read())
                        attachment.add_header(
                            'Content-Disposition', 
                            'attachment', 
                            filename=f'screenshots/{file_path.name}'
                        )
                        msg.attach(attachment)
                        logger.info(f"Attached screenshot: {file_path.name}")
                except Exception as e:
                    logger.error(f"Error attaching screenshot {file_path}: {str(e)}")

        # Attach files from reports directory
        reports_dir = self.trading_records_dir / "reports"
        if reports_dir.exists():
            for file_path in reports_dir.glob("*.*"):
                if file_path.name == '.gitkeep':
                    continue
                try:
                    with open(file_path, 'rb') as file:
                        attachment = MIMEApplication(file.read())
                        attachment.add_header(
                            'Content-Disposition', 
                            'attachment', 
                            filename=f'reports/{file_path.name}'
                        )
                        msg.attach(attachment)
                        logger.info(f"Attached report: {file_path.name}")
                except Exception as e:
                    logger.error(f"Error attaching report {file_path}: {str(e)}")

    def send_report(self, recipient_email: str, report_paths: List[Path], trading_summary: TradingSummary) -> bool:
        """Send trading report via email with all trading records"""
        if not self.is_configured or not self.sender_email or not self.sender_password:
            logger.warning("Email sender not configured. Skipping email report.")
            return False

        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = str(self.sender_email)
            msg['To'] = recipient_email
            msg['Subject'] = f"Trading Report - {datetime.now().strftime('%Y-%m-%d')}"

            # Create email body with trading summary
            body = self._create_email_body(trading_summary)
            msg.attach(MIMEText(body, 'html'))

            # Attach all trading records
            self._attach_trading_records(msg)

            # Send email
            with smtplib.SMTP(self.smtp_config.server, self.smtp_config.port) as server:
                server.starttls()
                assert self.sender_email is not None
                assert self.sender_password is not None
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            logger.info(f"Trading report sent to {recipient_email}")
            return True

        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False

    def _create_email_body(self, trading_summary: TradingSummary) -> str:
        """Create HTML email body with trading summary"""
        return f"""
        <html>
        <body>
            <h2>Trading Report Summary</h2>
            <p>Date: {datetime.now().strftime('%Y-%m-%d')}</p>
            
            <h3>Trading Summary:</h3>
            <ul>
                <li>Total Trades: {trading_summary['total_trades']}</li>
                <li>SPX Base Price: {self._format_float(trading_summary.get('spx_base_price'))}</li>
                <li>SPX Final Price: {self._format_float(trading_summary.get('spx_final_price'))}</li>
                <li>Total SPX Drop: {self._format_percentage(trading_summary.get('total_spx_drop'))}</li>
            </ul>

            <h3>Trading Details:</h3>
            <ul>
                <li>Symbol: {trading_summary['symbol']}</li>
                <li>Entry Price: {self._format_float(trading_summary.get('entry_price'))}</li>
                <li>Trading Mode: {trading_summary['trading_mode']}</li>
            </ul>

            <p>Please find the detailed reports and screenshots attached.</p>
            
            <p>Best regards,<br>IBKR Trading Bot</p>
        </body>
        </html>
        """