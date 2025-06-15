import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings loaded from environment variables."""
    
    # Anthropic API Configuration
    ANTHROPIC_API_KEY: str = os.getenv('ANTHROPIC_API_KEY', '')
    
    # Reddit API Configuration
    REDDIT_CLIENT_ID: str = os.getenv('REDDIT_CLIENT_ID', '')
    REDDIT_CLIENT_SECRET: str = os.getenv('REDDIT_CLIENT_SECRET', '')
    REDDIT_USER_AGENT: str = os.getenv('REDDIT_USER_AGENT', '')
    REDDIT_USERNAME: str = os.getenv('REDDIT_USERNAME', '')
    REDDIT_PASSWORD: str = os.getenv('REDDIT_PASSWORD', '')
    
    # Twitter API Configuration
    TWITTER_API_KEY: str = os.getenv('TWITTER_API_KEY', '')
    TWITTER_API_SECRET: str = os.getenv('TWITTER_API_SECRET', '')
    TWITTER_BEARER_TOKEN: str = os.getenv('TWITTER_BEARER_TOKEN', '')
    TWITTER_ACCESS_TOKEN: str = os.getenv('TWITTER_ACCESS_TOKEN', '')
    TWITTER_ACCESS_TOKEN_SECRET: str = os.getenv('TWITTER_ACCESS_TOKEN_SECRET', '')
    
    @classmethod
    def validate(cls) -> None:
        """Validate that all required environment variables are set."""
        required_vars = [
            'ANTHROPIC_API_KEY',
            'REDDIT_CLIENT_ID',
            'REDDIT_CLIENT_SECRET',
            'REDDIT_USER_AGENT',
            'REDDIT_USERNAME',
            'REDDIT_PASSWORD',
            'TWITTER_API_KEY',
            'TWITTER_API_SECRET',
            'TWITTER_BEARER_TOKEN',
            'TWITTER_ACCESS_TOKEN',
            'TWITTER_ACCESS_TOKEN_SECRET'
        ]
        
        missing_vars = [var for var in required_vars if not getattr(cls, var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    @classmethod
    def get_reddit_config(cls) -> Dict[str, str]:
        """Get Reddit configuration as a dictionary."""
        return {
            'client_id': cls.REDDIT_CLIENT_ID,
            'client_secret': cls.REDDIT_CLIENT_SECRET,
            'user_agent': cls.REDDIT_USER_AGENT,
            'username': cls.REDDIT_USERNAME,
            'password': cls.REDDIT_PASSWORD
        }
    
    @classmethod
    def get_twitter_config(cls) -> Dict[str, str]:
        """Get Twitter configuration as a dictionary."""
        return {
            'api_key': cls.TWITTER_API_KEY,
            'api_secret': cls.TWITTER_API_SECRET,
            'bearer_token': cls.TWITTER_BEARER_TOKEN,
            'access_token': cls.TWITTER_ACCESS_TOKEN,
            'access_token_secret': cls.TWITTER_ACCESS_TOKEN_SECRET
        }

# Create a singleton instance
settings = Settings()

# Validate settings on import
settings.validate() 