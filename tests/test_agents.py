import unittest
from unittest.mock import Mock, patch
from src.agents.twitter_agent import twitter_agent
from src.agents.reddit_agent import reddit_agent
from src.agents.web_agent import web_agent

class TestTwitterAgent(unittest.TestCase):
    """Test suite for the Twitter agent."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent = twitter_agent
    
    @patch('src.agents.twitter_agent.CodeAgent')
    def test_create_educational_tweet(self, mock_code_agent):
        """Test creating an educational tweet."""
        mock_code_agent.return_value.run.return_value = "Test tweet content"
        
        topic = "AI in Education"
        result = self.agent.create_educational_tweet(topic)
        
        self.assertIsNotNone(result)
        self.assertEqual(result, "Test tweet content")
    
    @patch('src.agents.twitter_agent.CodeAgent')
    def test_search_tweets(self, mock_code_agent):
        """Test searching tweets."""
        mock_code_agent.return_value.run.return_value = ["Tweet 1", "Tweet 2"]
        
        query = "AI education"
        result = self.agent.search_tweets(query)
        
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)

class TestRedditAgent(unittest.TestCase):
    """Test suite for the Reddit agent."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent = reddit_agent
    
    @patch('src.agents.reddit_agent.CodeAgent')
    def test_create_educational_post(self, mock_code_agent):
        """Test creating an educational post."""
        mock_code_agent.return_value.run.return_value = "Test post content"
        
        subreddit = "edtech"
        topic = "AI in Education"
        result = self.agent.create_educational_post(subreddit, topic)
        
        self.assertIsNotNone(result)
        self.assertEqual(result, "Test post content")
    
    @patch('src.agents.reddit_agent.CodeAgent')
    def test_analyze_subreddit(self, mock_code_agent):
        """Test analyzing a subreddit."""
        mock_code_agent.return_value.run.return_value = {
            "name": "edtech",
            "subscribers": 1000,
            "description": "Test description"
        }
        
        subreddit = "edtech"
        result = self.agent.analyze_subreddit(subreddit)
        
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

class TestWebAgent(unittest.TestCase):
    """Test suite for the Web agent."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent = web_agent
    
    @patch('src.agents.web_agent.CodeAgent')
    def test_analyze_website(self, mock_code_agent):
        """Test analyzing a website."""
        mock_code_agent.return_value.run.return_value = {
            "title": "Test Website",
            "content": "Test content",
            "keywords": ["test", "website"]
        }
        
        url = "https://example.com"
        result = self.agent.analyze_website(url)
        
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
    
    @patch('src.agents.web_agent.CodeAgent')
    def test_extract_content(self, mock_code_agent):
        """Test extracting content from a website."""
        mock_code_agent.return_value.run.return_value = "Test content"
        
        url = "https://example.com"
        result = self.agent.extract_content(url)
        
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)

if __name__ == '__main__':
    unittest.main() 