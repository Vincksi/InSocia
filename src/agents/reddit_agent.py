# Standard library imports
import praw
import json
import re
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from functools import wraps
import logging
import os
from dotenv import load_dotenv

# Third-party imports
import backoff
from smolagents import DuckDuckGoSearchTool, tool

# Local imports
from src.config.settings import settings
from src.agents.base_agent import BaseAgent
from src.services.reddit_service import RedditService
from src.utils.decorators import log_execution_time, rate_limit

# Configuration
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@tool
@backoff.on_exception(backoff.expo, praw.exceptions.RedditAPIException, max_tries=3)
@rate_limit(calls=30, period=60)
def publish_post(title: str, content: str, subreddit: str, 
                post_type: Optional[str] = None, url: Optional[str] = None) -> str:
    """
    Publie un post sur Reddit dans un subreddit spécifique.

    Args:
        title: Titre du post Reddit
        content: Contenu du post
        subreddit: Nom du subreddit (sans r/)
        post_type: Type de post ('text' ou 'link')
        url: URL si c'est un post de type link
    """
    try:
        # Validation des entrées
        if not title or len(title) > 300:
            raise ValueError("Le titre doit faire entre 1 et 300 caractères")
        if not content or len(content) > 40000:
            raise ValueError("Le contenu doit faire entre 1 et 40000 caractères")
        if not subreddit:
            raise ValueError("Le nom du subreddit est requis")
        if post_type and post_type not in ["text", "link"]:
            raise ValueError("Type de post invalide (text ou link)")
        if post_type == "link" and not url:
            raise ValueError("URL requise pour un post de type link")

        # Initialisation de l'API Reddit
        reddit = get_reddit_client()
        sub = reddit.subreddit(subreddit)
        
        if post_type is None:
            post_type = "text"
        
        if post_type == "text":
            submission = sub.submit(title=title, selftext=content)
        else:  # post_type == "link"
            submission = sub.submit(title=title, url=url)
        
        logger.info(f"Post publié avec succès dans r/{subreddit}")
        return f"Post publié avec succès! URL: https://reddit.com{submission.permalink}"
        
    except Exception as e:
        logger.error(f"Erreur lors de la publication: {str(e)}")
        raise

@tool
@backoff.on_exception(backoff.expo, praw.exceptions.RedditAPIException, max_tries=3)
@rate_limit(calls=30, period=60)
def analyze_subreddit(subreddit: str) -> str:
    """
    Analyse les règles et tendances d'un subreddit.

    Args:
        subreddit: Nom du subreddit à analyser
    """
    try:
        if not subreddit:
            raise ValueError("Le nom du subreddit est requis")

        reddit = get_reddit_client()
        sub = reddit.subreddit(subreddit)
        
        # Récupérer les règles
        rules = []
        try:
            for rule in sub.rules:
                rules.append(f"- {rule.short_name}: {rule.description}")
        except Exception as e:
            logger.warning(f"Impossible de récupérer les règles: {str(e)}")
            rules = ["Règles non accessibles"]
        
        # Analyser les posts populaires récents
        hot_posts = []
        try:
            for post in sub.hot(limit=10):
                hot_posts.append({
                    "title": post.title,
                    "score": post.score,
                    "num_comments": post.num_comments,
                    "is_self": post.is_self
                })
        except Exception as e:
            logger.warning(f"Impossible de récupérer les posts chauds: {str(e)}")
        
        analysis = f"""
        Analyse du subreddit r/{subreddit}:
        
        Règles principales:
        {chr(10).join(rules)}
        
        Tendances des posts populaires:
        - Score moyen: {sum(p['score'] for p in hot_posts) / len(hot_posts) if hot_posts else 0:.0f}
        - Commentaires moyens: {sum(p['num_comments'] for p in hot_posts) / len(hot_posts) if hot_posts else 0:.0f}
        - Posts texte: {sum(1 for p in hot_posts if p['is_self'])} / {len(hot_posts)}
        
        Exemples de titres populaires:
        {chr(10).join([f"- {p['title'][:80]}..." for p in hot_posts[:3]]) if hot_posts else "Aucun post disponible"}
        """
        
        logger.info(f"Analyse terminée pour r/{subreddit}")
        return analysis
        
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse: {str(e)}")
        raise

