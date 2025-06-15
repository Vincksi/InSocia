# Social Media Analysis and Content Generation Platform

A powerful platform that analyzes companies and generates social media content using AI agents. The platform coordinates multiple specialized agents to create and manage content across different social media platforms.

## Features

- **Company Analysis**: Deep analysis of company websites to extract key information
- **Social Media Strategy**: Automated creation of social media strategies
- **Content Generation**: AI-powered content creation for multiple platforms
- **Multi-Platform Support**: Currently supports Twitter and Reddit
- **Web Analysis**: Advanced website content extraction and analysis
- **Modern Web Interface**: Responsive and interactive web interface with real-time feedback

## Project Structure

```
.
├── src/
│   ├── agents/
│   │   ├── orchestrator_agent.py    # Main orchestrator agent
│   │   ├── twitter_agent.py         # Twitter content generation
│   │   ├── reddit_agent.py          # Reddit content generation
│   │   └── web_agent.py             # Website analysis
│   ├── config/
│   │   └── settings.py              # Configuration settings
│   ├── services/
│   │   ├── twitter_service.py       # Twitter API integration
│   │   ├── reddit_service.py        # Reddit API integration
│   │   └── web_service.py           # Web scraping and analysis
│   ├── templates/
│   │   ├── static/
│   │   │   ├── css/
│   │   │   │   └── style.css       # Custom styles
│   │   │   └── js/
│   │   │       └── main.js         # Frontend logic
│   │   └── index.html              # Web interface template
│   ├── utils/
│   │   └── decorators.py           # Utility decorators
│   └── app.py                      # Flask web application
├── tests/
│   ├── test_orchestrator_agent.py   # Orchestrator tests
│   ├── test_agents.py              # Individual agent tests
│   └── conftest.py                 # Test fixtures
├── .env.example                    # Example environment variables
├── requirements.txt                # Project dependencies
└── pytest.ini                      # Test configuration
```

## Frontend Features

The platform features a modern, responsive web interface with the following capabilities:

- **Real-time Validation**: Instant feedback on URL input
- **Interactive UI**: Smooth animations and transitions
- **Responsive Design**: Works seamlessly on all device sizes
- **Visual Feedback**: Clear loading states and error messages
- **Structured Results**: Well-organized and readable analysis output
- **Modern Styling**: Professional look with shadows and hover effects
- **Accessibility**: Proper ARIA labels and semantic HTML

### Frontend Technologies

- **HTML**: Semantic markup for better accessibility
- **CSS**: Modern styling with transitions and animations
- **JavaScript**: Interactive features and real-time updates
- **Bootstrap**: Responsive grid system and components
- **Font Awesome**: Professional icons and visual elements

## Prerequisites

- Python 3.8+
- Anthropic API key
- Twitter API credentials
- Reddit API credentials
- ... (Other Social Media API credentials)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and credentials
```

## Usage

### Web Interface

The platform provides a modern, user-friendly web interface for easy interaction:

1. Start the web server:
```bash
python src/app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Enter a company URL and click "Analyze" to:
   - Get real-time validation of the URL
   - See loading animations during analysis
   - View structured and formatted results
   - Receive clear error messages if needed

### Programmatic Usage

You can also use the platform programmatically:

```python
from src.agents.orchestrator_agent import OrchestratorAgent

# Initialize the orchestrator
orchestrator = OrchestratorAgent()

# Analyze a company and create social media content
url = "https://example.com"
result = orchestrator.run_app(url)

# Check the results
if result['status'] == 'success':
    print(result['result'])
```

## Testing

The project uses pytest for testing. To run the tests:

1. Install test dependencies:
```bash
pip install pytest pytest-cov
```

2. Run the tests:
```bash
pytest
```

For coverage report:
```bash
pytest --cov=src --cov-report=term-missing
```

## Configuration

The platform uses environment variables for configuration. Create a `.env` file with the following variables:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [smolagents](https://github.com/huggingface/smolagents) for the agent framework
- [Anthropic](https://www.anthropic.com/) for the AI model
- [Twitter API](https://developer.twitter.com/)
- [Reddit API](https://www.reddit.com/dev/api/)
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Bootstrap](https://getbootstrap.com/) for the frontend framework
- [Font Awesome](https://fontawesome.com/) for the icons 
