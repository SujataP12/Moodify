import pandas as pd
import time
import random
from spotify_client import SpotifyClient
import os

class SimpleDataCollector:
    def __init__(self):
        self.spotify = SpotifyClient()
        
        # Use search-based approach instead of playlists
        self.mood_search_terms = {
            'Happy': ['happy', 'upbeat', 'cheerful', 'joyful', 'positive'],
            'Sad': ['sad', 'melancholy', 'heartbreak', 'emotional', 'lonely'],
            'Angry': ['angry', 'rage', 'aggressive', 'intense', 'furious'],
            'Calm': ['calm', 'peaceful', 'relaxing', 'meditation', 'ambient'],
            'Energetic': ['energetic', 'pump up', 'workout', 'high energy', 'motivational']
        }
        
        # Popular genres that usually work
        self.mood_genres = {
            'Happy': ['pop', 'dance', 'funk'],
            'Sad': ['indie', 'alternative', 'folk'],
            'Angry': ['rock', 'metal', 'punk'],
            'Calm': ['ambient', 'classical', 'acoustic'],
            'Energetic': ['electronic', 'house', 'edm']
        }
    
    def collect_data_by_search(self, mood, max_tracks=100):
        """Collect track data using search terms instead of playlists"""
        all_tracks = []
        search_terms = self.mood_search_terms[mood]
        
        print(f"\n=== Collecting data for {mood} mood ===")
        
        for term in search_terms:
            print(f"Searching for '{term}' tracks...")
            try:
                # Search for tracks
                results = self.spotify.sp.search(
                    q=term,
                    type='track',
                    limit=20,
                    market='US'
                )
                
                for track in results['tracks']['items']:
                    if len(all_tracks) >= max_tracks:
                        break
                        
                    try:
                        # Get basic track info
                        track_data = {
                            'mood': mood,
                            'track_id': track['id'],
                            'track_name': track['name'],
                            'artist': track['artists'][0]['name'],
                            'album': track['album']['name'],
                            'popularity': track['popularity'],
                            'preview_url': track['preview_url'],
                            'image_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
                            'duration_ms': track['duration_ms'],
                            'explicit': track['explicit']
                        }
                        
                        all_tracks.append(track_data)
                        print(f"Collected: {track['name']} by {track['artists'][0]['name']}")
                        
                        # Rate limiting
                        time.sleep(0.1)
                        
                    except Exception as e:
                        print(f"Error processing track: {e}")
                        continue
                        
            except Exception as e:
                print(f"Error searching for '{term}': {e}")
                continue
                
            if len(all_tracks) >= max_tracks:
                break
        
        return all_tracks
    
    def collect_all_moods(self, tracks_per_mood=50):
        """Collect data for all moods"""
        all_data = []
        
        for mood in self.mood_search_terms.keys():
            mood_data = self.collect_data_by_search(mood, tracks_per_mood)
            all_data.extend(mood_data)
            print(f"Collected {len(mood_data)} tracks for {mood} mood")
            
            # Longer pause between moods
            time.sleep(1)
        
        return all_data
    
    def save_data(self, data, filename='mood_music_data.csv'):
        """Save collected data to CSV"""
        if not data:
            print("No data to save!")
            return
            
        df = pd.DataFrame(data)
        
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        filepath = os.path.join('data', filename)
        df.to_csv(filepath, index=False)
        
        print(f"\nData saved to {filepath}")
        print(f"Total tracks collected: {len(df)}")
        print(f"Tracks per mood:")
        print(df['mood'].value_counts())
        
        return df

def main():
    print("Starting simplified Moodify data collection...")
    
    try:
        collector = SimpleDataCollector()
        
        # Collect data for all moods
        data = collector.collect_all_moods(tracks_per_mood=30)  # Start with smaller number
        
        # Save the data
        df = collector.save_data(data)
        
        print("\n✅ Data collection completed successfully!")
        print(f"Dataset shape: {df.shape}")
        
    except Exception as e:
        print(f"❌ Error during data collection: {e}")

if __name__ == "__main__":
    main()
