# IBKR Trading App

An automated trading application that connects to Interactive Brokers (IBKR) for executing trades based on SPX movements. Features automatic trade execution, screenshot capture, and detailed reporting capabilities.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

## Features

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

## Prerequisites

- Python 3.8 or higher
- Interactive Brokers Workstation (IBW) or IB Gateway
- IBKR account (paper or live trading)
- Docker (for containerization)
- kubectl (for Kubernetes deployment)
- AWS CLI (for AWS deployment)

## Local Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ibkr_trading_app.git
cd ibkr_trading_app
```

2. Set up virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install development dependencies (optional):
```bash
pip install -r requirements-dev.txt
```

## Configuration

1. IBKR Workstation/Gateway Setup:
   - Launch TWS or IB Gateway
   - Configure API settings:
     - File → Global Configuration → API → Settings
     - Enable "Enable ActiveX and Socket Clients"
     - Set appropriate port numbers

2. Port Configuration:
   - Live Trading: 7496 (default)
   - Paper Trading: 7497 (default)

## Usage

### Local Run
```bash
python run.py
```

### Docker Run
```bash
# Build image
docker build -t ibkr-trading-app .

# Run container
docker run -d ibkr-trading-app
```

### Kubernetes Deployment
```bash
# Apply K8s manifests
kubectl apply -f kubernetes/deployment.yaml
```

## AWS Deployment

### Prerequisites
1. AWS CLI configured with appropriate credentials
2. EKS cluster created
3. ECR repository created

### Deployment Steps
1. Push to GitHub:
   - GitHub Actions will automatically:
     - Build Docker image
     - Push to ECR
     - Deploy to EKS

2. Monitor deployment:
```bash
kubectl get pods -n trading
kubectl logs -f deployment/ibkr-trading-app -n trading
```

## Project Structure

The project follows a modular structure:
```
ibkr_trading_app/
├── .github/                  # GitHub specific configurations
│   └── workflows/           # GitHub Actions workflows
│       └── deploy.yaml      # CI/CD pipeline configuration
│
├── kubernetes/              # Kubernetes manifests
│   └── deployment.yaml      # K8s deployment, service, and volume configs
│
├── src/                     # Main source code directory
│   ├── __init__.py         # Makes src a Python package
│   ├── main.py             # Application entry point
│   ├── app.py              # Main application logic with trading hours
│   ├── config.py           # Application configuration
│   │
│   ├── trading/            # Trading-related functionality
│   │   ├── __init__.py     # Package initialization
│   │   ├── market.py       # Market data handling
│   │   └── order.py        # Order management with type fixes
│   │
│   ├── utils/              # Utility functions
│   │   ├── __init__.py     # Package initialization
│   │   ├── logger.py       # Logging setup
│   │   ├── reporter.py     # Trade reporting
│   │   ├── screenshotter.py # Screenshot functionality
│   │   └── trading_hours.py # Market hours management
│   │
│   └── exceptions/         # Custom exceptions
│       ├── __init__.py     # Package initialization
│       └── trading_exceptions.py # Trading exceptions
│
├── logs/                   # Application logs
│   └── .gitkeep           # Git empty directory marker
│
├── trading_records/        # Trading data storage
│   ├── screenshots/        # Trade screenshots
│   │   └── .gitkeep       # Git empty directory marker
│   └── reports/           # Generated reports
│       └── .gitkeep       # Git empty directory marker
│
├── .vscode/               # VS Code settings
│   └── settings.json      # Editor configurations
│
├── tests/                 # Test directory
│   ├── __init__.py        # Test package initialization
│   ├── test_market.py     # Market module tests
│   └── test_order.py      # Order module tests
│
├── .gitignore            # Git ignore patterns
├── Dockerfile            # Docker container definition
├── LICENSE               # MIT License
├── README.md            # Project documentation
├── pyrightconfig.json   # Python type checking config
├── requirements.txt     # Production dependencies
├── requirements-dev.txt # Development dependencies
├── run.py              # Local run script
├── setup.cfg           # Package configuration
└── setup.py            # Package setup file
```

## Development

1. Setup development environment:
```bash
pip install -r requirements-dev.txt
```

2. Run tests:
```bash
pytest
```

3. Code formatting:
```bash
black src/
flake8 src/
```

## Monitoring & Debugging

### Logging
- Location: `logs/` directory
- Levels: DEBUG, INFO, WARNING, ERROR
- Format: `timestamp - level - message`

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

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This software is for educational purposes only. Trading carries significant financial risk, and users should carefully review all trading strategies before implementation. The authors take no responsibility for financial losses incurred through the use of this software.

## Acknowledgments

- Interactive Brokers API Documentation
- Python `ib_insync` library maintainers
- Contributors to the project