@tool
@backoff.on_exception(backoff.expo, praw.exceptions.RedditAPIException, max_tries=3)
@rate_limit(calls=30, period=60)
def comment_on_post(post_url: str, comment_text: str, 
                   parent_comment_id: Optional[str] = None) -> str:
    """
    Ajoute un commentaire à un post Reddit existant.

    Args:
        post_url: URL complète du post Reddit à commenter
        comment_text: Texte du commentaire à publier
        parent_comment_id: ID du commentaire parent si c'est une réponse
    """
    try:
        # Extraire l'ID du post depuis l'URL
        submission_id = _extract_submission_id(post_url)
        if not submission_id:
            raise ValueError("Impossible d'extraire l'ID du post depuis l'URL")
        
        reddit = get_reddit_client()
        
        # Récupérer le post
        submission = reddit.submission(id=submission_id)
        
        # Si c'est une réponse à un commentaire
        if parent_comment_id:
            parent_comment = reddit.comment(id=parent_comment_id)
            comment = parent_comment.reply(comment_text)
        else:
            comment = submission.reply(comment_text)
        
        logger.info(f"Commentaire publié avec succès sur {post_url}")
        return f"Commentaire publié avec succès! URL: https://reddit.com{comment.permalink}"
        
    except Exception as e:
        logger.error(f"Erreur lors de la publication du commentaire: {str(e)}")
        raise

def _extract_submission_id(url: str) -> Optional[str]:
    """Extrait l'ID du post depuis une URL Reddit"""
    patterns = [
        r'reddit\.com/r/\w+/comments/([a-zA-Z0-9]+)',
        r'redd\.it/([a-zA-Z0-9]+)',
        r'/comments/([a-zA-Z0-9]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def get_reddit_client():
    """Initialize and return an authenticated Reddit client"""
    config = settings.get_reddit_config()
    return praw.Reddit(
        client_id=config['client_id'],
        client_secret=config['client_secret'],
        user_agent=config['user_agent'],
        username=config['username'],
        password=config['password']
    )

class RedditAgent(BaseAgent):
    """Agent for handling Reddit interactions."""
    
    def __init__(self):
        """Initialize Reddit agent with necessary tools and services."""
        super().__init__(
            name="Reddit Agent",
            description="Agent for creating and managing Reddit content",
            tools=[publish_post, analyze_subreddit, comment_on_post, DuckDuckGoSearchTool()],
            temperature=0.7
        )
        self.reddit_service = RedditService()
    
    @log_execution_time
    def create_educational_post(self, subreddit: str, topic: str) -> Dict[str, Any]:
        """
        Create an educational post in a subreddit.
        
        Args:
            subreddit: Target subreddit
            topic: Topic to create post about
            
        Returns:
            Dict containing post information
        """
        # First, get subreddit info to ensure it exists and check rules
        subreddit_info = self.reddit_service.get_subreddit_info(subreddit)
        
        # Generate post content using the agent
        prompt = f"""
        Create an educational post about {topic} for the subreddit r/{subreddit}.
        The subreddit has {subreddit_info['subscribers']} subscribers.
        The post should be informative and follow these rules: {subreddit_info['rules']}
        """
        
        response = self.run(prompt)
        
        # Create the post
        return self.reddit_service.create_post(
            subreddit=subreddit,
            title=response.get('title', f'Educational Post: {topic}'),
            content=response.get('content', '')
        )
    
    @log_execution_time
    def analyze_subreddit(self, subreddit: str) -> Dict[str, Any]:
        """
        Analyze a subreddit and provide insights.
        
        Args:
            subreddit: Target subreddit
            
        Returns:
            Dict containing subreddit analysis
        """
        # Get subreddit information
        subreddit_info = self.reddit_service.get_subreddit_info(subreddit)
        
        # Get recent posts
        recent_posts = self.reddit_service.search_posts(subreddit, 'self:yes', limit=5)
        
        # Generate analysis using the agent
        prompt = f"""
        Analyze the subreddit r/{subreddit} with the following information:
        - Description: {subreddit_info['description']}
        - Subscriber count: {subreddit_info['subscribers']}
        - Rules: {subreddit_info['rules']}
        - Recent posts: {recent_posts}
        
        Provide insights about:
        1. The subreddit's focus and community
        2. Content preferences and style
        3. Best practices for posting
        4. Potential topics that would be well-received
        """
        
        analysis = self.run(prompt)
        
        return {
            'subreddit_info': subreddit_info,
            'recent_posts': recent_posts,
            'analysis': analysis
        }

# Create an instance of RedditAgent for use in other modules
reddit_agent = RedditAgent()