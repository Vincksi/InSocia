# InSocia - AI-Powered Social Media Assistant for Growth Strategy

InSocia is an intelligent social media assistant that helps you analyze, manage, and optimize your social media presence across multiple platforms. Using advanced AI technology, InSocia provides insights, automates content posting, and helps you make data-driven decisions for your social media strategy.

## Features

### Social Media API Integration
- Multi-platform support for various social media networks
- Analytics Reports with detailed insights
- Automated content posting
- Unified interface for managing all your social media accounts

### AI-Powered Insights
- Intelligent content recommendations
- Trend analysis and prediction
- Audience engagement optimization
- Performance analytics and reporting

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/insocia.git
cd insocia
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```env
# Social Media API Keys
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret

# Other API keys as needed
```

### Running the Application

1. Start the Flask development server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage

1. Enter a social media URL in the analysis form
2. Click "Analyze" to get AI-powered insights
3. View the detailed analysis report
4. Use the insights to optimize your social media strategy

## Project Structure

```
insocia/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── src/
│   ├── agents/           # AI agents for different tasks
│   ├── config/           # Configuration files
│   ├── services/         # External service integrations
│   ├── static/           # Static assets
│   ├── templates/        # HTML templates
│   └── utils/            # Utility functions
└── tests/                # Test files
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [smolagents](https://github.com/huggingface/smolagents) for the agent frameworkAdd commentMore actions
- [Anthropic](https://www.anthropic.com/) for the AI model
- [Twitter API](https://developer.twitter.com/)
- [Reddit API](https://www.reddit.com/dev/api/)
- [Flask](https://flask.palletsprojects.com/) for the web framework
