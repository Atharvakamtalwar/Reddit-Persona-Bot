"""
Quick validation script to check if the fixes work.
"""

import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Test imports
try:
    from src.reddit_scraper import RedditScraper
    print("✅ Reddit scraper imported successfully")
except Exception as e:
    print(f"❌ Reddit scraper import failed: {e}")

try:
    from src.persona_generator import PersonaGenerator
    print("✅ Persona generator imported successfully")
except Exception as e:
    print(f"❌ Persona generator import failed: {e}")

# Test initialization
try:
    scraper = RedditScraper()
    print("✅ Reddit scraper initialized")
    
    # Test username extraction
    username = scraper.extract_username_from_url("https://www.reddit.com/user/kojied/")
    print(f"✅ Username extraction works: {username}")
    
except Exception as e:
    print(f"❌ Reddit scraper initialization failed: {e}")

try:
    generator = PersonaGenerator()
    print("✅ Persona generator initialized")
except Exception as e:
    print(f"❌ Persona generator initialization failed: {e}")

print("\n🎉 Basic validation complete!")
print("💡 If all tests passed, the app should work correctly.")
print("💡 Run: streamlit run app.py")
