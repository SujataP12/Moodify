#!/usr/bin/env python3
"""
Moodify Demo Script
Demonstrates the app functionality without requiring Spotify credentials
"""

import pandas as pd
import numpy as np
from mood_classifier import MoodClassifier
import os

def create_sample_dataset():
    """Create a sample dataset for demonstration"""
    print("🎵 Creating sample music dataset...")
    
    # Sample data with different mood characteristics
    sample_data = []
    
    # Happy songs characteristics
    for i in range(50):
        sample_data.append({
            'mood': 'Happy',
            'track_id': f'happy_{i}',
            'track_name': f'Happy Song {i+1}',
            'artist': f'Happy Artist {i+1}',
            'album': f'Happy Album {i+1}',
            'popularity': np.random.randint(60, 100),
            'danceability': np.random.uniform(0.6, 0.9),
            'energy': np.random.uniform(0.6, 0.9),
            'loudness': np.random.uniform(-8, -3),
            'speechiness': np.random.uniform(0.03, 0.15),
            'acousticness': np.random.uniform(0.1, 0.4),
            'instrumentalness': np.random.uniform(0.0, 0.1),
            'liveness': np.random.uniform(0.05, 0.25),
            'valence': np.random.uniform(0.7, 0.95),
            'tempo': np.random.uniform(110, 140),
            'duration_ms': np.random.randint(180000, 240000),
            'time_signature': 4,
            'preview_url': None,
            'image_url': None
        })
    
    # Sad songs characteristics
    for i in range(50):
        sample_data.append({
            'mood': 'Sad',
            'track_id': f'sad_{i}',
            'track_name': f'Sad Song {i+1}',
            'artist': f'Sad Artist {i+1}',
            'album': f'Sad Album {i+1}',
            'popularity': np.random.randint(40, 80),
            'danceability': np.random.uniform(0.2, 0.5),
            'energy': np.random.uniform(0.2, 0.5),
            'loudness': np.random.uniform(-15, -8),
            'speechiness': np.random.uniform(0.03, 0.1),
            'acousticness': np.random.uniform(0.4, 0.8),
            'instrumentalness': np.random.uniform(0.0, 0.3),
            'liveness': np.random.uniform(0.05, 0.2),
            'valence': np.random.uniform(0.1, 0.4),
            'tempo': np.random.uniform(60, 90),
            'duration_ms': np.random.randint(200000, 300000),
            'time_signature': 4,
            'preview_url': None,
            'image_url': None
        })
    
    # Angry songs characteristics
    for i in range(50):
        sample_data.append({
            'mood': 'Angry',
            'track_id': f'angry_{i}',
            'track_name': f'Angry Song {i+1}',
            'artist': f'Angry Artist {i+1}',
            'album': f'Angry Album {i+1}',
            'popularity': np.random.randint(50, 85),
            'danceability': np.random.uniform(0.3, 0.7),
            'energy': np.random.uniform(0.8, 0.98),
            'loudness': np.random.uniform(-5, -1),
            'speechiness': np.random.uniform(0.05, 0.3),
            'acousticness': np.random.uniform(0.0, 0.2),
            'instrumentalness': np.random.uniform(0.0, 0.4),
            'liveness': np.random.uniform(0.1, 0.4),
            'valence': np.random.uniform(0.2, 0.5),
            'tempo': np.random.uniform(120, 180),
            'duration_ms': np.random.randint(180000, 250000),
            'time_signature': 4,
            'preview_url': None,
            'image_url': None
        })
    
    # Calm songs characteristics
    for i in range(50):
        sample_data.append({
            'mood': 'Calm',
            'track_id': f'calm_{i}',
            'track_name': f'Calm Song {i+1}',
            'artist': f'Calm Artist {i+1}',
            'album': f'Calm Album {i+1}',
            'popularity': np.random.randint(30, 70),
            'danceability': np.random.uniform(0.2, 0.5),
            'energy': np.random.uniform(0.1, 0.4),
            'loudness': np.random.uniform(-20, -10),
            'speechiness': np.random.uniform(0.03, 0.08),
            'acousticness': np.random.uniform(0.5, 0.95),
            'instrumentalness': np.random.uniform(0.2, 0.8),
            'liveness': np.random.uniform(0.05, 0.15),
            'valence': np.random.uniform(0.3, 0.7),
            'tempo': np.random.uniform(50, 80),
            'duration_ms': np.random.randint(240000, 360000),
            'time_signature': 4,
            'preview_url': None,
            'image_url': None
        })
    
    # Energetic songs characteristics
    for i in range(50):
        sample_data.append({
            'mood': 'Energetic',
            'track_id': f'energetic_{i}',
            'track_name': f'Energetic Song {i+1}',
            'artist': f'Energetic Artist {i+1}',
            'album': f'Energetic Album {i+1}',
            'popularity': np.random.randint(60, 95),
            'danceability': np.random.uniform(0.7, 0.95),
            'energy': np.random.uniform(0.8, 0.98),
            'loudness': np.random.uniform(-6, -2),
            'speechiness': np.random.uniform(0.03, 0.2),
            'acousticness': np.random.uniform(0.0, 0.3),
            'instrumentalness': np.random.uniform(0.0, 0.2),
            'liveness': np.random.uniform(0.1, 0.3),
            'valence': np.random.uniform(0.6, 0.9),
            'tempo': np.random.uniform(120, 160),
            'duration_ms': np.random.randint(180000, 240000),
            'time_signature': 4,
            'preview_url': None,
            'image_url': None
        })
    
    # Create DataFrame and save
    df = pd.DataFrame(sample_data)
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/mood_music_dataset.csv', index=False)
    
    print(f"✅ Created sample dataset with {len(df)} tracks")
    print(f"Mood distribution:")
    print(df['mood'].value_counts())
    
    return df

