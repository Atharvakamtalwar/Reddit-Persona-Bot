"""
Reddit User Persona Generator - Streamlit App
Main application for generating and displaying Reddit user personas.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
import json
from datetime import datetime
import sys
import io
import csv

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.reddit_scraper import RedditScraper
from src.persona_generator import PersonaGenerator


def setup_page():
    """Setup Streamlit page configuration."""
    st.set_page_config(
        page_title="Reddit User Persona Generator",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🤖 Reddit User Persona Generator")
    st.markdown("""
    Generate detailed user personas from Reddit activity using AI analysis.
    Enter a Reddit username or profile URL to get started.
    """)


def show_sidebar():
    """Display sidebar with configuration and information."""
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Status
        st.subheader("API Status")
        
        # Check Reddit API
        scraper = RedditScraper()
        if scraper.reddit:
            st.success("✅ Reddit API Connected")
        else:
            st.warning("⚠️ Reddit API Not Configured")
            with st.expander("Reddit API Setup"):
                st.markdown("""
                1. Go to [Reddit Apps](https://www.reddit.com/prefs/apps)
                2. Create a new app (script type)
                3. Copy your client ID and secret
                4. Add them to your .env file
                """)
        
        # Check Gemini API
        persona_gen = PersonaGenerator()
        if persona_gen.model:
            st.success("✅ Gemini API Connected")
        else:
            st.warning("⚠️ Gemini API Not Configured")
            with st.expander("Gemini API Setup"):
                st.markdown("""
                1. Get API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
                2. Add GEMINI_API_KEY to your .env file
                3. Restart the application
                """)
        
        st.divider()
        
        # Settings
        st.subheader("Settings")
        data_limit = st.slider("Data Limit", 50, 500, 100, 50,
                              help="Maximum number of posts/comments to analyze")
        
        show_raw_data = st.checkbox("Show Raw Data", False,
                                   help="Display scraped data in a separate tab")
        
        return data_limit, show_raw_data


def analyze_user_activity(reddit_data):
    """Analyze Reddit user activity for visualizations."""
    submissions = reddit_data['submissions']
    comments = reddit_data['comments']
    
    # Combine all data
    all_data = []
    
    # Process submissions
    for sub in submissions:
        all_data.append({
            'type': 'submission',
            'subreddit': sub['subreddit'],
            'score': sub['score'],
            'created_utc': sub['created_utc'],
            'text': f"{sub['title']} {sub['selftext']}"
        })
    
    # Process comments
    for comment in comments:
        all_data.append({
            'type': 'comment',
            'subreddit': comment['subreddit'],
            'score': comment['score'],
            'created_utc': comment['created_utc'],
            'text': comment['body']
        })
    
    if not all_data:
        return None
    
    df = pd.DataFrame(all_data)
    
    # Convert timestamps
    df['datetime'] = pd.to_datetime(df['created_utc'], unit='s')
    df['hour'] = df['datetime'].dt.hour
    df['day_of_week'] = df['datetime'].dt.day_name()
    
    # Calculate statistics
    total_posts = len(submissions)
    total_comments = len(comments)
    total_karma = df['score'].sum()
    avg_karma = df['score'].mean()
    
    # Top subreddits
    top_subreddits = df['subreddit'].value_counts().head(10)
    karma_by_subreddit = df.groupby('subreddit')['score'].sum().sort_values(ascending=False).head(10)
    
    # Activity patterns
    activity_by_hour = df['hour'].value_counts().sort_index()
    activity_by_day = df['day_of_week'].value_counts()
    
    # Most popular posts/comments
    most_upvoted = df.loc[df['score'].idxmax()] if not df.empty else None
    most_downvoted = df.loc[df['score'].idxmin()] if not df.empty else None
    
    return {
        'total_posts': total_posts,
        'total_comments': total_comments,
        'total_karma': total_karma,
        'avg_karma': avg_karma,
        'top_subreddits': top_subreddits,
        'karma_by_subreddit': karma_by_subreddit,
        'activity_by_hour': activity_by_hour,
        'activity_by_day': activity_by_day,
        'most_upvoted': most_upvoted,
        'most_downvoted': most_downvoted,
        'dataframe': df
    }


def generate_wordcloud(text):
    """Generate and display word cloud."""
    if not text or len(text.strip()) < 10:
        st.write("Not enough text data for word cloud generation.")
        return
    
    try:
        wordcloud = WordCloud(
            width=800, 
            height=400, 
            background_color='white',
            max_words=100,
            colormap='viridis'
        ).generate(text)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error generating word cloud: {e}")


def display_persona(persona_text, username):
    """Display the generated persona in a structured, user-friendly format."""
    st.header(f"🎭 User Persona: u/{username}")
    
    # Parse the persona text for better display
    lines = persona_text.split('\n')
    current_section = ""
    content = {}
    
    for line in lines:
        line = line.strip()
        if line.startswith('## '):
            current_section = line[3:].strip()
            content[current_section] = []
        elif line and current_section:
            content[current_section].append(line)
    
    # Display user profile prominently
    if '👤 User Profile' in content:
        st.markdown("### � User Profile")
        profile_content = '\n'.join(content['👤 User Profile'])
        st.markdown(profile_content)
        st.divider()
    
    # Core identity section
    if '🎯 Core Identity' in content:
        st.markdown("### 🎯 Core Identity")
        identity_content = '\n'.join(content['🎯 Core Identity'])
        st.markdown(identity_content)
        st.divider()
    
    # Create columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        # Interests & Hobbies
        if '🎮 Interests & Hobbies' in content:
            st.markdown("### 🎮 Interests & Hobbies")
            interests_content = '\n'.join(content['🎮 Interests & Hobbies'])
            st.markdown(interests_content)
        
        # Goals & Motivations
        if '🎯 Goals & Motivations' in content:
            st.markdown("### 🎯 Goals & Motivations")
            goals_content = '\n'.join(content['🎯 Goals & Motivations'])
            st.markdown(goals_content)
    
    with col2:
        # Values & Beliefs
        if '💭 Values & Beliefs' in content:
            st.markdown("### 💭 Values & Beliefs")
            values_content = '\n'.join(content['💭 Values & Beliefs'])
            st.markdown(values_content)
        
        # Frustrations & Pain Points
        if '😤 Frustrations & Pain Points' in content:
            st.markdown("### 😤 Frustrations & Pain Points")
            frustrations_content = '\n'.join(content['😤 Frustrations & Pain Points'])
            st.markdown(frustrations_content)
    
    # Behavioral patterns
    if '🔍 Behavioral Patterns' in content:
        st.markdown("### 🔍 Behavioral Patterns")
        behavior_content = '\n'.join(content['🔍 Behavioral Patterns'])
        st.markdown(behavior_content)
    
    # Activity summary
    if '📊 Activity Summary' in content:
        st.markdown("### 📊 Activity Summary")
        activity_content = '\n'.join(content['📊 Activity Summary'])
        st.markdown(activity_content)
    
    # Persona quote (highlighted)
    if '🎭 Persona Quote' in content:
        quote_content = '\n'.join(content['🎭 Persona Quote'])
        if quote_content.strip():
            st.markdown("### 💬 Persona Quote")
            st.markdown(f"> {quote_content}")
    
    # Summary
    if '📝 Summary' in content:
        st.markdown("### 📝 Summary")
        summary_content = '\n'.join(content['📝 Summary'])
        st.markdown(summary_content)
    
    # Citations in collapsible section
    if 'EVIDENCE SOURCES:' in persona_text:
        with st.expander("📎 View Sources & Citations"):
            sources_start = persona_text.find('EVIDENCE SOURCES:')
            if sources_start != -1:
                sources_text = persona_text[sources_start:]
                st.markdown(sources_text)
    
    # Recent activity highlights
    if '🔍 Recent Activity Highlights' in content:
        with st.expander("🔍 Recent Activity Highlights"):
            activity_content = '\n'.join(content['🔍 Recent Activity Highlights'])
            st.markdown(activity_content)
    
    # Enhancement notes
    if '📝 Enhancement Available' in content:
        with st.expander("ℹ️ About This Analysis"):
            enhancement_content = '\n'.join(content['📝 Enhancement Available'])
            st.markdown(enhancement_content)


def display_activity_analysis(analysis, reddit_data):
    """Display Reddit activity analysis and visualizations."""
    if not analysis:
        st.error("No activity data available for analysis.")
        return
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Posts", analysis['total_posts'])
    col2.metric("Total Comments", analysis['total_comments'])
    col3.metric("Total Karma", int(analysis['total_karma']))
    col4.metric("Avg Karma", f"{analysis['avg_karma']:.1f}")
    
    # Visualizations
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("📊 Top Subreddits")
        if len(analysis['top_subreddits']) > 0:
            fig_subs = px.bar(
                x=analysis['top_subreddits'].values,
                y=analysis['top_subreddits'].index,
                orientation='h',
                title="Most Active Subreddits",
                labels={'x': 'Posts/Comments', 'y': 'Subreddit'}
            )
            st.plotly_chart(fig_subs, use_container_width=True)
        else:
            st.write("No subreddit data available.")
        
        st.subheader("🕒 Activity by Hour")
        if len(analysis['activity_by_hour']) > 0:
            fig_hour = px.bar(
                x=analysis['activity_by_hour'].index,
                y=analysis['activity_by_hour'].values,
                title="Activity by Hour of Day",
                labels={'x': 'Hour', 'y': 'Posts/Comments'}
            )
            st.plotly_chart(fig_hour, use_container_width=True)
    
    with col_right:
        st.subheader("🏆 Karma by Subreddit")
        if len(analysis['karma_by_subreddit']) > 0:
            fig_karma = px.bar(
                x=analysis['karma_by_subreddit'].values,
                y=analysis['karma_by_subreddit'].index,
                orientation='h',
                title="Highest Karma Subreddits",
                labels={'x': 'Total Karma', 'y': 'Subreddit'}
            )
            st.plotly_chart(fig_karma, use_container_width=True)
        
        st.subheader("📅 Activity by Day")
        if len(analysis['activity_by_day']) > 0:
            fig_day = px.bar(
                x=analysis['activity_by_day'].index,
                y=analysis['activity_by_day'].values,
                title="Activity by Day of Week",
                labels={'x': 'Day', 'y': 'Posts/Comments'}
            )
            st.plotly_chart(fig_day, use_container_width=True)
    
    # Word cloud
    st.subheader("☁️ Word Cloud")
    if not analysis['dataframe'].empty and 'text' in analysis['dataframe'].columns:
        all_text = ' '.join(analysis['dataframe']['text'].fillna('').astype(str))
        if len(all_text.strip()) > 10:
            generate_wordcloud(all_text)
        else:
            st.write("Not enough text data for word cloud.")
    else:
        st.write("No text data available for word cloud.")
    
    # Top posts/comments
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⬆️ Most Upvoted")
        if analysis['most_upvoted'] is not None:
            most_up = analysis['most_upvoted']
            st.write(f"**Score:** {most_up['score']}")
            st.write(f"**Subreddit:** r/{most_up['subreddit']}")
            st.write(f"**Type:** {most_up['type']}")
            st.write(f"**Text:** {most_up['text'][:300]}...")
    
    with col2:
        st.subheader("⬇️ Most Downvoted")
        if analysis['most_downvoted'] is not None:
            most_down = analysis['most_downvoted']
            st.write(f"**Score:** {most_down['score']}")
            st.write(f"**Subreddit:** r/{most_down['subreddit']}")
            st.write(f"**Type:** {most_down['type']}")
            st.write(f"**Text:** {most_down['text'][:300]}...")


def display_raw_data(reddit_data):
    """Display raw scraped data."""
    st.subheader("📄 Raw Data Overview")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Scraping Method", reddit_data['method'])
        st.metric("Scraped At", reddit_data['scraped_at'])
    with col2:
        st.metric("Total Submissions", reddit_data['total_submissions'])
        st.metric("Total Comments", reddit_data['total_comments'])
    
    # Submissions
    if reddit_data['submissions']:
        st.subheader("📝 Submissions")
        subs_df = pd.DataFrame(reddit_data['submissions'])
        st.dataframe(subs_df)
    
    # Comments
    if reddit_data['comments']:
        st.subheader("💬 Comments")
        comments_df = pd.DataFrame(reddit_data['comments'])
        st.dataframe(comments_df)


def create_download_formats(persona_text, username, reddit_data):
    """Create multiple download formats for the persona."""
    
    # Format 1: Clean text format (no markdown)
    clean_text = persona_text.replace('#', '').replace('*', '').replace('_', '')
    clean_text = f"""
USER PERSONA REPORT
==================

Generated for: u/{username}
Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
Data Source: Reddit API via PRAW
Total Posts Analyzed: {reddit_data.get('total_submissions', 0)}
Total Comments Analyzed: {reddit_data.get('total_comments', 0)}

{clean_text}

---
Generated by Reddit User Persona Generator
https://github.com/yourusername/reddit-persona-generator
"""
    
    # Format 2: Professional PDF-ready format
    pdf_format = f"""
# USER PERSONA REPORT

**Subject:** u/{username}  
**Generated:** {datetime.now().strftime('%B %d, %Y')}  
**Data Points:** {reddit_data.get('total_submissions', 0)} posts, {reddit_data.get('total_comments', 0)} comments  

---

{persona_text}

---

**Methodology:** This persona was generated through AI analysis of publicly available Reddit posts and comments using Google Gemini API. The analysis identifies patterns in communication style, interests, and behavioral traits based on the user's posting history.

**Disclaimer:** This analysis is based solely on public Reddit activity and should not be considered a complete psychological profile. Individual privacy and consent should always be respected.

**Generated by:** Reddit User Persona Generator  
**Version:** 1.0.0
"""
    
    # Format 3: CSV data format for spreadsheet use
    csv_data = extract_persona_data_for_csv(persona_text, username, reddit_data)
    
    return {
        'clean_text': clean_text,
        'pdf_format': pdf_format,
        'csv_data': csv_data
    }

def extract_persona_data_for_csv(persona_text, username, reddit_data):
    """Extract structured data for CSV export."""
    
    # Parse persona for key data points
    lines = persona_text.split('\n')
    data_points = []
    
    current_section = ""
    for line in lines:
        line = line.strip()
        if line.startswith('## '):
            current_section = line[3:].strip()
        elif line.startswith('**') and ':' in line and current_section:
            key = line.split('**')[1].split(':')[0] if '**' in line else line.split(':')[0]
            value = ':'.join(line.split(':')[1:]).strip()
            data_points.append([current_section, key, value])
    
    # Create CSV content
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['Username', 'Category', 'Attribute', 'Value'])
    
    # Data
    for section, key, value in data_points:
        writer.writerow([username, section, key, value])
    
    # Summary stats
    writer.writerow([username, 'Statistics', 'Total Posts', reddit_data.get('total_submissions', 0)])
    writer.writerow([username, 'Statistics', 'Total Comments', reddit_data.get('total_comments', 0)])
    writer.writerow([username, 'Statistics', 'Analysis Date', datetime.now().strftime('%Y-%m-%d')])
    
    return output.getvalue()

def main():
    """Main Streamlit application."""
    setup_page()
    
    # Sidebar
    data_limit, show_raw_data = show_sidebar()
    
    # Main input
    st.header("🔍 User Analysis")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        user_input = st.text_input(
            "Enter Reddit username or profile URL:",
            placeholder="e.g., kojied or https://www.reddit.com/user/kojied/",
            help="You can enter just the username or the full Reddit profile URL"
        )
    
    with col2:
        analyze_button = st.button("🚀 Analyze User", type="primary")
    
    if analyze_button and user_input:
        # Initialize components
        scraper = RedditScraper()
        persona_generator = PersonaGenerator()
        
        username = scraper.extract_username_from_url(user_input)
        
        # Create progress container
        progress_container = st.empty()
        status_container = st.empty()
        
        # Progress callback function
        def update_progress(message):
            progress_container.info(message)
        
        try:
            # Scrape Reddit data with progress updates
            update_progress("🚀 Starting Reddit data scraping...")
            reddit_data = scraper.get_user_data(user_input, limit=data_limit, progress_callback=update_progress)
            
            if not reddit_data:
                progress_container.empty()
                st.error("❌ Could not retrieve data for this user. The user might not exist, have no posts/comments, or their profile might be private.")
                return
            
            # Save raw data
            update_progress("💾 Saving raw data...")
            raw_data_file = scraper.save_raw_data(reddit_data)
            
            # Show success message
            progress_container.empty()
            st.success(f"✅ Data scraped successfully! Found {reddit_data['total_submissions']} posts and {reddit_data['total_comments']} comments")
            st.info(f"📁 Raw data saved to: {raw_data_file}")
            
            # Generate persona with progress updates
            update_progress("🤖 Starting AI persona generation...")
            persona_text = persona_generator.generate_persona(reddit_data, progress_callback=update_progress)
            
            if persona_text:
                # Save persona
                update_progress("💾 Saving persona...")
                persona_file = persona_generator.save_persona(persona_text, username)
                
                # Clear progress and show success
                progress_container.empty()
                st.success(f"✅ Persona generated successfully! Saved to: {persona_file}")
                
                # Analyze activity
                update_progress("📊 Analyzing activity patterns...")
                activity_analysis = analyze_user_activity(reddit_data)
                progress_container.empty()
                
                # Create tabs for different views
                if show_raw_data:
                    tabs = st.tabs(["🎭 Persona", "📊 Activity Analysis", "📄 Raw Data"])
                else:
                    tabs = st.tabs(["🎭 Persona", "📊 Activity Analysis"])
                
                with tabs[0]:
                    display_persona(persona_text, username)
                    
                    # Create download options
                    download_formats = create_download_formats(persona_text, username, reddit_data)
                    
                    # Download section
                    st.subheader("📥 Download Options")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.download_button(
                            label="📄 Clean Text",
                            data=download_formats['clean_text'],
                            file_name=f"persona_{username}_{datetime.now().strftime('%Y%m%d')}.txt",
                            mime="text/plain",
                            key="download_clean",
                            help="Clean text format without markdown"
                        )
                    
                    with col2:
                        st.download_button(
                            label="� PDF Format",
                            data=download_formats['pdf_format'],
                            file_name=f"persona_{username}_{datetime.now().strftime('%Y%m%d')}.md",
                            mime="text/markdown",
                            key="download_pdf",
                            help="Professional format ready for PDF conversion"
                        )
                    
                    with col3:
                        st.download_button(
                            label="📊 CSV Data",
                            data=download_formats['csv_data'],
                            file_name=f"persona_{username}_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv",
                            key="download_csv",
                            help="Structured data for spreadsheet analysis"
                        )
                
                with tabs[1]:
                    st.header(f"📊 Activity Analysis for u/{username}")
                    display_activity_analysis(activity_analysis, reddit_data)
                
                if show_raw_data and len(tabs) > 2:
                    with tabs[2]:
                        display_raw_data(reddit_data)
            
            else:
                progress_container.empty()
                st.error("❌ Failed to generate persona. Please check your API configuration.")
                
        except Exception as e:
            progress_container.empty()
            st.error(f"❌ An error occurred: {str(e)}")
            st.exception(e)
    
    elif user_input and not analyze_button:
        st.info("👆 Click 'Analyze User' to start the analysis")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Reddit User Persona Generator | Built with Streamlit, PRAW, and Google Gemini</p>
        <p><small>⚠️ For educational purposes only. Please respect Reddit's terms of service.</small></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
