import tweepy
from typing import Optional, List, Dict, Any
from src.config.settings import settings
from src.utils.decorators import rate_limit, log_execution_time

class TwitterService:
    """Service for interacting with Twitter API."""
    
    def __init__(self):
        """Initialize Twitter service with configuration from settings."""
        config = settings.get_twitter_config()
        
        # Initialize API v1.1 client
        auth = tweepy.OAuthHandler(
            config['api_key'],
            config['api_secret']
        )
        auth.set_access_token(
            config['access_token'],
            config['access_token_secret']
        )
        self.api = tweepy.API(auth)
        
        # Initialize API v2 client
        self.client = tweepy.Client(
            bearer_token=config['bearer_token'],
            consumer_key=config['api_key'],
            consumer_secret=config['api_secret'],
            access_token=config['access_token'],
            access_token_secret=config['access_token_secret']
        )
    
    @rate_limit(calls=50, period=900)  # Twitter's rate limit
    @log_execution_time
    def create_tweet(self, text: str) -> Dict[str, Any]:
        """
        Create a new tweet.
        
        Args:
            text: Tweet content
            
        Returns:
            Dict containing tweet information
        """
        try:
            response = self.client.create_tweet(text=text)
            tweet = response.data
            return {
                'id': tweet['id'],
                'text': tweet['text'],
                'created_at': tweet['created_at']
            }
        except Exception as e:
            raise Exception(f"Failed to create tweet: {str(e)}")
    
    @rate_limit(calls=50, period=900)
    @log_execution_time
    def search_tweets(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search for tweets.
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of tweet information dictionaries
        """
        try:
            tweets = []
            for tweet in self.client.search_recent_tweets(
                query=query,
                max_results=max_results
            ).data or []:
                tweets.append({
                    'id': tweet.id,
                    'text': tweet.text,
                    'created_at': tweet.created_at
                })
            return tweets
        except Exception as e:
            raise Exception(f"Failed to search tweets: {str(e)}")
    
    @rate_limit(calls=50, period=900)
    @log_execution_time
    def get_user_info(self, username: str) -> Dict[str, Any]:
        """
        Get information about a Twitter user.
        
        Args:
            username: Twitter username
            
        Returns:
            Dict containing user information
        """
        try:
            user = self.client.get_user(username=username).data
            return {
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'description': user.description,
                'followers_count': user.public_metrics['followers_count'],
                'following_count': user.public_metrics['following_count']
            }
        except Exception as e:
            raise Exception(f"Failed to get user info: {str(e)}") 