"""
Setup script for Reddit User Persona Generator
Helps users configure the environment and API credentials.
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header():
    """Print setup header."""
    print("🤖 Reddit User Persona Generator - Setup")
    print("=" * 45)
    print()

def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 10):
        print("❌ Python 3.10+ is required. You have:", sys.version)
        print("   Please upgrade Python and try again.")
        return False
    else:
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detected")
        return True

def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print("   Try running: pip install -r requirements.txt")
        return False

def setup_env_file():
    """Setup environment file."""
    print("\n🔧 Setting up environment file...")
    
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if env_path.exists():
        print("✅ .env file already exists")
        overwrite = input("   Do you want to overwrite it? (y/N): ").lower().strip()
        if overwrite != 'y':
            return True
    
    if not env_example_path.exists():
        print("❌ .env.example file not found")
        return False
    
    # Copy example to .env
    with open(env_example_path, 'r') as f:
        content = f.read()
    
    with open(env_path, 'w') as f:
        f.write(content)
    
    print("✅ .env file created from template")
    return True

def get_api_credentials():
    """Guide user through API credential setup."""
    print("\n🔑 API Credentials Setup")
    print("-" * 25)
    
    # Reddit API
    print("\n1. Reddit API (Optional but recommended)")
    print("   • Go to: https://www.reddit.com/prefs/apps")
    print("   • Create a new app (script type)")
    print("   • Note your client ID and secret")
    
    setup_reddit = input("\n   Do you want to set up Reddit API now? (y/N): ").lower().strip()
    
    reddit_client_id = ""
    reddit_client_secret = ""
    reddit_user_agent = ""
    
    if setup_reddit == 'y':
        reddit_client_id = input("   Enter Reddit Client ID: ").strip()
        reddit_client_secret = input("   Enter Reddit Client Secret: ").strip()
        reddit_user_agent = input("   Enter User Agent (e.g., PersonaBot/1.0 by YourUsername): ").strip()
    
    # Gemini API
    print("\n2. Google Gemini API (Required for AI analysis)")
    print("   • Go to: https://aistudio.google.com/app/apikey")
    print("   • Create a new API key")
    print("   • Copy the key")
    
    gemini_api_key = input("\n   Enter Gemini API Key (required): ").strip()
    
    # Update .env file
    env_content = f"""# Reddit API Configuration
REDDIT_CLIENT_ID={reddit_client_id}
REDDIT_CLIENT_SECRET={reddit_client_secret}
REDDIT_USER_AGENT={reddit_user_agent}

# Gemini API Configuration
GEMINI_API_KEY={gemini_api_key}
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("✅ API credentials saved to .env file")
    
    if not gemini_api_key:
        print("⚠️  Warning: Gemini API key is required for AI persona generation")
        print("   You can add it later by editing the .env file")

def create_output_directory():
    """Create output directory."""
    print("\n📁 Creating output directory...")
    os.makedirs("output", exist_ok=True)
    print("✅ Output directory created")

def test_installation():
    """Test the installation."""
    print("\n🧪 Testing installation...")
    
    try:
        # Test imports
        sys.path.append('src')
        from src.reddit_scraper import RedditScraper
        from src.persona_generator import PersonaGenerator
        
        print("✅ Core modules imported successfully")
        
        # Test API connections
        scraper = RedditScraper()
        generator = PersonaGenerator()
        
        if scraper.reddit:
            print("✅ Reddit API connection successful")
        else:
            print("⚠️  Reddit API not configured (will use web scraping)")
        
        if generator.model:
            print("✅ Gemini API connection successful")
        else:
            print("❌ Gemini API not configured")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Some dependencies may not be installed correctly")
        return False
    except Exception as e:
        print(f"❌ Setup error: {e}")
        return False

def print_next_steps():
    """Print next steps for the user."""
    print("\n🎉 Setup Complete!")
    print("-" * 20)
    print("\nNext steps:")
    print("1. Start the web app:")
    print("   streamlit run app.py")
    print("\n2. Or use command line:")
    print("   python main.py --username kojied")
    print("\n3. Open browser to:")
    print("   http://localhost:8501")
    print("\n📚 For more info, see README.md")

def main():
    """Main setup function."""
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed. Please install dependencies manually.")
        sys.exit(1)
    
    # Setup environment
    if not setup_env_file():
        print("\n❌ Failed to setup environment file.")
        sys.exit(1)
    
    # Get API credentials
    get_api_credentials()
    
    # Create output directory
    create_output_directory()
    
    # Test installation
    if not test_installation():
        print("\n⚠️  Setup completed with warnings. Check the issues above.")
    
    # Show next steps
    print_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️  Setup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)
