#!/usr/bin/env python3
"""
Preview what your app will look like with real Spotify data
"""

import pandas as pd
import json

def create_realistic_sample_data():
    """Create realistic sample data that mimics real Spotify data"""
    print("🎵 Creating realistic sample data preview...")
    
    # Realistic song data based on actual popular songs
    realistic_data = [
        # Happy Songs
        {
            'mood': 'Happy',
            'track_id': 'spotify:track:4iV5W9uYEdYUVa79Axb7Rh',
            'track_name': 'Happy',
            'artist': 'Pharrell Williams',
            'album': 'G I R L',
            'popularity': 85,
            'danceability': 0.765,
            'energy': 0.822,
            'loudness': -5.817,
            'speechiness': 0.0583,
            'acousticness': 0.00146,
            'instrumentalness': 0.0,
            'liveness': 0.336,
            'valence': 0.962,
            'tempo': 159.96,
            'duration_ms': 232720,
            'time_signature': 4,
            'preview_url': 'https://p.scdn.co/mp3-preview/...',
            'image_url': 'https://i.scdn.co/image/ab67616d0000b273...'
        },
        {
            'mood': 'Happy',
            'track_name': 'Good as Hell',
            'artist': 'Lizzo',
            'album': 'Cuz I Love You',
            'popularity': 82,
            'danceability': 0.69,
            'energy': 0.83,
            'valence': 0.85,
            'tempo': 140.0
        },
        {
            'mood': 'Happy',
            'track_name': 'Uptown Funk',
            'artist': 'Mark Ronson ft. Bruno Mars',
            'album': 'Uptown Special',
            'popularity': 88,
            'danceability': 0.896,
            'energy': 0.842,
            'valence': 0.897,
            'tempo': 115.0
        },
        
        # Sad Songs
        {
            'mood': 'Sad',
            'track_name': 'Someone Like You',
            'artist': 'Adele',
            'album': '21',
            'popularity': 79,
            'danceability': 0.499,
            'energy': 0.244,
            'valence': 0.234,
            'tempo': 67.5
        },
        {
            'mood': 'Sad',
            'track_name': 'Mad World',
            'artist': 'Gary Jules',
            'album': 'Donnie Darko Soundtrack',
            'popularity': 71,
            'danceability': 0.289,
            'energy': 0.104,
            'valence': 0.0594,
            'tempo': 85.0
        },
        
        # Angry Songs
        {
            'mood': 'Angry',
            'track_name': 'Break Stuff',
            'artist': 'Limp Bizkit',
            'album': 'Significant Other',
            'popularity': 68,
            'danceability': 0.627,
            'energy': 0.973,
            'valence': 0.348,
            'tempo': 109.0
        },
        {
            'mood': 'Angry',
            'track_name': 'Bodies',
            'artist': 'Drowning Pool',
            'album': 'Sinner',
            'popularity': 65,
            'danceability': 0.456,
            'energy': 0.987,
            'valence': 0.267,
            'tempo': 152.0
        },
        
        # Calm Songs
        {
            'mood': 'Calm',
            'track_name': 'Weightless',
            'artist': 'Marconi Union',
            'album': 'Weightless',
            'popularity': 45,
            'danceability': 0.234,
            'energy': 0.089,
            'valence': 0.456,
            'tempo': 60.0
        },
        {
            'mood': 'Calm',
            'track_name': 'Clair de Lune',
            'artist': 'Claude Debussy',
            'album': 'Suite Bergamasque',
            'popularity': 52,
            'danceability': 0.123,
            'energy': 0.067,
            'valence': 0.389,
            'tempo': 72.0
        },
        
        # Energetic Songs
        {
            'mood': 'Energetic',
            'track_name': 'Titanium',
            'artist': 'David Guetta ft. Sia',
            'album': 'Nothing but the Beat',
            'popularity': 84,
            'danceability': 0.64,
            'energy': 0.78,
            'valence': 0.45,
            'tempo': 126.0
        },
        {
            'mood': 'Energetic',
            'track_name': 'Bangarang',
            'artist': 'Skrillex',
            'album': 'Bangarang EP',
            'popularity': 73,
            'danceability': 0.789,
            'energy': 0.923,
            'valence': 0.678,
            'tempo': 110.0
        }
    ]
    
    # Fill in missing fields with realistic defaults
    for song in realistic_data:
        song.setdefault('track_id', f"spotify:track:{'x' * 22}")
        song.setdefault('loudness', -6.0)
        song.setdefault('speechiness', 0.05)
        song.setdefault('acousticness', 0.2)
        song.setdefault('instrumentalness', 0.0)
        song.setdefault('liveness', 0.1)
        song.setdefault('duration_ms', 210000)
        song.setdefault('time_signature', 4)
        song.setdefault('preview_url', None)
        song.setdefault('image_url', None)
    
    return realistic_data

