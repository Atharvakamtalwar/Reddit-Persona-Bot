"""
Reddit User Data Scraper
This module handles scraping Reddit user data using PRAW and the Reddit API.
"""

import praw
import pandas as pd
import requests
import json
import time
from datetime import datetime
from typing import List, Dict, Optional, Union
import os
from dotenv import load_dotenv

load_dotenv()


class RedditScraper:
    """Reddit user data scraper using PRAW and fallback web scraping."""
    
    def __init__(self):
        """Initialize the Reddit scraper with API credentials."""
        self.reddit = None
        self.setup_praw()
    
    def setup_praw(self):
        """Setup PRAW with Reddit API credentials."""
        try:
            client_id = os.getenv('REDDIT_CLIENT_ID')
            client_secret = os.getenv('REDDIT_CLIENT_SECRET')
            user_agent = os.getenv('REDDIT_USER_AGENT', 'PersonaBot/1.0')
            
            if not client_id or not client_secret:
                print("Reddit API credentials not found, will use web scraping")
                self.reddit = None
                return
            
            self.reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent
            )
            
            # Test the connection with a simple request instead of user.me()
            # This tests read-only access without authentication
            try:
                test_sub = self.reddit.subreddit('test')
                list(test_sub.hot(limit=1))
                print("✅ Reddit API connection successful")
            except Exception as test_e:
                print(f"Reddit API test failed: {test_e}")
                self.reddit = None
                
        except Exception as e:
            print(f"PRAW setup failed: {e}")
            self.reddit = None
    
    def extract_username_from_url(self, url: str) -> str:
        """Extract username from Reddit profile URL."""
        if '/user/' in url:
            username = url.split('/user/')[-1].rstrip('/')
        elif '/u/' in url:
            username = url.split('/u/')[-1].rstrip('/')
        else:
            # Assume it's just a username
            username = url.strip()
        return username
    
    def get_user_data_praw(self, username: str, limit: int = 100, progress_callback=None) -> Optional[Dict]:
        """Get user data using PRAW (preferred method)."""
        if not self.reddit:
            return None
        
        try:
            if progress_callback:
                progress_callback("🔍 Connecting to Reddit API...")
            
            user = self.reddit.redditor(username)
            
            if progress_callback:
                progress_callback("📝 Fetching user submissions...")
            
            # Get submissions (posts)
            submissions = []
            for i, submission in enumerate(user.submissions.new(limit=limit)):
                submissions.append({
                    'type': 'submission',
                    'id': submission.id,
                    'title': submission.title,
                    'selftext': submission.selftext,
                    'url': f"https://www.reddit.com{submission.permalink}",
                    'subreddit': submission.subreddit.display_name,
                    'score': submission.score,
                    'created_utc': submission.created_utc,
                    'num_comments': submission.num_comments
                })
                
                if progress_callback and i % 10 == 0:
                    progress_callback(f"📝 Fetched {i+1} submissions...")
            
            if progress_callback:
                progress_callback("💬 Fetching user comments...")
            
            # Get comments
            comments = []
            for i, comment in enumerate(user.comments.new(limit=limit)):
                comments.append({
                    'type': 'comment',
                    'id': comment.id,
                    'body': comment.body,
                    'url': f"https://www.reddit.com{comment.permalink}",
                    'subreddit': comment.subreddit.display_name,
                    'score': comment.score,
                    'created_utc': comment.created_utc,
                    'submission_title': comment.submission.title if hasattr(comment, 'submission') else ''
                })
                
                if progress_callback and i % 10 == 0:
                    progress_callback(f"💬 Fetched {i+1} comments...")
            
            if progress_callback:
                progress_callback("✅ Data collection complete!")
            
            return {
                'username': username,
                'submissions': submissions,
                'comments': comments,
                'total_submissions': len(submissions),
                'total_comments': len(comments),
                'scraped_at': datetime.now().isoformat(),
                'method': 'praw'
            }
        
        except Exception as e:
            print(f"PRAW scraping failed for {username}: {e}")
            return None
    
    def get_user_data_web(self, username: str, limit: int = 100, progress_callback=None) -> Dict:
        """Fallback method using web scraping."""
        if progress_callback:
            progress_callback("🌐 Switching to web scraping mode...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        }
        
        all_comments = []
        all_submissions = []
        after = None
        
        # Get comments
        try:
            if progress_callback:
                progress_callback("💬 Scraping user comments...")
            
            comment_batches = 0
            while len(all_comments) < limit:
                url = f"https://www.reddit.com/user/{username}/comments.json?limit=25"
                if after:
                    url += f"&after={after}"
                
                response = requests.get(url, headers=headers)
                
                if response.status_code == 403:
                    if progress_callback:
                        progress_callback("⚠️ Access forbidden - Reddit may be blocking requests")
                    print("Access forbidden: Reddit is blocking the request.")
                    break
                elif response.status_code != 200:
                    if progress_callback:
                        progress_callback(f"❌ Error fetching comments: {response.status_code}")
                    print(f"Error fetching comments: {response.status_code}")
                    break
                
                data = response.json()
                
                if 'data' not in data or 'children' not in data['data']:
                    break
                
                comments_batch = [item['data'] for item in data['data']['children'] if item['kind'] == 't1']
                if not comments_batch:
                    break
                
                for comment in comments_batch:
                    all_comments.append({
                        'type': 'comment',
                        'id': comment.get('id', ''),
                        'body': comment.get('body', ''),
                        'url': f"https://www.reddit.com{comment.get('permalink', '')}",
                        'subreddit': comment.get('subreddit', ''),
                        'score': comment.get('score', 0),
                        'created_utc': comment.get('created_utc', 0),
                        'submission_title': ''
                    })
                
                comment_batches += 1
                if progress_callback:
                    progress_callback(f"💬 Fetched {len(all_comments)} comments (batch {comment_batches})...")
                
                after = data['data']['after']
                if not after:
                    break
                
                time.sleep(1)  # Rate limiting
        
        except Exception as e:
            print(f"Error scraping comments: {e}")
            if progress_callback:
                progress_callback(f"❌ Error scraping comments: {e}")
        
        # Get submissions
        try:
            if progress_callback:
                progress_callback("📝 Scraping user submissions...")
            
            after = None
            submission_batches = 0
            while len(all_submissions) < limit:
                url = f"https://www.reddit.com/user/{username}/submitted.json?limit=25"
                if after:
                    url += f"&after={after}"
                
                response = requests.get(url, headers=headers)
                
                if response.status_code != 200:
                    if progress_callback:
                        progress_callback(f"❌ Error fetching submissions: {response.status_code}")
                    break
                
                data = response.json()
                
                if 'data' not in data or 'children' not in data['data']:
                    break
                
                submissions_batch = [item['data'] for item in data['data']['children'] if item['kind'] == 't3']
                if not submissions_batch:
                    break
                
                for submission in submissions_batch:
                    all_submissions.append({
                        'type': 'submission',
                        'id': submission.get('id', ''),
                        'title': submission.get('title', ''),
                        'selftext': submission.get('selftext', ''),
                        'url': f"https://www.reddit.com{submission.get('permalink', '')}",
                        'subreddit': submission.get('subreddit', ''),
                        'score': submission.get('score', 0),
                        'created_utc': submission.get('created_utc', 0),
                        'num_comments': submission.get('num_comments', 0)
                    })
                
                submission_batches += 1
                if progress_callback:
                    progress_callback(f"📝 Fetched {len(all_submissions)} submissions (batch {submission_batches})...")
                
                after = data['data']['after']
                if not after:
                    break
                
                time.sleep(1)  # Rate limiting
        
        except Exception as e:
            print(f"Error scraping submissions: {e}")
            if progress_callback:
                progress_callback(f"❌ Error scraping submissions: {e}")
        
        if progress_callback:
            progress_callback("✅ Web scraping complete!")
        
        return {
            'username': username,
            'submissions': all_submissions,
            'comments': all_comments,
            'total_submissions': len(all_submissions),
            'total_comments': len(all_comments),
            'scraped_at': datetime.now().isoformat(),
            'method': 'web_scraping'
        }
    
    def get_user_data(self, username_or_url: str, limit: int = 100, progress_callback=None) -> Optional[Dict]:
        """
        Get user data using the best available method.
        
        Args:
            username_or_url: Reddit username or profile URL
            limit: Maximum number of posts/comments to fetch
            progress_callback: Optional callback function for progress updates
            
        Returns:
            Dictionary containing user data or None if failed
        """
        if progress_callback:
            progress_callback("🔍 Extracting username...")
        
        username = self.extract_username_from_url(username_or_url)
        
        if progress_callback:
            progress_callback(f"👤 Analyzing user: u/{username}")
        
        # Try PRAW first
        if self.reddit:
            if progress_callback:
                progress_callback("🔌 Using Reddit API (PRAW)...")
            
            data = self.get_user_data_praw(username, limit, progress_callback)
            if data and (data['total_comments'] > 0 or data['total_submissions'] > 0):
                return data
        
        # Fallback to web scraping
        if progress_callback:
            progress_callback("🌐 Falling back to web scraping...")
        
        print("Falling back to web scraping...")
        data = self.get_user_data_web(username, limit, progress_callback)
        
        if data and (data['total_comments'] > 0 or data['total_submissions'] > 0):
            return data
        
        return None
    
    def save_raw_data(self, data: Dict, output_dir: str = "output") -> str:
        """Save raw scraped data to JSON file."""
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{output_dir}/{data['username']}_raw_data.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return filename
    
    def prepare_data_for_analysis(self, data: Dict) -> str:
        """Prepare scraped data for LLM analysis."""
        username = data['username']
        submissions = data['submissions']
        comments = data['comments']
        
        formatted_text = f"Reddit User Analysis Data for u/{username}\n"
        formatted_text += f"Scraped on: {data['scraped_at']}\n"
        formatted_text += f"Total Submissions: {len(submissions)}\n"
        formatted_text += f"Total Comments: {len(comments)}\n\n"
        
        # Add submissions
        if submissions:
            formatted_text += "=== SUBMISSIONS (POSTS) ===\n\n"
            for i, sub in enumerate(submissions[:20], 1):  # Limit to avoid token limits
                formatted_text += f"Submission {i}:\n"
                formatted_text += f"Title: {sub['title']}\n"
                formatted_text += f"Subreddit: r/{sub['subreddit']}\n"
                formatted_text += f"Score: {sub['score']}\n"
                formatted_text += f"URL: {sub['url']}\n"
                if sub['selftext']:
                    formatted_text += f"Content: {sub['selftext'][:500]}...\n"
                formatted_text += "\n"
        
        # Add comments
        if comments:
            formatted_text += "=== COMMENTS ===\n\n"
            for i, comment in enumerate(comments[:30], 1):  # Limit to avoid token limits
                formatted_text += f"Comment {i}:\n"
                formatted_text += f"Subreddit: r/{comment['subreddit']}\n"
                formatted_text += f"Score: {comment['score']}\n"
                formatted_text += f"Content: {comment['body'][:300]}...\n"
                formatted_text += f"URL: {comment['url']}\n"
                formatted_text += "\n"
        
        return formatted_text
