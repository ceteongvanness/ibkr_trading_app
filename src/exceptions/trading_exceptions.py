"""Trading application exceptions"""

class TradingException(Exception):
    """Base exception for trading application"""
    pass

class MarketDataException(TradingException):
    """Exception raised for market data related errors"""
    pass

class OrderException(TradingException):
    """Exception raised for order related errors"""
    pass

class ConnectionException(TradingException):
    """Exception raised for connection related errors"""
    pass

class ConfigurationException(TradingException):
    """Exception raised for configuration related errors"""
    pass

class ReportingException(TradingException):
    """Exception raised for reporting related errors"""
    pass

class InsufficientFundsException(TradingException):
    """Exception raised when there are insufficient funds for trading"""
    pass

class InvalidSymbolException(TradingException):
    """Exception raised when an invalid symbol is provided"""
    pass

class PriceValidationException(TradingException):
    """Exception raised when price validation fails"""
    pass
