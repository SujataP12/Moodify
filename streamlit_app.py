import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from spotify_client import SpotifyClient
from mood_classifier import MoodClassifier
import os
import time

# Page configuration
st.set_page_config(
    page_title="Moodify - Emotion-Based Playlist Generator",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for mood-based themes
def load_css():
    st.markdown("""
    <style>
    .mood-button {
        padding: 20px;
        margin: 10px;
        border-radius: 15px;
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        border: none;
        color: white;
    }
    
    .happy-theme {
        background: linear-gradient(135deg, #FFD700, #FFA500);
    }
    
    .sad-theme {
        background: linear-gradient(135deg, #4682B4, #1E90FF);
    }
    
    .angry-theme {
        background: linear-gradient(135deg, #DC143C, #B22222);
    }
    
    .calm-theme {
        background: linear-gradient(135deg, #98FB98, #90EE90);
        color: #2F4F2F !important;
    }
    
    .energetic-theme {
        background: linear-gradient(135deg, #FF1493, #FF69B4);
    }
    
    .song-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #1DB954;
    }
    
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        border: none;
        padding: 10px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'selected_mood' not in st.session_state:
        st.session_state.selected_mood = None
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = []
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []

# Mood configuration
MOODS = {
    'Happy': {'emoji': '😊', 'color': '#FFD700', 'description': 'Upbeat and joyful music'},
    'Sad': {'emoji': '😢', 'color': '#4682B4', 'description': 'Melancholic and emotional music'},
    'Angry': {'emoji': '😠', 'color': '#DC143C', 'description': 'Intense and powerful music'},
    'Calm': {'emoji': '😌', 'color': '#98FB98', 'description': 'Peaceful and relaxing music'},
    'Energetic': {'emoji': '⚡', 'color': '#FF1493', 'description': 'High-energy and motivating music'}
}

@st.cache_resource
def load_spotify_client():
    """Load Spotify client with caching"""
    try:
        return SpotifyClient()
    except Exception as e:
        st.error(f"Failed to initialize Spotify client: {e}")
        st.info("Please check your .env file and ensure Spotify credentials are set correctly.")
        return None

@st.cache_resource
def load_mood_classifier():
    """Load mood classifier with caching"""
    classifier = MoodClassifier()
    if os.path.exists('models/mood_classifier.pkl'):
        classifier.load_model()
        return classifier
    else:
        st.warning("Mood classifier model not found. Using default recommendations.")
        return None

def display_mood_selector():
    """Display mood selection interface"""
    st.title("🎵 Moodify - Choose Your Mood")
    st.markdown("Select your current mood to get personalized music recommendations")
    
    cols = st.columns(len(MOODS))
    
    for i, (mood, config) in enumerate(MOODS.items()):
        with cols[i]:
            if st.button(
                f"{config['emoji']}\n{mood}\n{config['description']}", 
                key=f"mood_{mood}",
                help=f"Get {mood.lower()} music recommendations"
            ):
                st.session_state.selected_mood = mood
                st.rerun()

def get_recommendations(mood, spotify_client, limit=20):
    """Get music recommendations for selected mood"""
    try:
        # Get recommendations from Spotify
        track_ids = spotify_client.get_mood_based_recommendations(mood, limit=limit)
        
        recommendations = []
        for track_id in track_ids:
            track_info = spotify_client.get_track_info(track_id)
            if track_info:
                # Get audio features for additional info
                features = spotify_client.get_track_features(track_id)
                if features:
                    track_info.update({
                        'valence': features['valence'],
                        'energy': features['energy'],
                        'danceability': features['danceability'],
                        'tempo': features['tempo']
                    })
                recommendations.append(track_info)
        
        return recommendations
    except Exception as e:
        st.error(f"Error getting recommendations: {e}")
        return []

def display_recommendations(mood, recommendations):
    """Display music recommendations"""
    mood_config = MOODS[mood]
    
    # Header with mood theme
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {mood_config['color']}, {mood_config['color']}88); 
                padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px;">
        <h1 style="color: white; margin: 0;">{mood_config['emoji']} {mood} Playlist</h1>
        <p style="color: white; margin: 5px 0;">{mood_config['description']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not recommendations:
        st.warning("No recommendations found. Please try again.")
        return
    
    # Display recommendations
    st.subheader(f"🎶 {len(recommendations)} Songs for Your {mood} Mood")
    
    # Create columns for layout
    for i, track in enumerate(recommendations):
        with st.container():
            col1, col2, col3 = st.columns([1, 3, 1])
            
            with col1:
                # Display album art
                if track.get('image_url'):
                    st.image(track['image_url'], width=80)
                else:
                    st.markdown("🎵")
            
            with col2:
                # Track info
                st.markdown(f"**{track['name']}**")
                st.markdown(f"*by {track['artist']}*")
                st.markdown(f"Album: {track['album']}")
                
                # Audio features (if available)
                if 'valence' in track:
                    features_text = f"Mood: {track['valence']:.2f} | Energy: {track['energy']:.2f} | Tempo: {track['tempo']:.0f} BPM"
                    st.caption(features_text)
            
            with col3:
                # Action buttons
                if track.get('preview_url'):
                    st.markdown(f"[🎧 Preview]({track['preview_url']})")
                
                # Favorite button
                if st.button("❤️", key=f"fav_{i}", help="Add to favorites"):
                    if track not in st.session_state.favorites:
                        st.session_state.favorites.append(track)
                        st.success("Added to favorites!")
                    else:
                        st.info("Already in favorites!")
            
            st.divider()

def display_analytics(recommendations):
    """Display analytics about the recommendations"""
    if not recommendations or len(recommendations) == 0:
        return
    
    st.subheader("📊 Playlist Analytics")
    
    # Extract audio features
    features_data = []
    for track in recommendations:
        if all(key in track for key in ['valence', 'energy', 'danceability', 'tempo']):
            features_data.append({
                'Track': f"{track['name']} - {track['artist']}",
                'Valence': track['valence'],
                'Energy': track['energy'],
                'Danceability': track['danceability'],
                'Tempo': track['tempo']
            })
    
    if features_data:
        df = pd.DataFrame(features_data)
        
        # Create visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            # Scatter plot: Valence vs Energy
            fig1 = px.scatter(
                df, x='Valence', y='Energy',
                hover_data=['Track'],
                title='Mood Distribution (Valence vs Energy)',
                color='Danceability',
                size='Tempo'
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Bar chart: Average features
            avg_features = df[['Valence', 'Energy', 'Danceability']].mean()
            fig2 = go.Figure(data=[
                go.Bar(x=avg_features.index, y=avg_features.values, 
                       marker_color=['#1DB954', '#FF6B6B', '#4ECDC4'])
            ])
            fig2.update_layout(title='Average Audio Features', yaxis_range=[0, 1])
            st.plotly_chart(fig2, use_container_width=True)

def display_favorites():
    """Display favorite songs"""
    st.subheader("❤️ Your Favorite Songs")
    
    if not st.session_state.favorites:
        st.info("No favorite songs yet. Add some from your recommendations!")
        return
    
    for i, track in enumerate(st.session_state.favorites):
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col1:
            if track.get('image_url'):
                st.image(track['image_url'], width=60)
        
        with col2:
            st.markdown(f"**{track['name']}** by *{track['artist']}*")
        
        with col3:
            if st.button("🗑️", key=f"remove_{i}", help="Remove from favorites"):
                st.session_state.favorites.pop(i)
                st.rerun()

def main():
    """Main application function"""
    load_css()
    init_session_state()
    
    # Load clients
    spotify_client = load_spotify_client()
    mood_classifier = load_mood_classifier()
    
    if not spotify_client:
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.title("🎵 Moodify")
        st.markdown("---")
        
        # Navigation
        page = st.selectbox("Navigate", ["Mood Selection", "Favorites", "About"])
        
        if st.session_state.selected_mood:
            st.markdown(f"**Current Mood:** {st.session_state.selected_mood} {MOODS[st.session_state.selected_mood]['emoji']}")
            
            if st.button("🔄 Get New Recommendations"):
                with st.spinner("Getting fresh recommendations..."):
                    st.session_state.recommendations = get_recommendations(
                        st.session_state.selected_mood, spotify_client
                    )
            
            if st.button("🎭 Change Mood"):
                st.session_state.selected_mood = None
                st.session_state.recommendations = []
                st.rerun()
        
        st.markdown("---")
        st.markdown(f"**Favorites:** {len(st.session_state.favorites)}")
    
    # Main content
    if page == "Mood Selection":
        if not st.session_state.selected_mood:
            display_mood_selector()
        else:
            # Get recommendations if not already loaded
            if not st.session_state.recommendations:
                with st.spinner(f"Finding perfect {st.session_state.selected_mood.lower()} songs for you..."):
                    st.session_state.recommendations = get_recommendations(
                        st.session_state.selected_mood, spotify_client
                    )
            
            # Display recommendations
            display_recommendations(st.session_state.selected_mood, st.session_state.recommendations)
            
            # Display analytics
            if st.session_state.recommendations:
                with st.expander("📊 View Playlist Analytics"):
                    display_analytics(st.session_state.recommendations)
    
    elif page == "Favorites":
        display_favorites()
    
    elif page == "About":
        st.title("About Moodify")
        st.markdown("""
        **Moodify** is an AI-powered music recommendation app that generates personalized playlists based on your current mood.
        
        ### Features:
        - 🎭 **5 Mood Categories**: Happy, Sad, Angry, Calm, Energetic
        - 🎵 **Spotify Integration**: Real-time music data and previews
        - 🤖 **Machine Learning**: Intelligent mood classification
        - 📊 **Analytics**: Visualize your music preferences
        - ❤️ **Favorites**: Save your favorite discoveries
        
        ### How it works:
        1. Select your current mood
        2. Our AI analyzes audio features like valence, energy, and tempo
        3. Get personalized song recommendations from Spotify
        4. Discover new music that matches your emotional state
        
        ### Built with:
        - Python & Streamlit
        - Spotify Web API
        - Scikit-learn
        - Plotly for visualizations
        """)

if __name__ == "__main__":
    main()
