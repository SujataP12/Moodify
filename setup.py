#!/usr/bin/env python3
"""
Moodify Setup Script
Automates the setup process for the Moodify application
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_requirements():
    """Install Python requirements"""
    return run_command("pip install -r requirements.txt", "Installing Python packages")

def setup_environment():
    """Setup environment file"""
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if env_example.exists() and not env_file.exists():
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env file and add your Spotify credentials")
        return True
    elif env_file.exists():
        print("✅ .env file already exists")
        return True
    else:
        print("❌ .env.example file not found")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['data', 'models', 'assets']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✅ Created necessary directories")
    return True

def check_spotify_credentials():
    """Check if Spotify credentials are configured"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        
        if client_id and client_secret and client_id != 'your_spotify_client_id_here':
            print("✅ Spotify credentials configured")
            return True
        else:
            print("⚠️  Spotify credentials not configured")
            print("   Please visit https://developer.spotify.com/ to create an app")
            print("   Then update your .env file with the credentials")
            return False
    except Exception as e:
        print(f"❌ Error checking Spotify credentials: {e}")
        return False

def main():
    """Main setup function"""
    print("🎵 Moodify Setup Script")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Setup environment
    setup_environment()
    
    # Install requirements
    if not install_requirements():
        print("❌ Failed to install requirements. Please check your Python environment.")
        sys.exit(1)
    
    # Check Spotify credentials
    credentials_ok = check_spotify_credentials()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed!")
    
    if credentials_ok:
        print("\n📋 Next steps:")
        print("1. Run: python data_collector.py (to collect training data)")
        print("2. Run: python train_model.py (to train the ML model)")
        print("3. Run: streamlit run streamlit_app.py (for web app)")
        print("4. Run: python kivy_app.py (for mobile app)")
    else:
        print("\n📋 Next steps:")
        print("1. Configure Spotify credentials in .env file")
        print("2. Run this setup script again")
        print("3. Follow the remaining steps above")
    
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main()
