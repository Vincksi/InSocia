import logging
from src.agents.orchestrator_agent import OrchestratorAgent

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Fonction principale pour exécuter l'agent orchestrateur."""
    try:
        # Initialisation de l'orchestrateur
        orchestrator = OrchestratorAgent()
        
        # URL de l'entreprise à analyser
        url = "https://example.com/"
        logger.info(f"Démarrage de l'analyse de l'entreprise: {url}")
        
        # Exécution de l'analyse
        analysis_result = orchestrator.run_app(url)
        
        # Affichage des résultats
        if analysis_result['status'] == 'success':
            logger.info("Analyse terminée avec succès")
            print("\nAnalyse terminée!")
            print("-" * 50)
            print(analysis_result['result'])
        else:
            logger.error(f"Échec de l'analyse: {analysis_result['error']}")
        
    except Exception as e:
        logger.error(f"Une erreur est survenue: {str(e)}")
        raise

if __name__ == "__main__":
    main() 