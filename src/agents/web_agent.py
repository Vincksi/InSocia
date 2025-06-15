# Standard library imports
import requests
from typing import Dict, Any, List

# Third-party imports
from anthropic import Anthropic
from bs4 import BeautifulSoup
from smolagents import tool, CodeAgent, LiteLLMModel

# Local imports
from src.config.settings import settings
from src.agents.base_agent import BaseAgent
from src.services.web_service import WebService
from src.utils.decorators import log_execution_time, rate_limit

# Initialize Anthropic client
client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

@tool
@rate_limit(calls=10, period=60)
def describe_company_from_url(url: str) -> str:
    """
    Summarize the company description from the given website URL using Claude.

    Args:
        url: The URL of the company website to summarize.
    """
    website_text = scrape_website(url)
    if website_text.startswith("Error"):
        return website_text
    return generate_description(website_text)

@tool
@rate_limit(calls=10, period=60)
def profiler(company_description: str) -> str:
    """
    Based on the company description, profile the people that could be interested in the product.

    Args:
        company_description: The description of the company to analyze.
    """
    prompt = (
        f"Here is a company description:\n\n{company_description}\n\n"
        "Based on this description, please provide a detailed ideal customer profile including:\n"
        "1. Demographics (age, role, industry)\n"
        "2. Pain points and challenges they face\n"
        "3. Goals and objectives they want to achieve\n"
        "4. Decision-making factors\n"
        "5. Technical sophistication level\n"
        "Please format this as a clear, professional customer profile."
    )
    
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=300,
        temperature=0.5,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def scrape_website(url: str) -> str:
    """Scrape text content from the given website URL."""
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        # Remove scripts and styles
        for tag in soup(["script", "style"]): tag.decompose()
        return ' '.join(soup.stripped_strings)[:8000]  # truncate for Claude
    except Exception as e:
        return f"Error scraping site: {e}"

def generate_description(text: str) -> str:
    """Use Anthropic Claude to generate a company description from text."""
    prompt = (
        f"Here is some website content:\n\n{text}\n\n"
        "Please summarize this as a professional company description."
    )
    
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=300,
        temperature=0.5,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

class WebAgent(BaseAgent):
    """Agent for handling web analysis and content extraction."""
    
    def __init__(self):
        """Initialize Web agent with necessary tools and services."""
        super().__init__(
            name="Web Agent",
            description="Agent for analyzing websites and extracting content",
            tools=[describe_company_from_url, profiler],
            temperature=0.5
        )
        self.web_service = WebService()
    
    @log_execution_time
    def analyze_website_content(self, url: str) -> Dict[str, Any]:
        """
        Analyze a website's content and provide insights.
        
        Args:
            url: Website URL to analyze
            
        Returns:
            Dict containing website analysis
        """
        # Get website information
        website_info = self.web_service.analyze_website(url)
        
        # Generate analysis using the agent
        prompt = f"""
        Analyze the website {url} with the following information:
        - Meta information: {website_info['meta_info']}
        - Content summary: {website_info['content_summary']}
        - Status code: {website_info['status_code']}
        
        Provide insights about:
        1. Content quality and relevance
        2. SEO optimization opportunities
        3. Potential improvements
        4. Key topics and themes
        """
        
        analysis = self.run(prompt)
        
        return {
            'website_info': website_info,
            'analysis': analysis
        }
    
    @log_execution_time
    def extract_and_summarize(self, url: str) -> Dict[str, Any]:
        """
        Extract content from a website and create a summary.
        
        Args:
            url: Website URL to analyze
            
        Returns:
            Dict containing extracted content and summary
        """
        # Extract text content
        content = self.web_service.extract_text_content(url)
        
        # Generate summary using the agent
        prompt = f"""
        Create a comprehensive summary of the following content from {url}:
        
        {content[:2000]}  # Limit content length for the prompt
        
        The summary should:
        1. Capture the main points
        2. Highlight key insights
        3. Be well-structured and easy to read
        4. Include relevant statistics or data if present
        """
        
        summary = self.run(prompt)
        
        return {
            'url': url,
            'content_length': len(content),
            'summary': summary
        }
    
    @log_execution_time
    def compare_websites(self, urls: List[str]) -> Dict[str, Any]:
        """
        Compare multiple websites and provide insights.
        
        Args:
            urls: List of website URLs to compare
            
        Returns:
            Dict containing comparison analysis
        """
        # Get information for each website
        websites_info = []
        for url in urls:
            info = self.web_service.analyze_website(url)
            websites_info.append(info)
        
        # Generate comparison using the agent
        prompt = f"""
        Compare the following websites:
        {[{'url': info['url'], 'meta_info': info['meta_info']} for info in websites_info]}
        
        Provide insights about:
        1. Content quality comparison
        2. Common themes and differences
        3. Best practices observed
        4. Areas for improvement
        5. Unique strengths of each website
        """
        
        comparison = self.run(prompt)
        
        return {
            'websites_info': websites_info,
            'comparison': comparison
        }

web_agent = CodeAgent(tools=[describe_company_from_url, profiler], 
                      model=LiteLLMModel(
                          model_id="anthropic/claude-3-5-sonnet-latest",
                          api_key=settings.ANTHROPIC_API_KEY,
                      ),
                      name="URLDescriptionAgent",
                      description="An agent that gives you the ideal customer profile from website URLs"
                      )
