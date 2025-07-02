import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
import pandas as pd
import time
import random

load_dotenv()

class SpotifyClient:
    def __init__(self):
        """Initialize Spotify client with credentials"""
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        
        if not client_id or not client_secret:
            raise ValueError("Spotify credentials not found. Please check your .env file.")
        
        client_credentials_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    def get_track_features(self, track_id):
        """Get audio features for a track"""
        try:
            features = self.sp.audio_features([track_id])[0]
            return features
        except Exception as e:
            print(f"Error getting features for track {track_id}: {e}")
            return None
    
    def get_track_info(self, track_id):
        """Get basic track information"""
        try:
            track = self.sp.track(track_id)
            return {
                'id': track['id'],
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'image_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
                'preview_url': track['preview_url'],
                'popularity': track['popularity']
            }
        except Exception as e:
            print(f"Error getting track info for {track_id}: {e}")
            return None
    
    def search_tracks_by_genre(self, genre, limit=50):
        """Search for tracks by genre"""
        try:
            results = self.sp.search(
                q=f'genre:{genre}',
                type='track',
                limit=limit,
                market='US'
            )
            return [track['id'] for track in results['tracks']['items']]
        except Exception as e:
            print(f"Error searching tracks for genre {genre}: {e}")
            return []
    
    def get_playlist_tracks(self, playlist_id):
        """Get tracks from a playlist"""
        try:
            results = self.sp.playlist_tracks(playlist_id)
            track_ids = []
            for item in results['items']:
                if item['track'] and item['track']['id']:
                    track_ids.append(item['track']['id'])
            return track_ids
        except Exception as e:
            print(f"Error getting playlist tracks: {e}")
            return []
    
    def get_recommendations(self, seed_genres=None, seed_tracks=None, 
                          target_valence=None, target_energy=None, 
                          target_tempo=None, limit=20):
        """Get track recommendations based on audio features"""
        try:
            recommendations = self.sp.recommendations(
                seed_genres=seed_genres,
                seed_tracks=seed_tracks,
                target_valence=target_valence,
                target_energy=target_energy,
                target_tempo=target_tempo,
                limit=limit,
                market='US'
            )
            return [track['id'] for track in recommendations['tracks']]
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return []
    
    def get_mood_based_recommendations(self, mood, limit=20):
        """Get recommendations based on mood with predefined parameters"""
        mood_params = {
            'Happy': {
                'target_valence': 0.8,
                'target_energy': 0.7,
                'target_tempo': 120,
                'seed_genres': ['pop', 'dance', 'funk']
            },
            'Sad': {
                'target_valence': 0.2,
                'target_energy': 0.3,
                'target_tempo': 80,
                'seed_genres': ['indie', 'alternative', 'folk']
            },
            'Angry': {
                'target_valence': 0.3,
                'target_energy': 0.9,
                'target_tempo': 140,
                'seed_genres': ['rock', 'metal', 'punk']
            },
            'Calm': {
                'target_valence': 0.5,
                'target_energy': 0.2,
                'target_tempo': 70,
                'seed_genres': ['ambient', 'classical', 'chill']
            },
            'Energetic': {
                'target_valence': 0.7,
                'target_energy': 0.9,
                'target_tempo': 130,
                'seed_genres': ['electronic', 'house', 'techno']
            }
        }
        
        if mood not in mood_params:
            mood = 'Happy'  # Default mood
        
        params = mood_params[mood]
        return self.get_recommendations(
            seed_genres=params['seed_genres'][:3],  # Spotify allows max 5 seeds total
            target_valence=params['target_valence'],
            target_energy=params['target_energy'],
            target_tempo=params['target_tempo'],
            limit=limit
        )
