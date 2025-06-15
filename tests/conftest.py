import pytest
from unittest.mock import Mock, patch
from src.agents.orchestrator_agent import OrchestratorAgent
#from src.agents.twitter_agent import twitter_agent
#from src.agents.reddit_agent import reddit_agent
#from src.agents.web_agent import web_agent

@pytest.fixture
def mock_code_agent():
    """Fixture for mocking CodeAgent."""
    with patch('smolagents.CodeAgent') as mock:
        yield mock

@pytest.fixture
def orchestrator_agent():
    """Fixture for creating an OrchestratorAgent instance."""
    return OrchestratorAgent(
        model_id="test-model",
        temperature=0.3,
        planning_interval=5,
        verbosity_level=2,
        max_steps=20
    )

@pytest.fixture
def mock_twitter_agent():
    """Fixture for mocking Twitter agent."""
    with patch('src.agents.twitter_agent.twitter_agent') as mock:
        mock.create_educational_tweet.return_value = "Test tweet"
        mock.search_tweets.return_value = ["Tweet 1", "Tweet 2"]
        yield mock

@pytest.fixture
def mock_reddit_agent():
    """Fixture for mocking Reddit agent."""
    with patch('src.agents.reddit_agent.reddit_agent') as mock:
        mock.create_educational_post.return_value = "Test post"
        mock.analyze_subreddit.return_value = {
            "name": "edtech",
            "subscribers": 1000,
            "description": "Test description"
        }
        yield mock

@pytest.fixture
def mock_web_agent():
    """Fixture for mocking Web agent."""
    with patch('src.agents.web_agent.web_agent') as mock:
        mock.analyze_website.return_value = {
            "title": "Test Website",
            "content": "Test content",
            "keywords": ["test", "website"]
        }
        mock.extract_content.return_value = "Test content"
        yield mock 