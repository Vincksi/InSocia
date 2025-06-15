import praw
from typing import Optional, List, Dict, Any
from src.config.settings import settings
from src.utils.decorators import rate_limit, log_execution_time

class RedditService:
    """Service for interacting with Reddit API."""
    
    def __init__(self):
        """Initialize Reddit service with configuration from settings."""
        config = settings.get_reddit_config()
        self.reddit = praw.Reddit(
            client_id=config['client_id'],
            client_secret=config['client_secret'],
            user_agent=config['user_agent'],
            username=config['username'],
            password=config['password']
        )
    
    @rate_limit(calls=30, period=60)  # Reddit's rate limit
    @log_execution_time
    def create_post(self, subreddit: str, title: str, content: str) -> Dict[str, Any]:
        """
        Create a post in a subreddit.
        
        Args:
            subreddit: Name of the subreddit
            title: Post title
            content: Post content
            
        Returns:
            Dict containing post information
        """
        try:
            subreddit_instance = self.reddit.subreddit(subreddit)
            post = subreddit_instance.submit(
                title=title,
                selftext=content
            )
            return {
                'id': post.id,
                'title': post.title,
                'url': post.url,
                'created_utc': post.created_utc
            }
        except Exception as e:
            raise Exception(f"Failed to create Reddit post: {str(e)}")
    
    @rate_limit(calls=30, period=60)
    @log_execution_time
    def get_subreddit_info(self, subreddit: str) -> Dict[str, Any]:
        """
        Get information about a subreddit.
        
        Args:
            subreddit: Name of the subreddit
            
        Returns:
            Dict containing subreddit information
        """
        try:
            subreddit_instance = self.reddit.subreddit(subreddit)
            return {
                'name': subreddit_instance.display_name,
                'description': subreddit_instance.description,
                'subscribers': subreddit_instance.subscribers,
                'created_utc': subreddit_instance.created_utc,
                'rules': [rule.short_name for rule in subreddit_instance.rules]
            }
        except Exception as e:
            raise Exception(f"Failed to get subreddit info: {str(e)}")
    
    @rate_limit(calls=30, period=60)
    @log_execution_time
    def search_posts(self, subreddit: str, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for posts in a subreddit.
        
        Args:
            subreddit: Name of the subreddit
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of post information dictionaries
        """
        try:
            subreddit_instance = self.reddit.subreddit(subreddit)
            posts = []
            for post in subreddit_instance.search(query, limit=limit):
                posts.append({
                    'id': post.id,
                    'title': post.title,
                    'url': post.url,
                    'score': post.score,
                    'created_utc': post.created_utc
                })
            return posts
        except Exception as e:
            raise Exception(f"Failed to search posts: {str(e)}") 