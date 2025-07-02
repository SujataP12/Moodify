import pandas as pd
import time
import random
from spotify_client import SpotifyClient
import os

class MoodDataCollector:
    def __init__(self):
        self.spotify = SpotifyClient()
        self.mood_playlists = {
            'Happy': [
                '37i9dQZF1DX0XUsuxWHRQd',  # Happy Hits
                '37i9dQZF1DXdPec7aLTmlC',  # Happy Pop
                '37i9dQZF1DX9XIFQuFvzM4',  # Happy Country
            ],
            'Sad': [
                '37i9dQZF1DX7qK8ma5wgG1',  # Sad Songs
                '37i9dQZF1DWSqBruwoIXkA',  # Sad Indie
                '37i9dQZF1DX3YSRoSdA634',  # Melancholy
            ],
            'Angry': [
                '37i9dQZF1DWWOaP4H0w5b0',  # Angry Music
                '37i9dQZF1DX9qNs32fujYe',  # Rock Hard
                '37i9dQZF1DWTcqUzwhNmKv',  # Metal Mix
            ],
            'Calm': [
                '37i9dQZF1DWZqd5JICZI0u',  # Peaceful Piano
                '37i9dQZF1DX4sWSpwq3LiO',  # Peaceful Guitar
                '37i9dQZF1DX3Ogo9pFvBkY',  # Ambient Chill
            ],
            'Energetic': [
                '37i9dQZF1DX76Wlfdnj7AP',  # Beast Mode
                '37i9dQZF1DX0XUfTFmNBRM',  # Workout
                '37i9dQZF1DX4dyzvuaRJ0n',  # Electronic Mix
            ]
        }
        
        # Genre-based search terms for additional data
        self.mood_genres = {
            'Happy': ['pop', 'dance', 'funk', 'disco', 'reggae'],
            'Sad': ['indie', 'alternative', 'folk', 'blues', 'country'],
            'Angry': ['rock', 'metal', 'punk', 'hardcore', 'grunge'],
            'Calm': ['ambient', 'classical', 'new-age', 'meditation', 'acoustic'],
            'Energetic': ['electronic', 'house', 'techno', 'drum-and-bass', 'edm']
        }
    
    def collect_playlist_data(self, mood, playlist_ids, max_tracks_per_playlist=50):
        """Collect track data from playlists for a specific mood"""
        all_tracks = []
        
        for playlist_id in playlist_ids:
            print(f"Collecting tracks from playlist {playlist_id} for mood: {mood}")
            track_ids = self.spotify.get_playlist_tracks(playlist_id)
            
            # Limit tracks per playlist to avoid overwhelming data
            track_ids = track_ids[:max_tracks_per_playlist]
            
            for track_id in track_ids:
                try:
                    # Get track info
                    track_info = self.spotify.get_track_info(track_id)
                    if not track_info:
                        continue
                    
                    # Get audio features
                    features = self.spotify.get_track_features(track_id)
                    if not features:
                        continue
                    
                    # Combine data
                    track_data = {
                        'mood': mood,
                        'track_id': track_id,
                        'track_name': track_info['name'],
                        'artist': track_info['artist'],
                        'album': track_info['album'],
                        'popularity': track_info['popularity'],
                        'danceability': features['danceability'],
                        'energy': features['energy'],
                        'key': features['key'],
                        'loudness': features['loudness'],
                        'mode': features['mode'],
                        'speechiness': features['speechiness'],
                        'acousticness': features['acousticness'],
                        'instrumentalness': features['instrumentalness'],
                        'liveness': features['liveness'],
                        'valence': features['valence'],
                        'tempo': features['tempo'],
                        'duration_ms': features['duration_ms'],
                        'time_signature': features['time_signature'],
                        'preview_url': track_info['preview_url'],
                        'image_url': track_info['image_url']
                    }
                    
                    all_tracks.append(track_data)
                    print(f"Collected: {track_info['name']} by {track_info['artist']}")
                    
                    # Rate limiting
                    time.sleep(0.1)
                    
                except Exception as e:
                    print(f"Error processing track {track_id}: {e}")
                    continue
        
        return all_tracks
    
    def collect_genre_data(self, mood, genres, tracks_per_genre=30):
        """Collect additional track data by searching genres"""
        all_tracks = []
        
        for genre in genres:
            print(f"Searching for {genre} tracks for mood: {mood}")
            track_ids = self.spotify.search_tracks_by_genre(genre, limit=tracks_per_genre)
            
            for track_id in track_ids:
                try:
                    # Get track info
                    track_info = self.spotify.get_track_info(track_id)
                    if not track_info:
                        continue
                    
                    # Get audio features
                    features = self.spotify.get_track_features(track_id)
                    if not features:
                        continue
                    
                    # Combine data
                    track_data = {
                        'mood': mood,
                        'track_id': track_id,
                        'track_name': track_info['name'],
                        'artist': track_info['artist'],
                        'album': track_info['album'],
                        'popularity': track_info['popularity'],
                        'danceability': features['danceability'],
                        'energy': features['energy'],
                        'key': features['key'],
                        'loudness': features['loudness'],
                        'mode': features['mode'],
                        'speechiness': features['speechiness'],
                        'acousticness': features['acousticness'],
                        'instrumentalness': features['instrumentalness'],
                        'liveness': features['liveness'],
                        'valence': features['valence'],
                        'tempo': features['tempo'],
                        'duration_ms': features['duration_ms'],
                        'time_signature': features['time_signature'],
                        'preview_url': track_info['preview_url'],
                        'image_url': track_info['image_url']
                    }
                    
                    all_tracks.append(track_data)
                    print(f"Collected: {track_info['name']} by {track_info['artist']}")
                    
                    # Rate limiting
                    time.sleep(0.1)
                    
                except Exception as e:
                    print(f"Error processing track {track_id}: {e}")
                    continue
        
        return all_tracks
    
    def collect_all_data(self):
        """Collect data for all moods"""
        all_data = []
        
        for mood in self.mood_playlists.keys():
            print(f"\n=== Collecting data for {mood} mood ===")
            
            # Collect from playlists
            playlist_data = self.collect_playlist_data(
                mood, 
                self.mood_playlists[mood],
                max_tracks_per_playlist=30
            )
            all_data.extend(playlist_data)
            
            # Collect from genre searches
            genre_data = self.collect_genre_data(
                mood,
                self.mood_genres[mood],
                tracks_per_genre=20
            )
            all_data.extend(genre_data)
            
            print(f"Collected {len(playlist_data) + len(genre_data)} tracks for {mood}")
        
        return all_data
    
    def save_data(self, data, filename='mood_music_dataset.csv'):
        """Save collected data to CSV"""
        df = pd.DataFrame(data)
        
        # Remove duplicates based on track_id
        df = df.drop_duplicates(subset=['track_id'])
        
        # Save to data directory
        filepath = os.path.join('data', filename)
        df.to_csv(filepath, index=False)
        
        print(f"\nDataset saved to {filepath}")
        print(f"Total tracks: {len(df)}")
        print(f"Mood distribution:")
        print(df['mood'].value_counts())
        
        return df

def main():
    """Main function to collect and save mood music data"""
    print("Starting Moodify data collection...")
    
    collector = MoodDataCollector()
    
    try:
        # Collect all data
        data = collector.collect_all_data()
        
        # Save to CSV
        df = collector.save_data(data)
        
        print("\nData collection completed successfully!")
        print(f"Dataset shape: {df.shape}")
        
    except Exception as e:
        print(f"Error during data collection: {e}")

if __name__ == "__main__":
    main()