def demo_model_training():
    """Demonstrate model training"""
    print("\n🤖 Training mood classification model...")
    
    classifier = MoodClassifier()
    train_acc, test_acc = classifier.train()
    
    print(f"✅ Model trained successfully!")
    print(f"Training accuracy: {train_acc:.3f}")
    print(f"Testing accuracy: {test_acc:.3f}")
    
    # Save the model
    classifier.save_model()
    print("✅ Model saved to models/ directory")
    
    return classifier

def demo_predictions(classifier):
    """Demonstrate mood predictions"""
    print("\n🎯 Testing mood predictions...")
    
    # Test different audio feature combinations
    test_cases = [
        {
            'name': 'Happy Pop Song',
            'features': {
                'danceability': 0.8,
                'energy': 0.7,
                'loudness': -5.0,
                'speechiness': 0.1,
                'acousticness': 0.2,
                'instrumentalness': 0.0,
                'liveness': 0.1,
                'valence': 0.9,
                'tempo': 120.0,
                'popularity': 75
            }
        },
        {
            'name': 'Melancholic Ballad',
            'features': {
                'danceability': 0.3,
                'energy': 0.2,
                'loudness': -12.0,
                'speechiness': 0.05,
                'acousticness': 0.7,
                'instrumentalness': 0.1,
                'liveness': 0.1,
                'valence': 0.2,
                'tempo': 70.0,
                'popularity': 60
            }
        },
        {
            'name': 'High Energy Dance',
            'features': {
                'danceability': 0.9,
                'energy': 0.95,
                'loudness': -3.0,
                'speechiness': 0.15,
                'acousticness': 0.1,
                'instrumentalness': 0.0,
                'liveness': 0.2,
                'valence': 0.8,
                'tempo': 128.0,
                'popularity': 85
            }
        }
    ]
    
    for test_case in test_cases:
        result = classifier.predict_mood(test_case['features'])
        print(f"\n🎵 {test_case['name']}:")
        print(f"   Predicted mood: {result['predicted_mood']}")
        print(f"   Confidence: {result['confidence']:.3f}")
        print(f"   All probabilities:")
        for mood, prob in result['all_probabilities'].items():
            print(f"     {mood}: {prob:.3f}")

def demo_streamlit_info():
    """Show information about running the Streamlit app"""
    print("\n🌐 Web App Information:")
    print("To run the Streamlit web app:")
    print("1. Make sure you have Spotify credentials in .env file")
    print("2. Run: export PATH=$PATH:/home/sujata/.local/bin")
    print("3. Run: streamlit run streamlit_app.py")
    print("4. Open your browser to the displayed URL (usually http://localhost:8501)")
    
    print("\n📱 Mobile App Information:")
    print("To run the Kivy mobile app:")
    print("1. Run: export PATH=$PATH:/home/sujata/.local/bin")
    print("2. Run: python3 kivy_app.py")
    print("3. The mobile app window will open")

def main():
    """Main demo function"""
    print("🎵 Moodify Demo - Emotion-Based Playlist Generator")
    print("=" * 60)
    
    try:
        # Create sample dataset
        df = create_sample_dataset()
        
        # Train model
        classifier = demo_model_training()
        
        # Test predictions
        demo_predictions(classifier)
        
        # Show app info
        demo_streamlit_info()
        
        print("\n🎉 Demo completed successfully!")
        print("\nNext steps:")
        print("1. Get Spotify Developer credentials from https://developer.spotify.com/")
        print("2. Update .env file with your credentials")
        print("3. Run: python3 data_collector.py (to get real Spotify data)")
        print("4. Run: python3 train_model.py (to retrain with real data)")
        print("5. Launch the web or mobile app!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
