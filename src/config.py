from pathlib import Path
from dataclasses import dataclass
from typing import List

@dataclass
class TradingConfig:
    # Connection settings
    HOST: str = "127.0.0.1"
    LIVE_PORT: int = 7496
    PAPER_PORT: int = 7497
    CLIENT_ID: int = 1

    # Trading parameters
    RESERVE_PERCENTAGE: float = 50.0  # Keep 50% of funds in reserve
    SPX_DROP_LEVELS: List[int] = (10, 20, 30, 40)  # type: ignore
    PRICE_CHECK_THRESHOLD: float = 10.0  # 10% threshold for price reasonability

    # File paths
    BASE_DIR: Path = Path(__file__).parent.parent
    LOGS_DIR: Path = BASE_DIR / "logs"
    SCREENSHOTS_DIR: Path = BASE_DIR / "trading_records" / "screenshots"
    REPORTS_DIR: Path = BASE_DIR / "trading_records" / "reports"

    # Ensure directories exist
    def __post_init__(self):
        self.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        self.SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        self.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        # Convert tuple to list for SPX_DROP_LEVELS
        self.SPX_DROP_LEVELS = list(self.SPX_DROP_LEVELS)