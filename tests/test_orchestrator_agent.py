import unittest
from unittest.mock import Mock, patch
from src.agents.orchestrator_agent import OrchestratorAgent

class TestOrchestratorAgent(unittest.TestCase):
    """Test suite for the OrchestratorAgent class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.orchestrator = OrchestratorAgent(
            model_id="test-model",
            temperature=0.3,
            planning_interval=5,
            verbosity_level=2,
            max_steps=20
        )
    
    def test_init(self):
        """Test the initialization of OrchestratorAgent."""
        self.assertIsNotNone(self.orchestrator.agent)
        self.assertIsNotNone(self.orchestrator.web_search)
    
    def test_validate_url_valid(self):
        """Test URL validation with valid URLs."""
        valid_urls = [
            "https://example.com",
            "http://test.com/path",
            "https://sub.domain.com/page?param=value"
        ]
        for url in valid_urls:
            self.assertTrue(self.orchestrator._validate_url(url))
    
    def test_validate_url_invalid(self):
        """Test URL validation with invalid URLs."""
        invalid_urls = [
            "not-a-url",
            "http://",
            "https://",
            "ftp://invalid",
            ""
        ]
        for url in invalid_urls:
            self.assertFalse(self.orchestrator._validate_url(url))
    
    @patch('src.orchestrator_agent.CodeAgent')
    def test_run_app_success(self, mock_code_agent):
        """Test successful execution of run_app."""
        # Mock the agent's run method
        mock_code_agent.return_value.run.return_value = "Test analysis result"
        
        url = "https://example.com"
        result = self.orchestrator.run_app(url)
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['url'], url)
        self.assertEqual(result['result'], "Test analysis result")
    
    @patch('src.orchestrator_agent.CodeAgent')
    def test_run_app_invalid_url(self, mock_code_agent):
        """Test run_app with invalid URL."""
        url = "invalid-url"
        result = self.orchestrator.run_app(url)
        
        self.assertEqual(result['status'], 'error')
        self.assertEqual(result['url'], url)
        self.assertIn('Format d\'URL invalide', result['error'])
    
    @patch('src.orchestrator_agent.CodeAgent')
    def test_run_app_agent_error(self, mock_code_agent):
        """Test run_app when agent raises an error."""
        # Mock the agent's run method to raise an exception
        mock_code_agent.return_value.run.side_effect = Exception("Test error")
        
        url = "https://example.com"
        result = self.orchestrator.run_app(url)
        
        self.assertEqual(result['status'], 'error')
        self.assertEqual(result['url'], url)
        self.assertEqual(result['error'], "Test error")

if __name__ == '__main__':
    unittest.main() 