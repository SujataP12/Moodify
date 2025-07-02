import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

class SimpleMoodClassifier:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        
    def prepare_features(self, df):
        """Create features from available data"""
        features = []
        
        # Text features from track name and artist
        text_features = df['track_name'] + ' ' + df['artist']
        text_vectors = self.vectorizer.fit_transform(text_features).toarray()
        
        # Numerical features
        numerical_features = []
        
        # Popularity (normalize to 0-1)
        popularity = df['popularity'].fillna(0) / 100
        numerical_features.append(popularity.values.reshape(-1, 1))
        
        # Duration (normalize to minutes)
        duration = df['duration_ms'].fillna(0) / 60000  # Convert to minutes
        numerical_features.append(duration.values.reshape(-1, 1))
        
        # Explicit content (binary)
        explicit = df['explicit'].astype(int)
        numerical_features.append(explicit.values.reshape(-1, 1))
        
        # Combine all features
        numerical_array = np.hstack(numerical_features)
        features = np.hstack([text_vectors, numerical_array])
        
        return features
    
    def train(self, csv_file='data/mood_music_data.csv'):
        """Train the mood classification model"""
        print("Loading data...")
        df = pd.read_csv(csv_file)
        
        print(f"Dataset shape: {df.shape}")
        print(f"Mood distribution:\n{df['mood'].value_counts()}")
        
        # Prepare features
        print("Preparing features...")
        X = self.prepare_features(df)
        y = df['mood']
        
        print(f"Feature matrix shape: {X.shape}")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print("Training model...")
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\n✅ Model trained successfully!")
        print(f"Accuracy: {accuracy:.3f}")
        print(f"\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        # Save model
        self.save_model()
        
        return accuracy
    
    def save_model(self):
        """Save the trained model and vectorizer"""
        os.makedirs('models', exist_ok=True)
        
        joblib.dump(self.model, 'models/mood_classifier.pkl')
        joblib.dump(self.vectorizer, 'models/text_vectorizer.pkl')
        
        print("Model saved to models/mood_classifier.pkl")
        print("Vectorizer saved to models/text_vectorizer.pkl")
    
    def load_model(self):
        """Load a previously trained model"""
        self.model = joblib.load('models/mood_classifier.pkl')
        self.vectorizer = joblib.load('models/text_vectorizer.pkl')
        print("Model loaded successfully!")
    
    def predict_mood(self, track_name, artist, popularity=50, duration_ms=200000, explicit=False):
        """Predict mood for a single track"""
        # Create a DataFrame with the input
        data = {
            'track_name': [track_name],
            'artist': [artist],
            'popularity': [popularity],
            'duration_ms': [duration_ms],
            'explicit': [explicit]
        }
        df = pd.DataFrame(data)
        
        # Prepare features (but don't fit vectorizer again)
        text_features = df['track_name'] + ' ' + df['artist']
        text_vectors = self.vectorizer.transform(text_features).toarray()
        
        # Numerical features
        popularity_norm = df['popularity'].fillna(0) / 100
        duration_norm = df['duration_ms'].fillna(0) / 60000
        explicit_bin = df['explicit'].astype(int)
        
        numerical_array = np.hstack([
            popularity_norm.values.reshape(-1, 1),
            duration_norm.values.reshape(-1, 1),
            explicit_bin.values.reshape(-1, 1)
        ])
        
        features = np.hstack([text_vectors, numerical_array])
        
        # Predict
        prediction = self.model.predict(features)[0]
        probabilities = self.model.predict_proba(features)[0]
        
        # Get class names
        classes = self.model.classes_
        prob_dict = dict(zip(classes, probabilities))
        
        return prediction, prob_dict

def main():
    print("Starting simple mood classification training...")
    
    # Check if data exists
    if not os.path.exists('data/mood_music_data.csv'):
        print("❌ No data found! Please run simple_data_collector.py first.")
        return
    
    try:
        classifier = SimpleMoodClassifier()
        accuracy = classifier.train()
        
        print(f"\n🎵 Testing the model with sample predictions:")
        
        # Test predictions
        test_cases = [
            ("Happy", "Pharrell Williams", 85, 232720, False),
            ("Sad", "Lana Del Rey", 80, 250000, False),
            ("Thunderstruck", "AC/DC", 90, 300000, False),
            ("Weightless", "Marconi Union", 60, 480000, False),
            ("Pump It Up", "Endor", 75, 180000, False)
        ]
        
        for track, artist, pop, dur, exp in test_cases:
            mood, probs = classifier.predict_mood(track, artist, pop, dur, exp)
            print(f"'{track}' by {artist} -> Predicted: {mood}")
            print(f"  Confidence: {max(probs.values()):.3f}")
        
    except Exception as e:
        print(f"❌ Error during training: {e}")

if __name__ == "__main__":
    main()
