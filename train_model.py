from mood_classifier import MoodClassifier
import os

def main():
    """Train and save the mood classification model"""
    print("Starting Moodify model training...")
    
    # Check if dataset exists
    dataset_path = 'data/mood_music_dataset.csv'
    if not os.path.exists(dataset_path):
        print(f"Dataset not found at {dataset_path}")
        print("Please run 'python data_collector.py' first to collect training data.")
        return
    
    # Initialize classifier
    classifier = MoodClassifier()
    
    try:
        # Train the model
        train_acc, test_acc = classifier.train()
        
        # Save the trained model
        classifier.save_model()
        
        print(f"\nModel training completed successfully!")
        print(f"Final training accuracy: {train_acc:.3f}")
        print(f"Final testing accuracy: {test_acc:.3f}")
        print("Model saved to models/ directory")
        
        # Test the model with sample predictions
        print("\n=== Testing Model Predictions ===")
        
        # Sample audio features for testing
        test_features = {
            'danceability': 0.8,
            'energy': 0.7,
            'loudness': -5.0,
            'speechiness': 0.1,
            'acousticness': 0.2,
            'instrumentalness': 0.0,
            'liveness': 0.1,
            'valence': 0.9,
            'tempo': 120.0,
            'popularity': 70
        }
        
        result = classifier.predict_mood(test_features)
        print(f"Sample prediction: {result['predicted_mood']} (confidence: {result['confidence']:.3f})")
        print("All probabilities:", {k: f"{v:.3f}" for k, v in result['all_probabilities'].items()})
        
    except Exception as e:
        print(f"Error during model training: {e}")

if __name__ == "__main__":
    main()
