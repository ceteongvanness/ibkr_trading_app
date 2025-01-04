# IBKR Trading App

An automated trading application that connects to Interactive Brokers (IBKR) for executing trades based on SPX movements. The application features automatic screenshot capture, detailed reporting, and intelligent trade execution based on market conditions.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

## 🚀 Features

### Trading Capabilities
- Live and Paper trading support through IBKR API
- SPX-based trading strategy with multiple entry points:
  - 10% SPX drop trigger
  - 20% SPX drop trigger
  - 30% SPX drop trigger
  - 40% SPX drop trigger
- Intelligent price reasonability checks
- Automatic money management with 50% reserve maintenance

### Monitoring & Recording
- Real-time market data monitoring
- Automatic screenshot capture of trades
- Comprehensive transaction reporting:
  - CSV reports for data analysis
  - HTML reports with embedded screenshots
- Detailed logging system

### Safety Features
- Connection status verification
- Price validation
- Account balance monitoring
- Trade execution confirmation

## 📋 Prerequisites

- Python 3.8 or higher
- Interactive Brokers Workstation (IBW) or IB Gateway
- IBKR account (paper or live trading)
- Sufficient system permissions for screenshot capture

## 🔧 Installation

1. **Clone the repository**
```bash
git clone https://github.com/ceteongvanness/ibkr-trading-app.git
cd ibkr-trading-app
```

2. **Set up virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Install development dependencies** (optional)
```bash
pip install -r requirements-dev.txt
```

## ⚙️ Configuration

1. **IBKR Workstation/Gateway Setup**
   - Ensure IBKR Workstation or Gateway is running
   - Configure API settings in TWS:
     - File -> Global Configuration -> API -> Settings
     - Enable "Enable ActiveX and Socket Clients"
     - Set appropriate port numbers

2. **Port Configuration**
   - Live Trading: 7496 (default)
   - Paper Trading: 7497 (default)

## 🚦 Usage

1. **Start the application**
```bash
python -m src.app
```

2. **Follow the interactive prompts**
   - Select trading mode (live/paper)
   - Enter stock symbol for monitoring
   - Configure SPX monitoring parameters (optional)

### Trading Process

1. **Connection & Setup**
   - Application connects to IBKR
   - Verifies connection status
   - Validates trading environment

2. **Stock Selection**
   - Enter stock symbol
   - Price reasonability check
   - Current market conditions analysis

3. **SPX Monitoring**
   - Continuous monitoring of SPX movements
   - Trigger evaluation for different drop levels
   - Account balance verification

4. **Trade Execution**
   - Automatic order placement when conditions met
   - Screenshot capture
   - Transaction recording
   - Report generation

## 📁 Project Structure

```
ibkr_trading_app/
├── LICENSE                    # MIT License file for the project
├── README.md                  # Project documentation and setup instructions
├── requirements.txt          # Production dependencies (ib_insync, pandas, etc.)
├── requirements-dev.txt      # Development dependencies (pytest, black, etc.)
├── run.py                    # Executable script to start the application
├── setup.py                  # Package installation and distribution settings
├── setup.cfg                 # Additional package configuration settings
├── .gitignore               # Specifies which files Git should ignore
│
├── .vscode/                  # VS Code specific settings
│   └── settings.json        # Editor configurations for Python
│
├── pyrightconfig.json       # Python type checking configuration
│
├── src/                     # Main source code directory
│   ├── __init__.py         # Makes src a Python package, exports main classes
│   ├── main.py             # Application entry point
│   ├── app.py              # Main application logic and trading workflow
│   ├── config.py           # Configuration settings (ports, paths, etc.)
│   │
│   ├── trading/            # Trading-related functionality
│   │   ├── __init__.py     # Package initialization
│   │   ├── market.py       # Market data handling (prices, connections)
│   │   └── order.py        # Order management and execution
│   │
│   ├── utils/              # Utility functions and helper classes
│   │   ├── __init__.py     # Package initialization
│   │   ├── logger.py       # Logging configuration and setup
│   │   ├── reporter.py     # Trade reporting and analysis
│   │   └── screenshotter.py # Screenshot capture functionality
│   │
│   └── exceptions/         # Custom exception definitions
│       ├── __init__.py     # Package initialization
│       └── trading_exceptions.py # Trading-specific exceptions
│
├── logs/                   # Application logs directory
│   └── .gitkeep           # Maintains empty directory in Git
│
├── trading_records/        # Trading data and records
│   ├── screenshots/        # Trade screenshots storage
│   │   └── .gitkeep       # Maintains empty directory in Git
│   └── reports/           # Generated trade reports
│       └── .gitkeep       # Maintains empty directory in Git
│
└── venv/                  # Virtual environment (not in Git)
```

## 📊 Reports & Records

### Screenshots
- Location: `trading_records/screenshots/`
- Naming: `{symbol}_{timestamp}.png`
- Captures market conditions at trade execution

### Reports
- Location: `trading_records/reports/`
- Types:
  - CSV reports for data analysis
  - HTML reports with visual elements
- Content:
  - Transaction details
  - Price information
  - SPX conditions
  - Account balances
  - Screenshot references

## 🧪 Development

1. **Setup development environment**
```bash
pip install -r requirements-dev.txt
```

2. **Run tests**
```bash
pytest
```

3. **Code formatting**
```bash
black src/
flake8 src/
```

4. **Type checking**
```bash
mypy src/
```

## 🔍 Monitoring & Debugging

### Logging
- Location: `logs/` directory
- Levels: DEBUG, INFO, WARNING, ERROR
- Format: `timestamp - level - message`

### Error Handling
- Connection issues
- Data retrieval problems
- Order execution failures
- System errors

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This software is for educational purposes only. Trading carries significant financial risk, and users should carefully review all trading strategies before implementation. The authors take no responsibility for financial losses incurred through the use of this software.

## 🙏 Acknowledgments

- Interactive Brokers API Documentation
- Python `ib_insync` library maintainers
- Contributors to the project