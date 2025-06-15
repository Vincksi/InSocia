import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any, List
from src.utils.decorators import rate_limit, log_execution_time

class WebService:
    """Service for web scraping and analysis."""
    
    def __init__(self):
        """Initialize Web service."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    @rate_limit(calls=10, period=60)  # Conservative rate limit
    @log_execution_time
    def analyze_website(self, url: str) -> Dict[str, Any]:
        """
        Analyze a website and extract relevant information.
        
        Args:
            url: Website URL
            
        Returns:
            Dict containing website analysis
        """
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract meta information
            meta_info = {
                'title': soup.title.string if soup.title else None,
                'description': soup.find('meta', {'name': 'description'})['content'] if soup.find('meta', {'name': 'description'}) else None,
                'keywords': soup.find('meta', {'name': 'keywords'})['content'] if soup.find('meta', {'name': 'keywords'}) else None
            }
            
            # Extract main content
            main_content = soup.find('main') or soup.find('article') or soup.find('div', {'class': 'content'})
            content_text = main_content.get_text() if main_content else soup.get_text()
            
            # Extract links
            links = [a['href'] for a in soup.find_all('a', href=True)]
            
            return {
                'url': url,
                'meta_info': meta_info,
                'content_summary': content_text[:500] + '...' if len(content_text) > 500 else content_text,
                'links': links[:10],  # Limit to first 10 links
                'status_code': response.status_code
            }
        except Exception as e:
            raise Exception(f"Failed to analyze website: {str(e)}")
    
    @rate_limit(calls=10, period=60)
    @log_execution_time
    def extract_text_content(self, url: str) -> str:
        """
        Extract main text content from a webpage.
        
        Args:
            url: Website URL
            
        Returns:
            Extracted text content
        """
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # Break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # Drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return text
        except Exception as e:
            raise Exception(f"Failed to extract text content: {str(e)}")
    
    @rate_limit(calls=10, period=60)
    @log_execution_time
    def check_website_status(self, url: str) -> Dict[str, Any]:
        """
        Check the status and basic information of a website.
        
        Args:
            url: Website URL
            
        Returns:
            Dict containing website status information
        """
        try:
            response = self.session.head(url, allow_redirects=True)
            return {
                'url': url,
                'status_code': response.status_code,
                'content_type': response.headers.get('content-type'),
                'server': response.headers.get('server'),
                'final_url': response.url
            }
        except Exception as e:
            raise Exception(f"Failed to check website status: {str(e)}") 