# Reddit User Persona Generator 🤖

<div align="center">

![Reddit Logo](https://img.shields.io/badge/Reddit-FF4500?style=for-the-badge&logo=reddit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Neo4j](https://img.shields.io/badge/Neo4j-008CC1?style=for-the-badge&logo=neo4j&logoColor=white)

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Generate detailed user personas from Reddit activity using AI analysis powered by Google Gemini and interactive Q&A with Neo4j knowledge graphs.**

</div>

## ✨ Features

- 🔍 **Smart Data Scraping**: Reddit API (PRAW) with web scraping fallback
- 🤖 **AI-Powered Analysis**: Google Gemini for deep personality insights
- 📊 **Rich Visualizations**: Interactive charts, word clouds, activity patterns
- 💾 **Multiple Export Formats**: Text, PDF, CSV downloads
- 🌐 **Beautiful Web Interface**: Streamlit UI with real-time progress tracking
- 🗄️ **GraphRAG Chat**: Interactive Q&A using knowledge graphs powered by Neo4j
- 🎯 **Multi-User Support**: Handle multiple users with separate knowledge graphs
- 🔄 **Real-time Updates**: Live progress tracking and instant results

## 🚀 Quick Start

### 1. Installation

```bash
git clone https://github.com/Atharvakamtalwar/Reddit-Persona-Bot.git
cd Reddit-Persona-Bot
pip install -r requirements.txt
```

### 2. Environment Setup

Create a `.env` file with your API credentials:

```env
# Reddit API (optional but recommended for better data quality)
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=PersonaBot/1.0 by YourUsername

# Google Gemini API (required for AI analysis)
GEMINI_API_KEY=your_gemini_api_key

# Neo4j Cloud Database (for GraphRAG chat feature)
NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
```

### 3. Launch Application

```bash
streamlit run app.py
```

Open your browser and navigate to `http://localhost:8501`

## 🔧 API Configuration

### Reddit API (Optional)

_Improves data quality and reduces rate limits_

1. Visit [Reddit Apps](https://www.reddit.com/prefs/apps)
2. Click "Create App" → Select "script"
3. Copy your **Client ID** and **Client Secret**
4. Add to `.env`:
   ```env
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_CLIENT_SECRET=your_client_secret
   REDDIT_USER_AGENT=PersonaBot/1.0 by YourUsername
   ```

### Google Gemini API (Required)

_Powers AI persona generation and entity extraction_

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Add to `.env`:
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   ```

### Neo4j Cloud Database (For GraphRAG Chat)

_Enables interactive Q&A with knowledge graphs_

1. **Sign up** at [Neo4j AuraDB](https://neo4j.com/cloud/aura/)
2. **Create** a new database instance
3. **Copy** connection details:
   - URI: `neo4j+s://your-instance.databases.neo4j.io`
   - Username: `neo4j`
   - Password: `your_generated_password`
4. **Add to `.env`**:
   ```env
   NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=your_password
   ```

> **💡 Tip**: Neo4j AuraDB offers a free tier perfect for testing and small projects!

## 🎯 How to Use

1. **🌐 Launch the App**

   ```bash
   streamlit run app.py
   ```

2. **👤 Enter Reddit Username**

   - Type any Reddit username (e.g., `kojied`)
   - Or paste a full Reddit profile URL

3. **📊 Generate Persona**

   - Click "Analyze User" to start the process
   - Watch real-time progress updates
   - View comprehensive personality analysis

4. **🤖 Interactive GraphRAG Chat**

   - Switch to "GraphRAG Chat" tab
   - Create knowledge graph from persona
   - Ask questions about the user's personality
   - Get AI-powered insights and analysis

5. **💾 Export Results**
   - Download as Text, PDF, or CSV
   - Share insights with others
   - Save for future reference

## 📁 Project Structure

```
Reddit-Persona-Bot/
├── src/
│   ├── reddit_scraper.py      # Reddit data scraping with PRAW & web fallback
│   ├── persona_generator.py   # AI persona generation using Gemini
│   └── graphrag_handler.py    # GraphRAG knowledge graph integration
├── output/                    # Generated personas and exported data
├── temp_graph/               # Temporary graph data files
├── app.py                    # Main Streamlit web application
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (create from .env.example)
├── .gitignore               # Git ignore rules
├── LICENSE                  # MIT License
└── README.md                # This documentation
```

## 🎨 Sample Output

### Persona Preview

```markdown
# Reddit User Persona: u/kojied

## 👤 User Profile

**Age Range:** Early to mid-30s
**Location:** New York City, USA
**Primary Interests:** Tech & Spatial Computing, Strategic Gaming, NYC Culture

## 🎯 Core Identity

Analytical, curious tech professional with interests in emerging technologies like Apple Vision Pro and visionOS development. Active in NYC-focused communities and enjoys strategic gaming.

## 🎮 Interests & Hobbies

- **Programming**: iOS/visionOS development, spatial computing
- **Gaming**: Strategy games, RPGs, simulation games
- **Technology**: Apple Vision Pro, AI/ML, emerging tech trends
- **Location**: NYC restaurants, biking, urban culture
```

### GraphRAG Chat Example

```
🧑 You: What are their main interests?
🤖 Assistant: Based on the knowledge graph, kojied's main interests include:

1. **Technology & Development**: Active iOS/visionOS developer with strong interest in Apple Vision Pro and spatial computing
2. **Strategic Gaming**: Enjoys simulation games, RPGs, and strategy games
3. **NYC Culture**: Actively participates in NYC-focused communities, enjoys local dining and biking
4. **Emerging Tech**: Stays current with AI/ML trends and cutting-edge technology

They appear to be a tech-savvy professional who balances work interests with gaming hobbies and urban lifestyle activities.
```

## 🛠️ Technical Details

### Dependencies

- **Python 3.10+**: Core language requirement
- **Streamlit**: Web interface framework
- **PRAW**: Reddit API client
- **Google Generative AI**: Gemini API integration
- **Neo4j**: Graph database for knowledge graphs
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations

### Data Sources

- **Reddit API**: Primary data source via PRAW
- **Web Scraping**: Fallback when API is unavailable
- **Public Data Only**: No private messages or sensitive information

### GraphRAG Features

- **Entity Extraction**: Identifies interests, traits, and behaviors
- **Relationship Mapping**: Connects related concepts and patterns
- **Multi-User Support**: Separate knowledge graphs per user
- **Interactive Q&A**: Natural language queries about personas

## 🔒 Privacy & Ethics

- 🔐 **Public Data Only**: Analyzes publicly available Reddit content
- 🤖 **No Personal Info**: No private messages or personal data collection
- 📝 **Educational Use**: Intended for research and educational purposes
- ⚖️ **Terms of Service**: Users must comply with Reddit's Terms of Service
- 🛡️ **Data Security**: API keys stored locally in `.env` file
- 🗑️ **Data Cleanup**: Temporary files automatically cleaned after processing

## 🐛 Troubleshooting

### Common Issues

**❌ "Reddit API Not Connected"**

- Check your `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET` in `.env`
- Verify your app is set to "script" type in Reddit preferences
- The app will fallback to web scraping if API fails

**❌ "Gemini API Not Configured"**

- Ensure `GEMINI_API_KEY` is correctly set in `.env`
- Verify your API key is active at [Google AI Studio](https://aistudio.google.com/app/apikey)

**❌ "Neo4j Connection Failed"**

- Check your Neo4j AuraDB instance is running
- Verify `NEO4J_URI`, `NEO4J_USERNAME`, and `NEO4J_PASSWORD` in `.env`
- Ensure firewall allows connections to Neo4j cloud

**❌ "No persona generated"**

- User might have very little public activity
- Check if the username exists and has public posts/comments
- Try with a different user with more activity

### Getting Help

- 📖 Check the [Wiki](https://github.com/Atharvakamtalwar/Reddit-Persona-Bot/wiki) for detailed guides
- 🐛 Report bugs in [Issues](https://github.com/Atharvakamtalwar/Reddit-Persona-Bot/issues)
- 💬 Join discussions in [Discussions](https://github.com/Atharvakamtalwar/Reddit-Persona-Bot/discussions)

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/Reddit-Persona-Bot.git
cd Reddit-Persona-Bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Reddit API**: For providing access to user data
- **Google Gemini**: For powerful AI analysis capabilities
- **Neo4j**: For graph database technology
- **Streamlit**: For the beautiful web interface framework
- **Open Source Community**: For various Python libraries used

---

<div align="center">

**Made with ❤️ for the Reddit community**

[![GitHub stars](https://img.shields.io/github/stars/Atharvakamtalwar/Reddit-Persona-Bot?style=social)](https://github.com/Atharvakamtalwar/Reddit-Persona-Bot/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Atharvakamtalwar/Reddit-Persona-Bot?style=social)](https://github.com/Atharvakamtalwar/Reddit-Persona-Bot/network/members)

</div>
