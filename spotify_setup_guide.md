# Spotify API Setup Guide

## 1. Create Spotify Developer Account

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account (create one if needed)
3. Click "Create App"
4. Fill in the details:
   - **App Name**: Moodify
   - **App Description**: Emotion-based playlist generator
   - **Website**: http://localhost:8501 (for development)
   - **Redirect URI**: http://localhost:8501 (for development)
5. Accept terms and create the app

## 2. Get Your Credentials

1. Click on your newly created app
2. Click "Settings"
3. Copy your **Client ID**
4. Click "View client secret" and copy your **Client Secret**

## 3. Update Your .env File

Replace the placeholder values in your .env file:

```
SPOTIFY_CLIENT_ID=your_actual_client_id_here
SPOTIFY_CLIENT_SECRET=your_actual_client_secret_here
```

## 4. Test the Connection

Run this command to test your Spotify connection:
```bash
python3 -c "from spotify_client import SpotifyClient; client = SpotifyClient(); print('✅ Spotify connection successful!')"
```

## 5. Collect Real Data

Once credentials are set up, run:
```bash
python3 data_collector.py
```

This will collect real music data from Spotify playlists and genres.
