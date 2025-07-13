"""
Command-line interface for Reddit User Persona Generator
Alternative to the Streamlit web interface for command-line usage.
"""

import argparse
import sys
import os
from typing import Optional

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.reddit_scraper import RedditScraper
from src.persona_generator import PersonaGenerator


def main():
    """Main command-line interface."""
    parser = argparse.ArgumentParser(
        description="Generate user personas from Reddit activity",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --url https://www.reddit.com/user/kojied/
  %(prog)s --username kojied --limit 200
  %(prog)s --username Hungry-Move-6603 --output custom_output/
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '--url',
        help='Reddit user profile URL (e.g., https://www.reddit.com/user/kojied/)'
    )
    input_group.add_argument(
        '--username',
        help='Reddit username (e.g., kojied)'
    )
    
    # Configuration options
    parser.add_argument(
        '--limit',
        type=int,
        default=100,
        help='Maximum number of posts/comments to analyze (default: 100)'
    )
    parser.add_argument(
        '--output',
        default='output',
        help='Output directory for generated files (default: output)'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Verbose output'
    )
    parser.add_argument(
        '--no-persona',
        action='store_true',
        help='Skip persona generation (only scrape and save raw data)'
    )
    
    args = parser.parse_args()
    
    # Determine input
    user_input = args.url if args.url else args.username
    
    if args.verbose:
        print(f"🚀 Starting Reddit User Persona Generator")
        print(f"📝 Target: {user_input}")
        print(f"📊 Data limit: {args.limit}")
        print(f"📁 Output directory: {args.output}")
        print("-" * 50)
    
    # Initialize components
    print("🔧 Initializing scraper...")
    scraper = RedditScraper()
    
    if not args.no_persona:
        print("🤖 Initializing persona generator...")
        persona_generator = PersonaGenerator()
    
    # Extract username
    username = scraper.extract_username_from_url(user_input)
    print(f"👤 Analyzing user: u/{username}")
    
    # Progress callback for command line
    def progress_callback(message):
        print(f"   {message}")
    
    # Scrape data
    print("🔍 Scraping Reddit data...")
    reddit_data = scraper.get_user_data(user_input, limit=args.limit, progress_callback=progress_callback)
    
    if not reddit_data:
        print("❌ Error: Could not retrieve data for this user.")
        print("   The user might not exist, have no posts/comments, or their profile might be private.")
        sys.exit(1)
    
    print(f"✅ Data scraped successfully!")
    print(f"   📊 Posts: {reddit_data['total_submissions']}")
    print(f"   💬 Comments: {reddit_data['total_comments']}")
    print(f"   📡 Method: {reddit_data['method']}")
    
    # Save raw data
    raw_data_file = scraper.save_raw_data(reddit_data, args.output)
    print(f"💾 Raw data saved: {raw_data_file}")
    
    if args.no_persona:
        print("⏭️  Skipping persona generation (--no-persona flag)")
        print("✨ Analysis complete!")
        return
    
    # Generate persona
    print("🧠 Generating AI persona...")
    persona_text = persona_generator.generate_persona(reddit_data, progress_callback=progress_callback)
    
    if persona_text:
        persona_file = persona_generator.save_persona(persona_text, username, args.output)
        print(f"🎭 Persona generated: {persona_file}")
        
        if args.verbose:
            print("\n" + "="*60)
            print("GENERATED PERSONA PREVIEW")
            print("="*60)
            # Show first 500 characters of persona
            preview = persona_text[:500] + "..." if len(persona_text) > 500 else persona_text
            print(preview)
            print("="*60)
        
        print("✨ Analysis complete!")
        print(f"📁 Check the '{args.output}' directory for all generated files.")
    else:
        print("❌ Error: Failed to generate persona.")
        print("   Please check your Gemini API configuration.")
        sys.exit(1)


def print_status():
    """Print API configuration status."""
    print("🔧 API Configuration Status:")
    print("-" * 30)
    
    # Check Reddit API
    scraper = RedditScraper()
    if scraper.reddit:
        print("✅ Reddit API: Connected")
    else:
        print("⚠️  Reddit API: Not configured (will use web scraping)")
    
    # Check Gemini API
    persona_gen = PersonaGenerator()
    if persona_gen.model:
        print("✅ Gemini API: Connected")
    else:
        print("❌ Gemini API: Not configured")
        print("   Get API key from: https://aistudio.google.com/app/apikey")
    
    print("-" * 30)


if __name__ == "__main__":
    # Check if user wants status
    if len(sys.argv) > 1 and sys.argv[1] in ['--status', 'status']:
        print_status()
        sys.exit(0)
    
    # Check if user wants help with no args
    if len(sys.argv) == 1:
        print("Reddit User Persona Generator - Command Line Interface")
        print("=" * 55)
        print_status()
        print()
        print("Usage examples:")
        print("  python main.py --username kojied")
        print("  python main.py --url https://www.reddit.com/user/kojied/")
        print("  python main.py --username kojied --limit 200 --verbose")
        print()
        print("For detailed help:")
        print("  python main.py --help")
        sys.exit(0)
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️  Analysis interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        if "--verbose" in sys.argv or "-v" in sys.argv:
            import traceback
            traceback.print_exc()
        sys.exit(1)
