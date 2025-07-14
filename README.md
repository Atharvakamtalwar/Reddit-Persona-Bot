# Reddit User Persona Generator 🤖

<div align="center">

![Reddit Logo](https://img.shields.io/badge/Reddit-FF4500?style=for-the-badge&logo=reddit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Generate detailed user personas from Reddit activity using AI analysis powered by Google Gemini.

</div>

## Overview

Analyze Reddit user activity to create comprehensive personality profiles using AI. Features smart data scraping, persona generation, activity analytics, and beautiful visualizations.

## Features

- 🔍 **Smart Data Scraping**: Reddit API (PRAW) with web scraping fallback
- 🤖 **AI-Powered Analysis**: Google Gemini for deep personality insights
- 📊 **Rich Visualizations**: Interactive charts, word clouds, activity patterns
- 💾 **Multiple Export Formats**: Text, PDF, CSV downloads
- 🌐 **Web Interface**: Beautiful Streamlit UI with progress tracking
- 🗄️ **GraphRAG Chat**: Interactive Q&A using knowledge graphs powered by Neo4j

## Quick Start

1. **Clone and install**

   ```bash
   git clone https://github.com/yourusername/reddit-persona-generator.git
   cd reddit-persona-generator
   pip install -r requirements.txt
   ```

2. **Configure APIs**
   Create a `.env` file with your API credentials:

   ```env
   # Reddit API (optional but recommended)
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_CLIENT_SECRET=your_client_secret
   REDDIT_USER_AGENT=PersonaBot/1.0 by YourUsername

   # Google Gemini API (required for AI analysis)
   GEMINI_API_KEY=your_gemini_api_key

   # Neo4j Database (for GraphRAG chat)
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=password
   ```

3. **Setup Neo4j Database** (for GraphRAG chat feature)

   ```bash
   # Option 1: Auto-setup with Docker
   python setup_neo4j.py

   # Option 2: Manual Docker setup
   docker run --name neo4j-persona -p 7474:7474 -p 7687:7687 \
     -e NEO4J_AUTH=neo4j/password -d neo4j:latest
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## API Setup

### Reddit API (Optional)

1. Go to [Reddit Apps](https://www.reddit.com/prefs/apps)
2. Create a new "script" app
3. Get your client ID and secret
4. Add to `.env`: `REDDIT_CLIENT_ID=your_id` and `REDDIT_CLIENT_SECRET=your_secret`

### Google Gemini API (Required)

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create an API key
3. Add to `.env`: `GEMINI_API_KEY=your_key`

### Neo4j Database (For GraphRAG Chat)

1. **Auto-setup**: Run `python setup_neo4j.py`
2. **Manual setup**: Install Neo4j Desktop or use Docker
3. **Docker**: `docker run --name neo4j-persona -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password -d neo4j:latest`
4. Add to `.env`: `NEO4J_URI=bolt://localhost:7687`, `NEO4J_USER=neo4j`, `NEO4J_PASSWORD=password`

## Usage

1. **Start the app**: `streamlit run app.py`
2. **Enter a Reddit username** (e.g., `kojied`)
3. **Generate persona** and explore analytics
4. **Use GraphRAG chat** for interactive Q&A about the persona
5. **Download results** in multiple formats

## Project Structure

```
reddit-persona-generator/
├── src/
│   ├── reddit_scraper.py      # Reddit data scraping
│   ├── persona_generator.py   # AI persona generation
│   └── graphrag_handler.py    # GraphRAG knowledge graph
├── output/                    # Generated personas and data
├── temp_graph/               # Temporary graph data files
├── app.py                    # Streamlit web application
├── setup_neo4j.py           # Neo4j database setup
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── .gitignore               # Git ignore rules
├── LICENSE                  # MIT License
└── README.md                # This file
```

## Sample Output

```markdown
# Reddit User Persona: u/kojied

## 👤 User Profile

**Age Range:** Early to mid-30s
**Location:** New York City, USA
**Primary Interests:** Tech & Spatial Computing, Strategic Gaming, NYC Culture

## 🎯 Core Identity

Analytical, curious tech professional with interests in emerging technologies...
```

## Privacy & Ethics

- 🔐 **Public Data Only**: Analyzes publicly available Reddit content
- 🤖 **No Personal Info**: No private messages or personal data collection
- 📝 **Educational Use**: Intended for research and educational purposes
- ⚖️ **Terms of Service**: Users must comply with Reddit's ToS

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- Check [Issues](https://github.com/yourusername/reddit-persona-generator/issues) for common problems
- Create a new issue if you need help

---

<div align="center">
Made with ❤️ for the Reddit community
</div>
