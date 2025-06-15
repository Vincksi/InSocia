import logging
from typing import Dict, Any
from urllib.parse import urlparse

from smolagents import CodeAgent, LiteLLMModel, DuckDuckGoSearchTool
from twitter_agent import twitter_agent 
from src.agents.reddit_agent import reddit_agent
from src.agents.web_agent import web_agent
from src.config.settings import settings

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class OrchestratorAgent:
    """Agent orchestrateur principal qui coordonne tous les autres agents."""
    
    def __init__(
        self,
        model_id: str = "anthropic/claude-3-5-sonnet-latest",
        temperature: float = 0.3,
        planning_interval: int = 5,
        verbosity_level: int = 2,
        max_steps: int = 20
    ):
        """Initialise l'agent orchestrateur."""
        self.web_search = DuckDuckGoSearchTool()
        
        self.agent = CodeAgent(
            model=LiteLLMModel(
                model_id=model_id,
                api_key=settings.ANTHROPIC_API_KEY,
                temperature=temperature
            ),
            tools=[self.web_search],
            managed_agents=[web_agent, twitter_agent, reddit_agent],
            planning_interval=planning_interval,
            verbosity_level=verbosity_level,
            final_answer_checks=[],
            max_steps=max_steps
        )
    
    def _validate_url(self, url: str) -> bool:
        """Valide le format d'une URL."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    def run_app(self, url: str) -> Dict[str, Any]:
        """
        Analyse une entreprise et crée une stratégie de médias sociaux.
        
        Args:
            url: URL du site web de l'entreprise
            
        Returns:
            Dict contenant les résultats de l'analyse
        """
        try:
            logger.info(f"Début de l'analyse de l'entreprise: {url}")
            
            if not self._validate_url(url):
                raise ValueError(f"Format d'URL invalide: {url}")
            
            result = self.agent.run(
                f"""Analyze the company at {url} and create a comprehensive social media strategy.
                
                Follow these steps:
                1. Website Analysis:
                   - Analyze the website content and structure
                   - Extract key topics, themes, and value propositions
                   - Identify target audience and key messages
                
                2. Social Media Strategy:
                   For each platform (Twitter and Reddit):
                   - Research relevant communities and hashtags
                   - Analyze engagement patterns and best posting times
                   - Identify key influencers and thought leaders
                   - Review community guidelines and rules
                
                3. Content Creation and Distribution:
                   Twitter:
                   - Create 3-5 educational tweets about the company's key features
                   - Include relevant hashtags and mentions
                   - Ensure content is informative and adds value
                   
                   Reddit:
                   - Identify 2-3 relevant subreddits for posting
                   - Create an educational post for each subreddit
                   - Include detailed analysis and insights
                   - Engage with community comments
                
                4. Engagement Plan:
                   - Monitor and respond to comments
                   - Participate in relevant discussions
                   - Share additional insights and resources
                
                Use the following tools and agents:
                - Web Agent: For website analysis and content extraction
                - Twitter Agent: For creating and managing Twitter content
                - Reddit Agent: For creating and managing Reddit content
                - Web Search: For additional research and verification
                
                Important Guidelines:
                - Ensure all content is educational and adds value
                - Follow each platform's community guidelines
                - Maintain a professional and helpful tone
                - Include relevant data and examples
                - Engage authentically with the community
                """
            )
            
            logger.info("Analyse terminée avec succès")
            return {
                'status': 'success',
                'url': url,
                'result': result
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse: {str(e)}")
            return {
                'status': 'error',
                'url': url,
                'error': str(e)
            }