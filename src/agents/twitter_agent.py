# Standard library imports
import tweepy
import logging
from typing import Dict, Any, List

# Third-party imports
import backoff
from smolagents import tool

# Local imports
from src.config.settings import settings
from src.agents.base_agent import BaseAgent
from src.services.twitter_service import TwitterService
from src.utils.decorators import log_execution_time, rate_limit

# Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@tool
@backoff.on_exception(backoff.expo, tweepy.TweepyException, max_tries=3)
@rate_limit(calls=50, period=900)  # 50 tweets per 15 minutes (Twitter's limit)
def post_tweet(text: str) -> Dict[str, Any]:
    """
    Post a tweet to Twitter.

    Args:
        text: The text content of the tweet (max 280 characters)
    
    Returns:
        dict: Contains success status, tweet ID, and URL if successful
    """
    try:
        if not text or len(text.strip()) == 0:
            raise ValueError("Tweet text cannot be empty")
        
        if len(text) > 280:
            text = text[:277] + "..."
            logger.warning(f"Tweet text was truncated to 280 characters")
        
        client = get_twitter_client()
        response = client.create_tweet(text=text)
        
        result = {
            "success": True,
            "tweet_id": response.data['id'],
            "text": text,
            "url": f"https://twitter.com/user/status/{response.data['id']}"
        }
        
        logger.info(f"Tweet posted successfully: {result['url']}")
        return result
        
    except Exception as e:
        logger.error(f"Error posting tweet: {str(e)}")
        return {"success": False, "error": str(e)}

@tool
@backoff.on_exception(backoff.expo, tweepy.TweepyException, max_tries=3)
@rate_limit(calls=900, period=900)  # 900 requests per 15 minutes
def get_user_timeline(username: str, count: int = 5) -> Dict[str, Any]:
    """
    Get recent tweets from a user's timeline.

    Args:
        username: Twitter username (without @)
        count: Number of tweets to retrieve (max 100)
    
    Returns:
        dict: Contains user info and list of recent tweets
    """
    try:
        if not username:
            raise ValueError("Username is required")
            
        count = min(max(1, count), 100)  # Ensure count is between 1 and 100
        
        client = get_twitter_client()
        user = client.get_user(username=username)
        
        if not user.data:
            return {"success": False, "error": f"User @{username} not found"}
            
        tweets = client.get_users_tweets(
            id=user.data.id,
            tweet_fields=["created_at", "public_metrics"],
            max_results=count
        )
        
        result = {
            "success": True,
            "user": {
                "id": user.data.id,
                "username": user.data.username,
                "name": user.data.name,
                "description": user.data.description
            },
            "tweets": [{
                "id": tweet.id,
                "text": tweet.text,
                "created_at": tweet.created_at,
                "url": f"https://twitter.com/{user.data.username}/status/{tweet.id}",
                "metrics": tweet.public_metrics
            } for tweet in tweets.data] if tweets.data else []
        }
        
        logger.info(f"Retrieved {len(result['tweets'])} tweets from @{username}")
        return result
        
    except Exception as e:
        logger.error(f"Error fetching user timeline: {str(e)}")
        return {"success": False, "error": str(e)}

def get_twitter_client():
    """Initialize and return an authenticated Twitter client"""
    config = settings.get_twitter_config()
    return tweepy.Client(
        consumer_key=config['api_key'],
        consumer_secret=config['api_secret'],
        access_token=config['access_token'],
        access_token_secret=config['access_token_secret'],
        wait_on_rate_limit=True
    )

class TwitterAgent(BaseAgent):
    """Agent for handling Twitter interactions."""
    
    def __init__(self):
        """Initialize Twitter agent with necessary tools and services."""
        super().__init__(
            name="Twitter Agent",
            description="Agent for creating and managing Twitter content",
            tools=[post_tweet, get_user_timeline],
            temperature=0.7
        )
        self.twitter_service = TwitterService()
    
    @log_execution_time
    def create_educational_tweet(self, topic: str) -> Dict[str, Any]:
        """
        Create an educational tweet about a topic.
        
        Args:
            topic: Topic to tweet about
            
        Returns:
            Dict containing tweet information
        """
        # Generate tweet content using the agent
        prompt = f"""
        Create an educational tweet about {topic}.
        The tweet should be:
        1. Informative and educational
        2. Under 280 characters
        3. Include relevant hashtags
        4. Be engaging and shareable
        """
        
        response = self.run(prompt)
        
        # Create the tweet
        return self.twitter_service.create_tweet(response.get('content', ''))
    
    @log_execution_time
    def analyze_topic(self, topic: str) -> Dict[str, Any]:
        """
        Analyze a topic on Twitter and provide insights.
        
        Args:
            topic: Topic to analyze
            
        Returns:
            Dict containing topic analysis
        """
        # Search for recent tweets about the topic
        recent_tweets = self.twitter_service.search_tweets(topic, max_results=10)
        
        # Generate analysis using the agent
        prompt = f"""
        Analyze the topic '{topic}' on Twitter with the following information:
        - Recent tweets: {recent_tweets}
        
        Provide insights about:
        1. Current discussion trends
        2. Key influencers and their approaches
        3. Best practices for engaging with this topic
        4. Potential angles for educational content
        """
        
        analysis = self.run(prompt)
        
        return {
            'recent_tweets': recent_tweets,
            'analysis': analysis
        }
    
    @log_execution_time
    def create_tweet_thread(self, topic: str, num_tweets: int = 5) -> List[Dict[str, Any]]:
        """
        Create a thread of educational tweets about a topic.
        
        Args:
            topic: Topic to create thread about
            num_tweets: Number of tweets in the thread
            
        Returns:
            List of tweet information dictionaries
        """
        # Generate thread content using the agent
        prompt = f"""
        Create an educational thread about {topic} with {num_tweets} tweets.
        Each tweet should:
        1. Be under 280 characters
        2. Be informative and educational
        3. Flow naturally from the previous tweet
        4. Include relevant hashtags
        5. End with a call to action in the final tweet
        """
        
        response = self.run(prompt)
        tweets = response.get('tweets', [])
        
        # Create the tweets
        created_tweets = []
        for tweet_content in tweets:
            tweet = self.twitter_service.create_tweet(tweet_content)
            created_tweets.append(tweet)
        
        return created_tweets

# Create an instance of TwitterAgent for use in other modules
twitter_agent = TwitterAgent()