def show_data_comparison():
    """Show the difference between current and real data"""
    print("\n📊 DATA COMPARISON")
    print("=" * 50)
    
    print("🔴 CURRENT (Sample Data):")
    print("   • Track names: 'Happy Song 1', 'Sad Song 2'")
    print("   • Artists: 'Happy Artist 1', 'Sad Artist 2'")
    print("   • Albums: 'Happy Album 1', 'Sad Album 2'")
    print("   • No album art or previews")
    print("   • Synthetic audio features")
    
    print("\n🟢 WITH REAL SPOTIFY DATA:")
    realistic_data = create_realistic_sample_data()
    
    print("   • Real songs:")
    for song in realistic_data[:5]:
        print(f"     - '{song['track_name']}' by {song['artist']}")
    
    print("   • Real album artwork")
    print("   • 30-second song previews")
    print("   • Accurate audio analysis from Spotify")
    print("   • Real popularity scores")
    print("   • Thousands of songs across all moods")

def show_collection_process():
    """Explain what happens during data collection"""
    print("\n🔄 DATA COLLECTION PROCESS")
    print("=" * 50)
    
    print("When you run 'python3 data_collector.py', it will:")
    print("1. 🎵 Connect to Spotify API")
    print("2. 📋 Access curated playlists for each mood:")
    print("   • Happy: 'Happy Hits', 'Feel Good Pop'")
    print("   • Sad: 'Sad Songs', 'Melancholy Indie'")
    print("   • Angry: 'Rock Hard', 'Metal Mix'")
    print("   • Calm: 'Peaceful Piano', 'Ambient Chill'")
    print("   • Energetic: 'Workout', 'Electronic Dance'")
    print("3. 🔍 Search by genres for additional variety")
    print("4. 📊 Extract audio features for each song")
    print("5. 💾 Save ~1000+ real songs to CSV dataset")
    print("6. ⏱️  Takes about 10-15 minutes to complete")

def create_setup_checklist():
    """Create a setup checklist"""
    checklist = """
# 🎯 MOODIFY SETUP CHECKLIST

## ✅ Completed
- [x] App structure created
- [x] Dependencies installed  
- [x] ML model working
- [x] Demo data generated
- [x] Web app running

## 🔄 Next Steps (To Get Real Data)

### 1. Spotify Developer Setup (5 minutes)
- [ ] Go to https://developer.spotify.com/dashboard
- [ ] Create new app called "Moodify"
- [ ] Copy Client ID and Client Secret
- [ ] Update .env file with real credentials

### 2. Data Collection (15 minutes)
- [ ] Run: python3 test_spotify.py (verify connection)
- [ ] Run: python3 data_collector.py (collect real songs)
- [ ] Wait for ~1000 songs to be collected

### 3. Model Training (2 minutes)  
- [ ] Run: python3 train_model.py (retrain with real data)
- [ ] Model will be much more accurate

### 4. Launch Enhanced App
- [ ] Run: streamlit run streamlit_app.py
- [ ] Enjoy real music recommendations!

## 🎉 Final Result
Your app will have:
- Real song names, artists, albums
- Album artwork and previews
- Accurate mood classifications
- Professional-quality recommendations
"""
    
    with open('SETUP_CHECKLIST.md', 'w') as f:
        f.write(checklist)
    
    print("📋 Created SETUP_CHECKLIST.md for you to follow!")

def main():
    print("🎵 Moodify - Real Data Preview")
    print("=" * 50)
    
    show_data_comparison()
    show_collection_process()
    create_setup_checklist()
    
    print("\n🚀 READY TO UPGRADE?")
    print("Follow these steps to get real Spotify data:")
    print("1. Check 'spotify_setup_guide.md' for detailed instructions")
    print("2. Follow 'SETUP_CHECKLIST.md' step by step")
    print("3. Your app will transform from basic to professional!")

if __name__ == "__main__":
    main()
