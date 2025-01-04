from pathlib import Path
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)

def load_env_variables():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent.parent.parent / '.env'
    
    if not env_path.exists():
        template_path = Path(__file__).parent.parent.parent / '.env.template'
        if template_path.exists():
            logger.warning(
                f"No .env file found. Please copy .env.template to .env "
                f"and fill in your values."
            )
        else:
            logger.error("Neither .env nor .env.template found!")
        return False
    
    load_dotenv(env_path)
    
    # Verify required variables
    required_vars = [
        'TRADING_EMAIL',
        'TRADING_EMAIL_PASSWORD',
        'TRADING_REPORT_EMAIL'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        return False
        
    return True