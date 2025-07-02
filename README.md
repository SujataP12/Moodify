# Moodify - Emotion-Based Playlist Generator

An intelligent music recommendation app that generates playlists based on your current mood using Spotify's API and machine learning.

## Features

- 🎭 Mood-based song recommendations (Happy, Sad, Angry, Calm, Energetic)
- 🎵 Spotify API integration for real-time music data
- 🤖 Machine learning model for mood classification
- 🎨 Beautiful UI with mood-specific themes and animations
- 📱 Available as both web app (Streamlit) and mobile app (Kivy)
- 🎧 30-second song previews
- ❤️ Save favorite songs

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create Spotify App at https://developer.spotify.com/
4. Copy `.env.example` to `.env` and add your Spotify credentials
5. Run data collection: `python data_collector.py`
6. Train the model: `python train_model.py`
7. Launch the app:
   - Web version: `streamlit run streamlit_app.py`
   - Mobile version: `python kivy_app.py`

## Project Structure

```
Moodify/
├── data_collector.py      # Spotify data collection
├── train_model.py         # ML model training
├── streamlit_app.py       # Web app
├── kivy_app.py           # Mobile app
├── mood_classifier.py     # ML model class
├── spotify_client.py      # Spotify API wrapper
├── data/                  # Dataset storage
├── models/               # Trained models
└── assets/               # UI assets
```
