import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os

class MoodClassifier:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2
        )
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.feature_columns = [
            'danceability', 'energy', 'loudness', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 
            'valence', 'tempo', 'popularity'
        ]
        self.is_trained = False
    
    def load_data(self, filepath='data/mood_music_dataset.csv'):
        """Load the mood music dataset"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Dataset not found at {filepath}. Please run data_collector.py first.")
        
        df = pd.read_csv(filepath)
        print(f"Loaded dataset with {len(df)} tracks")
        print(f"Mood distribution:\n{df['mood'].value_counts()}")
        
        return df
    
    def preprocess_data(self, df):
        """Preprocess the data for training"""
        # Remove rows with missing values in feature columns
        df_clean = df.dropna(subset=self.feature_columns + ['mood'])
        
        # Extract features and target
        X = df_clean[self.feature_columns].copy()
        y = df_clean['mood'].copy()
        
        # Handle any remaining missing values
        X = X.fillna(X.mean())
        
        print(f"Preprocessed data shape: {X.shape}")
        print(f"Features used: {self.feature_columns}")
        
        return X, y
    
    def train(self, df=None, filepath='data/mood_music_dataset.csv'):
        """Train the mood classification model"""
        if df is None:
            df = self.load_data(filepath)
        
        # Preprocess data
        X, y = self.preprocess_data(df)
        
        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        print("Training Random Forest model...")
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        train_score = self.model.score(X_train_scaled, y_train)
        test_score = self.model.score(X_test_scaled, y_test)
        
        print(f"Training accuracy: {train_score:.3f}")
        print(f"Testing accuracy: {test_score:.3f}")
        
        # Cross-validation
        cv_scores = cross_val_score(self.model, X_train_scaled, y_train, cv=5)
        print(f"Cross-validation accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
        
        # Detailed evaluation
        y_pred = self.model.predict(X_test_scaled)
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=self.label_encoder.classes_))
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nFeature Importance:")
        print(feature_importance)
        
        self.is_trained = True
        return train_score, test_score
    
    def predict_mood(self, audio_features):
        """Predict mood from audio features"""
        if not self.is_trained:
            raise ValueError("Model not trained. Please train the model first.")
        
        # Convert to DataFrame if it's a dictionary
        if isinstance(audio_features, dict):
            audio_features = pd.DataFrame([audio_features])
        
        # Select and order features
        features = audio_features[self.feature_columns].copy()
        
        # Handle missing values
        features = features.fillna(features.mean())
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Predict
        predictions = self.model.predict(features_scaled)
        probabilities = self.model.predict_proba(features_scaled)
        
        # Decode labels
        mood_predictions = self.label_encoder.inverse_transform(predictions)
        
        # Create results with probabilities
        results = []
        for i, mood in enumerate(mood_predictions):
            prob_dict = dict(zip(self.label_encoder.classes_, probabilities[i]))
            results.append({
                'predicted_mood': mood,
                'confidence': max(probabilities[i]),
                'all_probabilities': prob_dict
            })
        
        return results[0] if len(results) == 1 else results
    
    def get_mood_characteristics(self):
        """Get the characteristic audio features for each mood"""
        if not hasattr(self, 'label_encoder') or not self.is_trained:
            # Return default characteristics if model not trained
            return {
                'Happy': {'valence': 0.8, 'energy': 0.7, 'danceability': 0.7, 'tempo': 120},
                'Sad': {'valence': 0.2, 'energy': 0.3, 'danceability': 0.4, 'tempo': 80},
                'Angry': {'valence': 0.3, 'energy': 0.9, 'danceability': 0.5, 'tempo': 140},
                'Calm': {'valence': 0.5, 'energy': 0.2, 'danceability': 0.3, 'tempo': 70},
                'Energetic': {'valence': 0.7, 'energy': 0.9, 'danceability': 0.8, 'tempo': 130}
            }
        
        # If model is trained, we could analyze the training data to get actual characteristics
        # For now, return the default values
        return self.get_mood_characteristics()
    
    def save_model(self, model_dir='models'):
        """Save the trained model and preprocessors"""
        if not self.is_trained:
            raise ValueError("Model not trained. Please train the model first.")
        
        os.makedirs(model_dir, exist_ok=True)
        
        # Save model components
        joblib.dump(self.model, os.path.join(model_dir, 'mood_classifier.pkl'))
        joblib.dump(self.scaler, os.path.join(model_dir, 'scaler.pkl'))
        joblib.dump(self.label_encoder, os.path.join(model_dir, 'label_encoder.pkl'))
        
        # Save feature columns
        with open(os.path.join(model_dir, 'feature_columns.txt'), 'w') as f:
            f.write('\n'.join(self.feature_columns))
        
        print(f"Model saved to {model_dir}/")
    
    def load_model(self, model_dir='models'):
        """Load a pre-trained model"""
        try:
            self.model = joblib.load(os.path.join(model_dir, 'mood_classifier.pkl'))
            self.scaler = joblib.load(os.path.join(model_dir, 'scaler.pkl'))
            self.label_encoder = joblib.load(os.path.join(model_dir, 'label_encoder.pkl'))
            
            # Load feature columns
            with open(os.path.join(model_dir, 'feature_columns.txt'), 'r') as f:
                self.feature_columns = [line.strip() for line in f.readlines()]
            
            self.is_trained = True
            print(f"Model loaded from {model_dir}/")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
