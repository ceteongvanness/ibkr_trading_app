from datetime import datetime, time, timedelta
import pytz

class TradingHours:
    def __init__(self):
        self.et_timezone = pytz.timezone('US/Eastern')
        self.market_open = time(9, 30)  # 9:30 AM ET
        self.market_close = time(16, 0)  # 4:00 PM ET

    def is_trading_day(self) -> bool:
        """Check if today is a trading day (Monday-Friday)"""
        et_now = datetime.now(self.et_timezone)
        return et_now.weekday() < 5  # 0-4 represents Monday-Friday

    def is_market_open(self) -> bool:
        """Check if market is currently open"""
        et_now = datetime.now(self.et_timezone)
        current_time = et_now.time()
        
        return (
            self.is_trading_day() and
            self.market_open <= current_time < self.market_close
        )

    def time_until_market_open(self) -> int:
        """Get seconds until market opens"""
        et_now = datetime.now(self.et_timezone)
        current_time = et_now.time()
        
        if current_time < self.market_open:
            # Market opens today
            market_open = datetime.combine(et_now.date(), self.market_open)
            market_open = self.et_timezone.localize(market_open)
            return int((market_open - et_now).total_seconds())
        else:
            # Market opens next trading day
            next_day = et_now + timedelta(days=1)
            while next_day.weekday() >= 5:  # Skip weekends
                next_day += timedelta(days=1)
            market_open = datetime.combine(next_day.date(), self.market_open)
            market_open = self.et_timezone.localize(market_open)
            return int((market_open - et_now).total_seconds())

    def time_until_market_close(self) -> int:
        """Get seconds until market closes"""
        et_now = datetime.now(self.et_timezone)
        market_close = datetime.combine(et_now.date(), self.market_close)
        market_close = self.et_timezone.localize(market_close)
        return int((market_close - et_now).total_seconds())