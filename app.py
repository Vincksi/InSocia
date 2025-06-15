from flask import Flask, render_template, request, jsonify
from src.agents.orchestrator_agent import OrchestratorAgent
import logging
import os

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app with static folder configuration
app = Flask(__name__, 
    template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src/templates'),
    static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src/static'),
    static_url_path='/static'
)

orchestrator = OrchestratorAgent()

@app.route('/')
def index():
    """Page d'accueil."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyse une entreprise et génère du contenu."""
    try:
        url = request.form.get('url')
        if not url:
            return jsonify({
                'status': 'error',
                'message': 'URL is required'
            }), 400

        logger.info(f"Starting analysis for URL: {url}")
        result = orchestrator.run_app(url)

        if result['status'] == 'success':
            return jsonify({
                'status': 'success',
                'data': result['result']
            })
        else:
            return jsonify({
                'status': 'error',
                'message': result['error']
            }), 500

    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/status')
def status():
    """Vérifie le statut de l'application."""
    return jsonify({
        'status': 'ok',
        'message': 'Application is running'
    })

if __name__ == '__main__':
    app.run(debug=True) 