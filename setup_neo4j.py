#!/usr/bin/env python3
"""
Neo4j Setup Script for GraphRAG
Sets up Neo4j database for Reddit User Persona Generator
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header():
    """Print setup header."""
    print("🗄️  Neo4j Database Setup for GraphRAG")
    print("=" * 45)
    print()

def check_docker():
    """Check if Docker is installed and running."""
    try:
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Docker is installed")
            
            # Check if Docker is running
            result = subprocess.run(['docker', 'ps'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ Docker is running")
                return True
            else:
                print("❌ Docker is not running. Please start Docker Desktop.")
                return False
        else:
            print("❌ Docker is not installed")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Docker is not installed or not accessible")
        return False

def setup_neo4j_docker():
    """Setup Neo4j using Docker."""
    print("\n🐳 Setting up Neo4j with Docker...")
    
    # Check if Neo4j container already exists
    try:
        result = subprocess.run(['docker', 'ps', '-a', '--filter', 'name=neo4j-persona'],
                              capture_output=True, text=True)
        
        if 'neo4j-persona' in result.stdout:
            print("📦 Neo4j container already exists")
            
            # Check if it's running
            result = subprocess.run(['docker', 'ps', '--filter', 'name=neo4j-persona'],
                                  capture_output=True, text=True)
            
            if 'neo4j-persona' in result.stdout:
                print("✅ Neo4j container is running")
                return True
            else:
                print("🔄 Starting existing Neo4j container...")
                result = subprocess.run(['docker', 'start', 'neo4j-persona'],
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print("✅ Neo4j container started")
                    return True
                else:
                    print("❌ Failed to start Neo4j container")
                    return False
        else:
            print("🚀 Creating new Neo4j container...")
            
            # Create Neo4j container
            docker_cmd = [
                'docker', 'run', '--name', 'neo4j-persona',
                '-p', '7474:7474', '-p', '7687:7687',
                '-e', 'NEO4J_AUTH=neo4j/password',
                '-e', 'NEO4J_PLUGINS=["apoc"]',
                '-d', 'neo4j:latest'
            ]
            
            result = subprocess.run(docker_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Neo4j container created and started")
                print("📍 Neo4j Browser: http://localhost:7474")
                print("🔑 Username: neo4j")
                print("🔑 Password: password")
                return True
            else:
                print("❌ Failed to create Neo4j container")
                print(f"Error: {result.stderr}")
                return False
                
    except Exception as e:
        print(f"❌ Error setting up Neo4j: {e}")
        return False

def install_neo4j_desktop():
    """Provide instructions for Neo4j Desktop installation."""
    print("\n🖥️  Alternative: Neo4j Desktop Installation")
    print("-" * 40)
    
    system = platform.system()
    
    if system == "Windows":
        print("For Windows:")
        print("1. Download Neo4j Desktop from: https://neo4j.com/download/")
        print("2. Install and create a new database")
        print("3. Set password to 'password' (or update your .env file)")
        print("4. Start the database")
        
    elif system == "Darwin":  # macOS
        print("For macOS:")
        print("1. Install via Homebrew: brew install neo4j")
        print("2. Or download Neo4j Desktop from: https://neo4j.com/download/")
        print("3. Set password to 'password' (or update your .env file)")
        print("4. Start the database")
        
    else:  # Linux
        print("For Linux:")
        print("1. Install via package manager or download from: https://neo4j.com/download/")
        print("2. Set password to 'password' (or update your .env file)")
        print("3. Start the database")

def test_neo4j_connection():
    """Test Neo4j connection."""
    print("\n🔍 Testing Neo4j connection...")
    
    try:
        # Try to import neo4j driver
        from neo4j import GraphDatabase
        
        # Try to connect
        driver = GraphDatabase.driver(
            "bolt://localhost:7687",
            auth=("neo4j", "password")
        )
        
        with driver.session() as session:
            result = session.run("RETURN 'Hello Neo4j!' as message")
            record = result.single()
            
            if record:
                print("✅ Neo4j connection successful!")
                print(f"🎉 Response: {record['message']}")
                return True
            else:
                print("❌ No response from Neo4j")
                return False
                
    except ImportError:
        print("❌ Neo4j driver not installed")
        print("💡 Install with: pip install neo4j==5.16.0")
        return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("💡 Make sure Neo4j is running and credentials are correct")
        return False
    finally:
        try:
            driver.close()
        except:
            pass

def update_env_file():
    """Update .env file with Neo4j configuration."""
    print("\n📝 Updating .env file...")
    
    env_path = Path(".env")
    
    if not env_path.exists():
        print("❌ .env file not found")
        return False
    
    # Read existing content
    with open(env_path, 'r') as f:
        content = f.read()
    
    # Add Neo4j configuration if not present
    neo4j_config = """
# Neo4j Database Configuration (for GraphRAG)
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password"""
    
    if "NEO4J_URI" not in content:
        content += neo4j_config
        
        with open(env_path, 'w') as f:
            f.write(content)
        
        print("✅ .env file updated with Neo4j configuration")
    else:
        print("✅ Neo4j configuration already present in .env file")
    
    return True

def main():
    """Main setup function."""
    print_header()
    
    # Check Docker
    docker_available = check_docker()
    
    if docker_available:
        # Setup Neo4j with Docker
        neo4j_success = setup_neo4j_docker()
        
        if neo4j_success:
            # Wait a moment for Neo4j to start
            import time
            print("⏳ Waiting for Neo4j to start...")
            time.sleep(10)
            
            # Test connection
            connection_success = test_neo4j_connection()
            
            if connection_success:
                # Update .env file
                update_env_file()
                
                print("\n🎉 Neo4j setup completed successfully!")
                print("📍 Neo4j Browser: http://localhost:7474")
                print("🔑 Username: neo4j")
                print("🔑 Password: password")
                print("💡 You can now use the GraphRAG chat feature!")
                
            else:
                print("\n⚠️  Neo4j is running but connection failed")
                print("💡 Check the Neo4j logs and try again")
        else:
            print("\n❌ Failed to setup Neo4j with Docker")
            install_neo4j_desktop()
    else:
        print("\n🔄 Docker not available, showing alternative installation methods")
        install_neo4j_desktop()
    
    print("\n" + "=" * 45)
    print("🔗 Useful Links:")
    print("   Neo4j Desktop: https://neo4j.com/download/")
    print("   Neo4j Documentation: https://neo4j.com/docs/")
    print("   Docker Installation: https://docs.docker.com/get-docker/")

if __name__ == "__main__":
    main()
