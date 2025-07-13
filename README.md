# Reddit User Persona Generator 🤖

<div align="center">

![Reddit Logo](https://img.shields.io/badge/Reddit-FF4500?style=for-the-badge&logo=reddit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Generate detailed user personas from Reddit activity using AI analysis powered by Google Gemini.

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [API Setup](#api-setup) • [Examples](#examples)

</div>

## Overview

The Reddit User Persona Generator is a powerful tool that analyzes Reddit user activity to create comprehensive personality profiles. It uses advanced AI analysis through Google Gemini to understand user behavior, interests, communication patterns, and more.

### Key Capabilities

- 🔍 **Smart Data Scraping**: Uses Reddit API (PRAW) with web scraping fallback
- 🤖 **AI-Powered Analysis**: Leverages Google Gemini for deep personality insights
- 📊 **Rich Visualizations**: Interactive charts, word clouds, and activity patterns
- 💾 **Data Export**: Save personas and raw data for further analysis
- 🌐 **Web Interface**: Beautiful Streamlit UI for easy interaction

## Features

### 🎭 Persona Generation

- **Comprehensive Analysis**: Interests, personality traits, communication style, demographics
- **Evidence-Based**: Every characteristic backed by specific posts/comments with citations
- **Confidence Ratings**: AI provides confidence levels for each inference
- **Structured Output**: Well-organized persona reports in multiple formats

### 📊 Activity Analytics

- **Subreddit Analysis**: Top communities and karma distribution
- **Temporal Patterns**: Activity by hour and day of the week
- **Content Analysis**: Most upvoted/downvoted posts and comments
- **Word Clouds**: Visual representation of frequently used terms

### 🔧 Technical Features

- **Dual Scraping Methods**: Reddit API (PRAW) + web scraping fallback
- **Rate Limiting**: Respectful API usage with built-in delays
- **Error Handling**: Robust error handling for various edge cases
- **Data Persistence**: JSON export of raw data for reproducibility

## Installation

### Prerequisites

- Python 3.10 or higher
- Reddit API credentials (optional but recommended)
- Google Gemini API key (for AI analysis)

### Quick Start

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/reddit-persona-generator.git
   cd reddit-persona-generator
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv

   # Windows
   venv\\Scripts\\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**

   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env with your API credentials
   ```

5. **Run the application**

   ```bash
   streamlit run app.py
   ```

6. **Open your browser** to `http://localhost:8501`

## API Setup

### Reddit API (Recommended)

1. Go to [Reddit Apps](https://www.reddit.com/prefs/apps)
2. Click "Create App" or "Create Another App"
3. Choose "script" as the app type
4. Fill in the required fields:
   - **name**: YourAppName
   - **description**: Reddit User Persona Generator
   - **redirect uri**: http://localhost:8080
5. Note your **client ID** (under the app name) and **secret**
6. Add to `.env`:
   ```
   REDDIT_CLIENT_ID=your_client_id_here
   REDDIT_CLIENT_SECRET=your_client_secret_here
   REDDIT_USER_AGENT=PersonaBot/1.0 by YourUsername
   ```

### Google Gemini API (Required for AI Analysis)

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key
5. Add to `.env`:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

### Environment Configuration

Create a `.env` file in the project root:

```env
# Reddit API Configuration
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
REDDIT_USER_AGENT=PersonaBot/1.0 by YourUsername

# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here
```

## Usage

### Web Interface (Recommended)

1. **Start the application**

   ```bash
   streamlit run app.py
   ```

2. **Enter a Reddit user**

   - Username: `kojied`
   - Profile URL: `https://www.reddit.com/user/kojied/`

3. **Configure settings** (sidebar)

   - Data limit: Number of posts/comments to analyze
   - Show raw data: Display scraped data

4. **Analyze and explore**
   - View generated persona
   - Explore activity analytics
   - Download results

### Command Line Usage

You can also use the core modules directly:

```python
from src.reddit_scraper import RedditScraper
from src.persona_generator import PersonaGenerator

# Initialize
scraper = RedditScraper()
generator = PersonaGenerator()

# Scrape data
data = scraper.get_user_data('username', limit=100)

# Generate persona
persona = generator.generate_persona(data)

# Save results
generator.save_persona(persona, 'username')
```

## Project Structure

```
reddit-persona-generator/
├── src/
│   ├── reddit_scraper.py      # Reddit data scraping
│   └── persona_generator.py   # AI persona generation
├── output/                    # Generated personas and data
├── app.py                     # Streamlit web application
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── .gitignore                # Git ignore rules
├── LICENSE                   # MIT License
└── README.md                 # This file
```

## Examples

### Sample Output

Here's what a generated persona looks like:

```markdown
# User Persona for u/kojied

## Overview

Active Reddit user with strong interests in technology, programming, and gaming.
Demonstrates analytical thinking and helpful communication style.

## Detailed Characteristics

### Interests & Hobbies

- **Programming & Technology**: Frequently discusses Python, web development, and
  software engineering topics (Confidence: High)
  - Evidence: "I've been working with FastAPI for the past year..."
  - Source: https://www.reddit.com/r/Python/comments/...

### Personality Traits

- **Helpful & Collaborative**: Often provides detailed assistance to other users
  (Confidence: High)
  - Evidence: "Here's a step-by-step solution to your problem..."
  - Source: https://www.reddit.com/r/learnpython/comments/...
```

### Use Cases

- **Content Strategy**: Understand your audience for better content creation
- **Market Research**: Analyze user behavior in specific communities
- **Academic Research**: Study online behavior patterns (with ethical considerations)
- **Personal Insights**: Understand your own Reddit activity patterns

## Configuration Options

### Data Limits

- **Minimum**: 50 posts/comments (faster analysis)
- **Default**: 100 posts/comments (balanced)
- **Maximum**: 500 posts/comments (comprehensive analysis)

### Analysis Depth

The tool automatically adjusts analysis depth based on available data:

- **Basic**: Activity statistics and top subreddits
- **Standard**: Includes temporal patterns and content analysis
- **Comprehensive**: Full AI persona with evidence citations

## Troubleshooting

### Common Issues

**"Could not retrieve data for this user"**

- User might not exist or have no public posts/comments
- Profile might be private or suspended
- Check username spelling

**"Reddit API Not Connected"**

- Verify your Reddit API credentials in `.env`
- Ensure your Reddit app is configured correctly
- Check that you're using the correct client ID and secret

**"Gemini API Not Connected"**

- Verify your Gemini API key in `.env`
- Check that you have API quota remaining
- Ensure your Google account has access to Gemini API

**"Access forbidden: Reddit is blocking the request"**

- This can happen with web scraping fallback
- Try using Reddit API credentials instead
- Consider changing your IP or using a VPN

### Rate Limiting

The tool implements respectful rate limiting:

- **Reddit API**: Follows PRAW's built-in rate limiting
- **Web Scraping**: 1-second delays between requests
- **Gemini API**: Respects API quota limits

## Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Add tests** if applicable
5. **Commit your changes** (`git commit -m 'Add amazing feature'`)
6. **Push to the branch** (`git push origin feature/amazing-feature`)
7. **Open a Pull Request**

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/reddit-persona-generator.git

# Create development environment
python -m venv dev-env
source dev-env/bin/activate  # or dev-env\\Scripts\\activate on Windows

# Install development dependencies
pip install -r requirements.txt
pip install black flake8 pytest

# Run tests
pytest

# Format code
black src/ app.py
```

## Privacy & Ethics

### Important Considerations

- 🔐 **Public Data Only**: Only analyzes publicly available Reddit posts and comments
- 🤖 **No Personal Info**: Does not collect private messages, email, or personal data
- 📝 **Educational Use**: Intended for educational and research purposes
- ⚖️ **Terms of Service**: Users must comply with Reddit's Terms of Service
- 🛡️ **Data Protection**: Raw data is stored locally and not transmitted to third parties

### Best Practices

- Always get consent before analyzing someone else's profile extensively
- Use insights responsibly and ethically
- Respect user privacy and Reddit's community guidelines
- Don't use for harassment, stalking, or malicious purposes

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **PRAW**: Python Reddit API Wrapper for Reddit integration
- **Google Gemini**: AI-powered text analysis and persona generation
- **Streamlit**: Beautiful web interface framework
- **Reddit Community**: For providing the data that makes this analysis possible

## Support

If you encounter issues or have questions:

1. Check the [troubleshooting section](#troubleshooting)
2. Search [existing issues](https://github.com/yourusername/reddit-persona-generator/issues)
3. [Create a new issue](https://github.com/yourusername/reddit-persona-generator/issues/new) if needed

---

<div align="center">
Made with ❤️ for the Reddit community
</div>
