#!/usr/bin/env python3
"""
Test Spotify API connection and fetch some real data
"""

import os
from spotify_client import SpotifyClient
from dotenv import load_dotenv

def test_spotify_connection():
    """Test if Spotify credentials work"""
    print("🎵 Testing Spotify API connection...")
    
    # Load environment variables
    load_dotenv()
    
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    print(f"Client ID: {client_id[:10]}..." if client_id else "Client ID: Not found")
    print(f"Client Secret: {'*' * 10}" if client_secret else "Client Secret: Not found")
    
    if not client_id or client_id == 'your_spotify_client_id_here':
        print("❌ Spotify Client ID not configured")
        print("Please update your .env file with real Spotify credentials")
        return False
    
    if not client_secret or client_secret == 'your_spotify_client_secret_here':
        print("❌ Spotify Client Secret not configured")
        print("Please update your .env file with real Spotify credentials")
        return False
    
    try:
        # Initialize Spotify client
        spotify = SpotifyClient()
        print("✅ Spotify client initialized successfully")
        
        # Test search functionality
        print("\n🔍 Testing search functionality...")
        track_ids = spotify.search_tracks_by_genre('pop', limit=5)
        print(f"Found {len(track_ids)} pop tracks")
        
        if track_ids:
            # Get info for first track
            track_info = spotify.get_track_info(track_ids[0])
            if track_info:
                print(f"✅ Sample track: '{track_info['name']}' by {track_info['artist']}")
                
                # Get audio features
                features = spotify.get_track_features(track_ids[0])
                if features:
                    print(f"✅ Audio features: Valence={features['valence']:.2f}, Energy={features['energy']:.2f}")
        
        # Test mood-based recommendations
        print("\n🎭 Testing mood-based recommendations...")
        happy_tracks = spotify.get_mood_based_recommendations('Happy', limit=3)
        print(f"Found {len(happy_tracks)} happy song recommendations")
        
        if happy_tracks:
            for i, track_id in enumerate(happy_tracks[:2]):
                track_info = spotify.get_track_info(track_id)
                if track_info:
                    print(f"  {i+1}. '{track_info['name']}' by {track_info['artist']}")
        
        print("\n🎉 Spotify API connection test successful!")
        print("You can now collect real music data!")
        return True
        
    except Exception as e:
        print(f"❌ Spotify API connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check your Spotify credentials in .env file")
        print("2. Make sure your Spotify app is properly configured")
        print("3. Verify your internet connection")
        return False

def show_next_steps():
    """Show what to do next"""
    print("\n📋 Next Steps:")
    print("1. Run: python3 data_collector.py (collect real music data)")
    print("2. Run: python3 train_model.py (retrain model with real data)")
    print("3. Launch your app with real recommendations!")
    print("\n🎵 Your app will then have:")
    print("   • Real song names and artists")
    print("   • Album artwork")
    print("   • 30-second previews")
    print("   • Accurate mood classifications")

if __name__ == "__main__":
    print("🎵 Moodify - Spotify Connection Test")
    print("=" * 50)
    
    success = test_spotify_connection()
    
    if success:
        show_next_steps()
    else:
        print("\n📖 Setup Guide:")
        print("Please follow the instructions in 'spotify_setup_guide.md'")
        print("Or visit: https://developer.spotify.com/dashboard")
