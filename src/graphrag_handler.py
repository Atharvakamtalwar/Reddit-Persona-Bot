"""
GraphRAG Integration for Reddit User Persona Generator
Integrates with Neo4j LLM Graph Builder for graph-based Q&A
"""

import os
import sys
import json
import requests
import tempfile
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()


class GraphRAGHandler:
    """Handle GraphRAG operations for persona Q&A."""
    
    def __init__(self):
        """Initialize GraphRAG handler."""
        self.neo4j_uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        self.neo4j_user = os.getenv('NEO4J_USER', 'neo4j')
        self.neo4j_password = os.getenv('NEO4J_PASSWORD', 'password')
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        
        # Initialize Gemini for Q&A
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel('models/gemini-2.0-flash-exp')
        else:
            self.model = None
            
        # Track graph state per user
        self.user_graphs = {}  # {username: {'created': bool, 'data': dict}}
        
    def is_graph_created(self, username: str) -> bool:
        """Check if graph exists for specific user."""
        return self.user_graphs.get(username, {}).get('created', False)
    
    def get_graph_data(self, username: str) -> Optional[Dict]:
        """Get graph data for specific user."""
        return self.user_graphs.get(username, {}).get('data', None)
        
    def check_neo4j_connection(self) -> bool:
        """Check if Neo4j is accessible."""
        try:
            from neo4j import GraphDatabase
            driver = GraphDatabase.driver(self.neo4j_uri, auth=(self.neo4j_user, self.neo4j_password))
            with driver.session() as session:
                session.run("RETURN 1")
            driver.close()  
            return True
        except Exception as e:
            print(f"Neo4j connection failed: {e}")
            return False
    
    def create_graph_from_persona(self, persona_text: str, username: str, reddit_data: Optional[Dict] = None) -> bool:
        """Create knowledge graph from persona text."""
        try:
            # Try to load existing persona file first
            if not persona_text:
                loaded_persona = self._load_existing_persona_file(username)
                if not loaded_persona:
                    print(f"No persona text provided and no existing file found for {username}")
                    return False
                persona_text = loaded_persona
            
            # Create minimal reddit_data if not provided
            if not reddit_data:
                reddit_data = self._create_minimal_reddit_data(username)
            
            # Create temporary file with persona data
            persona_file = self._create_persona_file(persona_text, username, reddit_data)
            
            # Extract entities and relationships from persona
            entities_and_relations = self._extract_entities_and_relations(persona_text, username, reddit_data)
            
            if not entities_and_relations:
                return False
            
            # Create graph in Neo4j
            self._create_neo4j_graph(entities_and_relations, username)
            
            # Update user-specific graph state
            self.user_graphs[username] = {
                'created': True,
                'data': entities_and_relations
            }
            
            return True
            
        except Exception as e:
            print(f"Error creating graph: {e}")
            return False
    
    def _create_minimal_reddit_data(self, username: str) -> Dict:
        """Create minimal reddit_data structure for existing persona files."""
        return {
            'username': username,
            'total_submissions': 0,
            'total_comments': 0,
            'submissions': [],
            'comments': [],
            'method': 'file_load',
            'scraped_at': 'loaded_from_file'
        }
    
    def _create_persona_file(self, persona_text: str, username: str, reddit_data: Optional[Dict]) -> str:
        """Create a temporary file with persona data."""
        temp_dir = Path("temp_graph")
        temp_dir.mkdir(exist_ok=True)
        
        file_path = temp_dir / f"{username}_persona_graph.txt"
        
        # Ensure reddit_data is not None
        if reddit_data is None:
            reddit_data = self._create_minimal_reddit_data(username)
        
        # Enhanced persona data for graph creation
        enhanced_content = f"""
USER PERSONA GRAPH DATA
=====================

Username: {username}
Data Points: {reddit_data.get('total_submissions', 0)} posts, {reddit_data.get('total_comments', 0)} comments
Generated: {reddit_data.get('scraped_at', 'unknown')}

PERSONA CONTENT:
{persona_text}

ACTIVITY SUMMARY:
- Total Posts: {reddit_data.get('total_submissions', 0)}
- Total Comments: {reddit_data.get('total_comments', 0)}
- Scraping Method: {reddit_data.get('method', 'unknown')}

SUBREDDIT ACTIVITY:
"""
        
        # Add subreddit information
        subreddits = set()
        for submission in reddit_data.get('submissions', [])[:20]:  # Top 20 submissions
            if 'subreddit' in submission:
                subreddits.add(submission['subreddit'])
        
        for comment in reddit_data.get('comments', [])[:20]:  # Top 20 comments
            if 'subreddit' in comment:
                subreddits.add(comment['subreddit'])
        
        for subreddit in sorted(subreddits):
            enhanced_content += f"- r/{subreddit}\n"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(enhanced_content)
        
        return str(file_path)
    
    def _extract_entities_and_relations(self, persona_text: str, username: str, reddit_data: Dict) -> Optional[Dict]:
        """Extract entities and relationships using LLM."""
        if not self.model:
            return None
        
        extraction_prompt = f"""
You are an expert knowledge graph builder. Extract entities and relationships from this Reddit user persona to create a knowledge graph.

PERSONA DATA:
{persona_text}

REDDIT DATA:
- Username: {username}
- Posts: {reddit_data.get('total_submissions', 0)}
- Comments: {reddit_data.get('total_comments', 0)}

IMPORTANT INSTRUCTIONS:
1. Create unique IDs for each entity (e.g., "user_{username}", "interest_programming", "trait_analytical")
2. Ensure every relationship references valid entity IDs from the entities list
3. Include confidence scores (0.0-1.0) for relationships
4. Focus on extracting concrete, factual information

Extract the following in JSON format:

ENTITY TYPES:
- User: The Reddit user themselves
- Interest: Hobbies, topics, activities they care about
- Personality_Trait: Character traits and behavioral patterns
- Subreddit: Reddit communities they're active in
- Technology: Programming languages, tools, frameworks
- Location: Geographic locations mentioned
- Skill: Professional or personal competencies

RELATIONSHIP TYPES:
- HAS_INTEREST: User -> Interest
- HAS_TRAIT: User -> Personality_Trait
- ACTIVE_IN: User -> Subreddit
- SKILLED_IN: User -> Technology/Skill
- LIVES_IN: User -> Location
- RELATED_TO: Interest -> Interest
- REQUIRES: Skill -> Technology

Return ONLY valid JSON in this exact format:
{{
  "entities": [
    {{
      "id": "user_{username}",
      "type": "User",
      "properties": {{
        "name": "{username}",
        "age_range": "extracted_age_range",
        "location": "extracted_location",
        "description": "brief_description"
      }}
    }},
    {{
      "id": "interest_example",
      "type": "Interest",
      "properties": {{
        "name": "Interest Name",
        "category": "category",
        "confidence": 0.8
      }}
    }}
  ],
  "relationships": [
    {{
      "from": "user_{username}",
      "to": "interest_example",
      "type": "HAS_INTEREST",
      "properties": {{
        "strength": "high",
        "confidence": 0.9
      }}
    }}
  ]
}}

CRITICAL: Every entity must have a unique "id" field, and every relationship must reference valid entity IDs.
"""
        
        try:
            print(f"🤖 Calling Gemini API for entity extraction for user: {username}")
            print(f"📝 Prompt length: {len(extraction_prompt)} characters")
            
            response = self.model.generate_content(extraction_prompt)
            
            print(f"✅ Gemini API response received")
            print(f"📄 Response length: {len(response.text)} characters")
            
            # Clean and parse JSON response
            json_text = response.text.strip()
            print(f"🔍 Raw response preview: {json_text[:200]}...")
            
            if json_text.startswith('```json'):
                json_text = json_text[7:-3]
            elif json_text.startswith('```'):
                json_text = json_text[3:-3]
            
            graph_data = json.loads(json_text)
            
            print(f"✅ Successfully parsed JSON response")
            print(f"📊 Found {len(graph_data.get('entities', []))} entities")
            print(f"🔗 Found {len(graph_data.get('relationships', []))} relationships")
            
            # Debug: Print first few entities and relationships
            if graph_data.get('entities'):
                print(f"🎯 Sample entity: {graph_data['entities'][0]}")
            if graph_data.get('relationships'):
                print(f"🔗 Sample relationship: {graph_data['relationships'][0]}")
            
            return graph_data
            
        except Exception as e:
            print(f"❌ Error extracting entities: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _create_neo4j_graph(self, graph_data: Dict, username: str):
        """Create graph in Neo4j database."""
        try:
            from neo4j import GraphDatabase
            
            driver = GraphDatabase.driver(self.neo4j_uri, auth=(self.neo4j_user, self.neo4j_password))
            
            print(f"🗄️ Creating Neo4j graph for user: {username}")
            print(f"📊 Processing {len(graph_data.get('entities', []))} entities and {len(graph_data.get('relationships', []))} relationships")
            
            with driver.session() as session:
                # Clear existing data for this user
                print(f"🗑️ Clearing existing data for user: {username}")
                session.run("MATCH (n) WHERE n.username = $username DETACH DELETE n", parameters={"username": username})
                
                # Create entities
                print(f"🎯 Creating {len(graph_data.get('entities', []))} entities...")
                entities_created = 0
                for entity in graph_data.get('entities', []):
                    entity_type = entity['type']
                    properties = entity['properties'].copy()
                    properties['username'] = username  # Add username for filtering
                    properties['id'] = entity['id']  # Ensure id is set
                    
                    # Create entity node - using parameterized query to avoid SQL injection
                    query = f"CREATE (n:{entity_type}) SET n = $properties"
                    session.run(query, parameters={"properties": properties})
                    entities_created += 1
                
                print(f"✅ Created {entities_created} entities")
                
                # Create relationships
                print(f"🔗 Creating {len(graph_data.get('relationships', []))} relationships...")
                relationships_created = 0
                relationships_failed = 0
                
                for rel in graph_data.get('relationships', []):
                    from_id = rel['from']
                    to_id = rel['to']
                    rel_type = rel['type']
                    rel_props = rel.get('properties', {})
                    
                    # Create relationship - using parameterized query
                    query = f"""
                    MATCH (a {{id: $from_id, username: $username}})
                    MATCH (b {{id: $to_id, username: $username}})
                    CREATE (a)-[r:{rel_type}]->(b)
                    SET r = $rel_props
                    RETURN a, r, b
                    """
                    
                    result = session.run(query, parameters={
                        "from_id": from_id, 
                        "to_id": to_id, 
                        "username": username, 
                        "rel_props": rel_props
                    })
                    
                    # Check if relationship was created
                    if result.single():
                        relationships_created += 1
                        print(f"✅ Created relationship: {from_id} -> {rel_type} -> {to_id}")
                    else:
                        relationships_failed += 1
                        print(f"❌ Failed to create relationship: {from_id} -> {rel_type} -> {to_id}")
                        print(f"   (Check if entities with IDs {from_id} and {to_id} exist)")
                
                print(f"✅ Created {relationships_created} relationships")
                if relationships_failed > 0:
                    print(f"⚠️ Failed to create {relationships_failed} relationships")
                
                # Verify the graph was created
                verify_query = "MATCH (n) WHERE n.username = $username RETURN count(n) as node_count"
                result = session.run(verify_query, parameters={"username": username})
                record = result.single()
                node_count = record['node_count'] if record else 0
                print(f"🔍 Graph verification: {node_count} nodes created for user {username}")
                
                # Count relationships
                rel_query = "MATCH (a)-[r]->(b) WHERE a.username = $username AND b.username = $username RETURN count(r) as rel_count"
                result = session.run(rel_query, parameters={"username": username})
                record = result.single()
                rel_count = record['rel_count'] if record else 0
                print(f"🔍 Graph verification: {rel_count} relationships created for user {username}")
            
            driver.close()
            
        except Exception as e:
            print(f"❌ Error creating Neo4j graph: {e}")
            import traceback
            traceback.print_exc()
    
    def query_graph(self, question: str, username: str) -> str:
        """Query the knowledge graph to answer questions."""
        if not self.is_graph_created(username) or not self.model:
            return "Graph not created or AI model not available. Please ensure the graph is built and API keys are configured."
        
        try:
            print(f"🔍 Querying graph for user: {username}")
            print(f"❓ Question: {question}")
            
            # Get relevant graph data
            graph_context = self._get_graph_context(question, username)
            
            print(f"📊 Retrieved graph context ({len(graph_context)} characters)")
            
            # Generate answer using LLM with graph context
            answer_prompt = f"""
You are a helpful assistant that can answer questions about a Reddit user's persona based on their knowledge graph.

KNOWLEDGE GRAPH CONTEXT:
{graph_context}

USER QUESTION: {question}

Instructions:
1. Use the knowledge graph data to provide accurate, specific answers
2. Reference specific entities and relationships when relevant
3. If the information isn't in the graph, say so clearly
4. Provide insights based on the user's interests, traits, and activity patterns
5. Be conversational and helpful

Answer the question based on the knowledge graph:
"""
            
            print(f"🤖 Calling Gemini API for Q&A...")
            response = self.model.generate_content(answer_prompt)
            print(f"✅ Received Q&A response ({len(response.text)} characters)")
            
            return response.text
            
        except Exception as e:
            print(f"❌ Error querying graph: {str(e)}")
            import traceback
            traceback.print_exc()
            return f"Error querying graph: {str(e)}"
    
    def _get_graph_context(self, question: str, username: str) -> str:
        """Get relevant graph context for the question."""
        try:
            from neo4j import GraphDatabase
            
            driver = GraphDatabase.driver(self.neo4j_uri, auth=(self.neo4j_user, self.neo4j_password))
            
            with driver.session() as session:
                # Get all entities and relationships for the user
                query = """
                MATCH (n {username: $username})
                OPTIONAL MATCH (n)-[r]->(m {username: $username})
                RETURN n, r, m
                """
                result = session.run(query, parameters={"username": username})
                
                context_parts = []
                for record in result:
                    node = record['n']
                    rel = record['r']
                    target = record['m']
                    
                    # Format entity information
                    entity_info = f"Entity: {list(node.labels)[0]} - {dict(node)}"
                    context_parts.append(entity_info)
                    
                    # Format relationship information
                    if rel and target:
                        rel_info = f"Relationship: {node.get('name', node.get('id', 'Unknown'))} -> {rel.type} -> {target.get('name', target.get('id', 'Unknown'))}"
                        context_parts.append(rel_info)
                
                driver.close()
                return "\n".join(context_parts[:50])  # Limit context size
                
        except Exception as e:
            print(f"Error getting graph context: {e}")
            return "Error retrieving graph context"
    
    def get_suggested_questions(self, username: str) -> List[str]:
        """Get suggested questions based on the persona."""
        if not self.is_graph_created(username):
            return ["Please create the graph first"]
        
        suggestions = [
            f"What are {username}'s main interests?",
            f"What personality traits does {username} have?",
            f"Which subreddits is {username} most active in?",
            f"What technologies does {username} know about?",
            f"What can you tell me about {username}'s communication style?",
            f"What are {username}'s strengths and weaknesses?",
            f"How would you describe {username}'s online persona?",
            f"What topics does {username} care about most?"
        ]
        
        return suggestions
    
    def cleanup_graph(self, username: str):
        """Clean up graph data for a specific user."""
        try:
            from neo4j import GraphDatabase
            
            driver = GraphDatabase.driver(self.neo4j_uri, auth=(self.neo4j_user, self.neo4j_password))
            
            with driver.session() as session:
                session.run("MATCH (n) WHERE n.username = $username DETACH DELETE n", parameters={"username": username})
            
            driver.close()
            
            # Remove from user graphs tracking
            if username in self.user_graphs:
                del self.user_graphs[username]
            
        except Exception as e:
            print(f"Error cleaning up graph: {e}")
    
    def check_dependencies(self) -> Dict[str, bool]:
        """Check if all required dependencies are available."""
        checks = {
            'neo4j_driver': False,
            'neo4j_connection': False,
            'gemini_api': False
        }
        
        # Check Neo4j driver
        try:
            import neo4j
            checks['neo4j_driver'] = True
        except ImportError:
            pass
        
        # Check Neo4j connection
        checks['neo4j_connection'] = self.check_neo4j_connection()
        
        # Check Gemini API
        checks['gemini_api'] = self.model is not None
        
        return checks
    
    def _load_existing_persona_file(self, username: str) -> Optional[str]:
        """Load existing persona file from output folder."""
        output_dir = Path("output")
        
        # Try different possible filename patterns
        possible_files = [
            output_dir / f"{username}_persona.txt",
            output_dir / f"{username}.txt",
            output_dir / f"{username}_persona.md",
            output_dir / f"{username}.md"
        ]
        
        for file_path in possible_files:
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    print(f"✅ Loaded existing persona file: {file_path}")
                    return content
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
                    continue
        
        print(f"⚠️ No existing persona file found for {username}")
        return None
