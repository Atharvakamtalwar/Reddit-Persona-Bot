"""
LLM Persona Generator using Google Gemini API
This module handles generating user personas from Reddit data using Gemini.
"""

import google.generativeai as genai
import os
from typing import Dict, Optional
from dotenv import load_dotenv
import json
import re

load_dotenv()


class PersonaGenerator:
    """Generate user personas using Google Gemini API."""
    
    def __init__(self):
        """Initialize the Gemini API client."""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        else:
            self.model = None
            print("Warning: Gemini API key not found. Persona generation will be limited.")
    
    def create_persona_prompt(self, formatted_data: str, username: str) -> str:
        """Create a detailed prompt for persona generation."""
        prompt = f"""
You are an expert user researcher and data analyst. Analyze the following Reddit user data for u/{username} and create a comprehensive, user-friendly persona.

INSTRUCTIONS:
1. Analyze the user's posts, comments, and activity patterns
2. Create a persona that feels like a real person with:
   - Basic demographics (age range, location hints, lifestyle)
   - Core interests and hobbies
   - Personality traits and characteristics
   - Communication style and tone
   - Values and beliefs
   - Goals and motivations
   - Frustrations and pain points
   - Behavioral patterns

3. Make it engaging and human-readable, like a character profile
4. For sensitive inferences, use appropriate confidence qualifiers
5. Structure your response EXACTLY as follows:

# Reddit User Persona: u/{username}

## 👤 User Profile

**Age Range:** [Estimated age range based on references and communication style]
**Location:** [Inferred location based on posts/comments]
**Lifestyle:** [Brief description of their lifestyle]
**Primary Interests:** [Top 3-4 main interests]

## 🎯 Core Identity

### Personality Overview
[2-3 sentences describing their overall personality and approach to life]

### Communication Style
[How they communicate online - tone, style, approach]

## 🎮 Interests & Hobbies

### Primary Interests
- **[Interest 1]**: [Description of involvement and expertise level]
- **[Interest 2]**: [Description of involvement and expertise level]
- **[Interest 3]**: [Description of involvement and expertise level]

### Secondary Interests
- **[Interest 4]**: [Brief description]
- **[Interest 5]**: [Brief description]

## 💭 Values & Beliefs

### Core Values
- **[Value 1]**: [How this shows up in their posts]
- **[Value 2]**: [How this shows up in their posts]
- **[Value 3]**: [How this shows up in their posts]

### Perspectives
[Their general worldview and perspectives on life/society]

## 🎯 Goals & Motivations

### What Drives Them
- [Primary motivation 1]
- [Primary motivation 2]
- [Primary motivation 3]

### What They're Seeking
[What they seem to be looking for in their online interactions]

## 😤 Frustrations & Pain Points

### Common Frustrations
- [Frustration 1 based on complaints or negative comments]
- [Frustration 2]
- [Frustration 3]

### Challenges They Face
[Challenges they discuss or seem to encounter]

## 🔍 Behavioral Patterns

### Online Behavior
- **Activity Level**: [How often they post/comment]
- **Engagement Style**: [How they interact with others]
- **Content Preference**: [What type of content they create/engage with]

### Communication Patterns
- **Helpfulness**: [How helpful they are to others]
- **Expertise Sharing**: [How they share knowledge]
- **Community Involvement**: [How they participate in communities]

## 📊 Activity Summary

**Most Active In**: [Top 3 subreddits]
**Total Posts**: [Number]
**Total Comments**: [Number]
**Account Age Estimate**: [Based on references and posting patterns]

## 🎭 Persona Quote
"[A quote that would represent this user's perspective or approach to life, based on their communication style]"

## 📝 Summary
[2-3 sentences summarizing who this person is and what makes them unique]

---

EVIDENCE SOURCES:
[List key sources used for major inferences, formatted as: Topic - URL]

DATA TO ANALYZE:

{formatted_data}

Remember: Make this feel like a real person, not a dry analysis. Focus on creating an engaging, relatable persona while staying true to the evidence.
"""
        return prompt
    
    def generate_persona(self, reddit_data: Dict, progress_callback=None) -> Optional[str]:
        """
        Generate a user persona from Reddit data using Gemini.
        
        Args:
            reddit_data: Dictionary containing scraped Reddit data
            progress_callback: Optional callback function for progress updates
            
        Returns:
            Generated persona text or None if failed
        """
        if progress_callback:
            progress_callback("🤖 Initializing AI persona generation...")
        
        if not self.model:
            if progress_callback:
                progress_callback("⚠️ Gemini API not available, generating basic persona...")
            return self.generate_fallback_persona(reddit_data)
        
        try:
            if progress_callback:
                progress_callback("📊 Preparing data for AI analysis...")
            
            # Prepare data for analysis
            from .reddit_scraper import RedditScraper
            scraper = RedditScraper()
            formatted_data = scraper.prepare_data_for_analysis(reddit_data)
            
            if progress_callback:
                progress_callback("📝 Creating analysis prompt...")
            
            # Create prompt
            prompt = self.create_persona_prompt(formatted_data, reddit_data['username'])
            
            if progress_callback:
                progress_callback("🧠 Generating persona with AI...")
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                if progress_callback:
                    progress_callback("✅ AI persona generation complete!")
                return response.text
            else:
                if progress_callback:
                    progress_callback("⚠️ AI generation failed, creating fallback persona...")
                print("No response generated from Gemini API")
                return self.generate_fallback_persona(reddit_data)
                
        except Exception as e:
            if progress_callback:
                progress_callback(f"❌ AI generation error: {str(e)[:50]}...")
            print(f"Error generating persona with Gemini: {e}")
            return self.generate_fallback_persona(reddit_data)
    
    def generate_fallback_persona(self, reddit_data: Dict) -> str:
        """Generate a user-friendly persona without LLM when API is unavailable."""
        username = reddit_data['username']
        submissions = reddit_data['submissions']
        comments = reddit_data['comments']
        
        # Basic statistics
        total_submissions = len(submissions)
        total_comments = len(comments)
        
        # Get top subreddits
        subreddits = {}
        for item in submissions + comments:
            subreddit = item.get('subreddit', 'unknown')
            subreddits[subreddit] = subreddits.get(subreddit, 0) + 1
        
        top_subreddits = sorted(subreddits.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Analyze content for basic insights
        all_text = []
        for comment in comments[:10]:
            all_text.append(comment.get('body', ''))
        for submission in submissions[:5]:
            all_text.append(submission.get('title', ''))
            all_text.append(submission.get('selftext', ''))
        
        combined_text = ' '.join(all_text).lower()
        
        # Basic persona inference
        interests = []
        if any(word in combined_text for word in ['game', 'gaming', 'play']):
            interests.append("🎮 Gaming")
        if any(word in combined_text for word in ['tech', 'programming', 'code', 'software']):
            interests.append("💻 Technology")
        if any(word in combined_text for word in ['food', 'cooking', 'restaurant']):
            interests.append("🍽️ Food & Dining")
        if any(word in combined_text for word in ['travel', 'trip', 'vacation']):
            interests.append("✈️ Travel")
        if any(word in combined_text for word in ['music', 'song', 'band']):
            interests.append("🎵 Music")
        if any(word in combined_text for word in ['movie', 'film', 'show', 'tv']):
            interests.append("🎬 Entertainment")
        
        # Generate user-friendly persona
        persona = f"""# Reddit User Persona: u/{username}

## 👤 User Profile

**Activity Level:** {total_submissions} posts, {total_comments} comments
**Community Engagement:** Active in {len(subreddits)} different subreddits
**Primary Communities:** {', '.join([f"r/{sub}" for sub, _ in top_subreddits[:3]])}

## 🎯 Core Identity

### Personality Overview
This Reddit user demonstrates active engagement across multiple communities, showing curiosity and willingness to participate in diverse discussions.

### Communication Style
Based on their posting patterns, they appear to be a regular contributor who engages with various topics and communities.

## 🎮 Interests & Hobbies

### Identified Interests
"""
        
        if interests:
            for interest in interests[:4]:
                persona += f"- **{interest}**: Shows engagement through posts and comments\n"
        else:
            persona += "- **Community Engagement**: Active participant in Reddit discussions\n"
            persona += "- **Diverse Topics**: Engages with multiple subject areas\n"
        
        persona += f"""

### Top Communities
"""
        for i, (subreddit, count) in enumerate(top_subreddits[:5], 1):
            persona += f"{i}. **r/{subreddit}**: {count} posts/comments\n"
        
        persona += f"""

## 📊 Activity Summary

**Total Contributions:** {total_submissions + total_comments} posts and comments
**Community Diversity:** Active in {len(subreddits)} different subreddits
**Engagement Level:** {'High' if total_submissions + total_comments > 50 else 'Moderate' if total_submissions + total_comments > 20 else 'Light'} activity level

## 🔍 Recent Activity Highlights

"""
        
        # Add some sample content
        if comments:
            persona += "**Recent Comments:**\n"
            for i, comment in enumerate(comments[:3], 1):
                content = comment.get('body', '')[:150]
                if len(comment.get('body', '')) > 150:
                    content += "..."
                persona += f"{i}. In r/{comment.get('subreddit', 'unknown')}: \"{content}\"\n"
                persona += f"   📎 [View Source]({comment.get('url', '')})\n\n"
        
        if submissions:
            persona += "**Recent Posts:**\n"
            for i, submission in enumerate(submissions[:3], 1):
                title = submission.get('title', '')
                persona += f"{i}. \"{title}\" in r/{submission.get('subreddit', 'unknown')}\n"
                persona += f"   📎 [View Source]({submission.get('url', '')})\n\n"
        
        persona += f"""## 🎭 Persona Summary

u/{username} appears to be an engaged Reddit user who actively participates in community discussions across {len(subreddits)} different subreddits. Their activity pattern suggests someone who enjoys exploring diverse topics and contributing to conversations.

## 📝 Enhancement Available

This is a basic analysis generated without advanced AI processing. For a more detailed personality analysis with deeper insights into interests, communication patterns, and behavioral traits, configure the Gemini API key.

**To get enhanced persona analysis:**
1. Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Add it to your .env file as `GEMINI_API_KEY=your_key_here`
3. Re-run the analysis for comprehensive insights

---
*Generated on {reddit_data.get('scraped_at', 'Unknown date')} using {reddit_data.get('method', 'unknown method')}*
"""
        
        return persona
    
    def save_persona(self, persona_text: str, username: str, output_dir: str = "output") -> str:
        """Save generated persona to a text file."""
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{output_dir}/{username}_persona.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(persona_text)
        
        return filename
    
    def extract_persona_sections(self, persona_text: str) -> Dict:
        """Extract different sections from the persona for structured display."""
        sections = {
            'overview': '',
            'interests': '',
            'personality': '',
            'communication': '',
            'demographics': '',
            'values': '',
            'knowledge': '',
            'behavior': '',
            'summary': '',
            'limitations': ''
        }
        
        # Simple regex patterns to extract sections
        patterns = {
            'overview': r'## Overview\s*(.*?)(?=##|$)',
            'interests': r'### Interests & Hobbies\s*(.*?)(?=###|##|$)',
            'personality': r'### Personality Traits\s*(.*?)(?=###|##|$)',
            'communication': r'### Communication Style\s*(.*?)(?=###|##|$)',
            'demographics': r'### Demographics.*?\s*(.*?)(?=###|##|$)',
            'values': r'### Values & Beliefs\s*(.*?)(?=###|##|$)',
            'knowledge': r'### Knowledge Areas & Expertise\s*(.*?)(?=###|##|$)',
            'behavior': r'### Online Behavior Patterns\s*(.*?)(?=###|##|$)',
            'summary': r'## Summary Assessment\s*(.*?)(?=##|$)',
            'limitations': r'## Limitations & Notes\s*(.*?)(?=##|$)'
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, persona_text, re.DOTALL | re.IGNORECASE)
            if match:
                sections[key] = match.group(1).strip()
        
        return sections
