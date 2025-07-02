from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.image import AsyncImage
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.animation import Animation
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.list import OneLineListItem
from kivymd.theming import ThemableBehavior
import threading
from spotify_client import SpotifyClient
from mood_classifier import MoodClassifier
import os

class MoodButton(MDRaisedButton):
    """Custom mood selection button with animations"""
    def __init__(self, mood, emoji, color, **kwargs):
        super().__init__(**kwargs)
        self.mood = mood
        self.emoji = emoji
        self.text = f"{emoji} {mood}"
        self.md_bg_color = color
        self.size_hint = (1, None)
        self.height = "80dp"
        self.bind(on_press=self.animate_press)
    
    def animate_press(self, *args):
        """Animate button press"""
        anim = Animation(size=(self.width * 1.1, self.height * 1.1), duration=0.1)
        anim += Animation(size=(self.width, self.height), duration=0.1)
        anim.start(self)

class SongCard(MDCard):
    """Custom card for displaying song information"""
    def __init__(self, track_info, **kwargs):
        super().__init__(**kwargs)
        self.track_info = track_info
        self.orientation = "vertical"
        self.size_hint = (1, None)
        self.height = "120dp"
        self.padding = "10dp"
        self.spacing = "5dp"
        self.elevation = 2
        
        # Create layout
        main_layout = MDBoxLayout(orientation="horizontal", spacing="10dp")
        
        # Album art
        if track_info.get('image_url'):
            album_art = AsyncImage(
                source=track_info['image_url'],
                size_hint=(None, 1),
                width="80dp"
            )
            main_layout.add_widget(album_art)
        
        # Song info
        info_layout = MDBoxLayout(orientation="vertical", spacing="2dp")
        
        # Song name
        song_label = MDLabel(
            text=track_info['name'],
            theme_text_color="Primary",
            font_style="H6",
            size_hint_y=None,
            height="30dp"
        )
        info_layout.add_widget(song_label)
        
        # Artist
        artist_label = MDLabel(
            text=f"by {track_info['artist']}",
            theme_text_color="Secondary",
            font_style="Body2",
            size_hint_y=None,
            height="25dp"
        )
        info_layout.add_widget(artist_label)
        
        # Album
        album_label = MDLabel(
            text=track_info['album'],
            theme_text_color="Hint",
            font_style="Caption",
            size_hint_y=None,
            height="20dp"
        )
        info_layout.add_widget(album_label)
        
        main_layout.add_widget(info_layout)
        
        # Action buttons
        button_layout = MDBoxLayout(
            orientation="vertical",
            size_hint=(None, 1),
            width="50dp",
            spacing="5dp"
        )
        
        # Preview button
        if track_info.get('preview_url'):
            preview_btn = MDIconButton(
                icon="play",
                theme_icon_color="Custom",
                icon_color="green",
                on_press=lambda x: self.play_preview()
            )
            button_layout.add_widget(preview_btn)
        
        # Favorite button
        fav_btn = MDIconButton(
            icon="heart-outline",
            theme_icon_color="Custom",
            icon_color="red",
            on_press=lambda x: self.toggle_favorite()
        )
        button_layout.add_widget(fav_btn)
        
        main_layout.add_widget(button_layout)
        self.add_widget(main_layout)
    
    def play_preview(self):
        """Handle preview playback (placeholder)"""
        # In a real app, you would implement audio playback here
        print(f"Playing preview for {self.track_info['name']}")
    
    def toggle_favorite(self):
        """Toggle favorite status"""
        print(f"Toggled favorite for {self.track_info['name']}")

class MoodScreen(MDScreen):
    """Main mood selection screen"""
    def __init__(self, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.app_instance = app_instance
        self.name = "mood_screen"
        
        # Main layout
        main_layout = MDBoxLayout(orientation="vertical", spacing="10dp", padding="20dp")
        
        # Title
        title = MDLabel(
            text="🎵 Moodify",
            theme_text_color="Primary",
            font_style="H3",
            size_hint_y=None,
            height="60dp",
            halign="center"
        )
        main_layout.add_widget(title)
        
        # Subtitle
        subtitle = MDLabel(
            text="Choose your mood to get personalized music recommendations",
            theme_text_color="Secondary",
            font_style="Body1",
            size_hint_y=None,
            height="40dp",
            halign="center"
        )
        main_layout.add_widget(subtitle)
        
        # Mood buttons
        moods = {
            'Happy': {'emoji': '😊', 'color': [1, 0.84, 0, 1]},  # Gold
            'Sad': {'emoji': '😢', 'color': [0.27, 0.51, 0.71, 1]},  # Steel Blue
            'Angry': {'emoji': '😠', 'color': [0.86, 0.08, 0.24, 1]},  # Crimson
            'Calm': {'emoji': '😌', 'color': [0.6, 0.98, 0.6, 1]},  # Light Green
            'Energetic': {'emoji': '⚡', 'color': [1, 0.08, 0.58, 1]}  # Deep Pink
        }
        
        button_layout = MDBoxLayout(orientation="vertical", spacing="15dp")
        
        for mood, config in moods.items():
            btn = MoodButton(
                mood=mood,
                emoji=config['emoji'],
                color=config['color'],
                on_press=lambda x, m=mood: self.select_mood(m)
            )
            button_layout.add_widget(btn)
        
        main_layout.add_widget(button_layout)
        self.add_widget(main_layout)
    
    def select_mood(self, mood):
        """Handle mood selection"""
        self.app_instance.selected_mood = mood
        self.app_instance.load_recommendations(mood)

class RecommendationsScreen(MDScreen):
    """Screen for displaying music recommendations"""
    def __init__(self, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.app_instance = app_instance
        self.name = "recommendations_screen"
        
        # Main layout
        main_layout = MDBoxLayout(orientation="vertical")
        
        # Toolbar
        toolbar = MDTopAppBar(
            title="Recommendations",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            right_action_items=[["refresh", lambda x: self.refresh_recommendations()]]
        )
        main_layout.add_widget(toolbar)
        
        # Content area
        self.content_layout = MDBoxLayout(orientation="vertical", padding="10dp")
        
        # Loading indicator
        self.loading_layout = MDBoxLayout(
            orientation="vertical",
            spacing="20dp",
            padding="50dp"
        )
        
        loading_label = MDLabel(
            text="Finding perfect songs for your mood...",
            theme_text_color="Primary",
            font_style="H6",
            halign="center"
        )
        self.loading_layout.add_widget(loading_label)
        
        # Progress bar would go here in a real implementation
        
        # Scroll view for recommendations
        self.scroll_view = ScrollView()
        self.recommendations_layout = MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            size_hint_y=None
        )
        self.recommendations_layout.bind(minimum_height=self.recommendations_layout.setter('height'))
        
        self.scroll_view.add_widget(self.recommendations_layout)
        
        main_layout.add_widget(self.content_layout)
        self.add_widget(main_layout)
    
    def show_loading(self):
        """Show loading screen"""
        self.content_layout.clear_widgets()
        self.content_layout.add_widget(self.loading_layout)
    
    def show_recommendations(self, recommendations):
        """Display recommendations"""
        self.content_layout.clear_widgets()
        
        if not recommendations:
            error_label = MDLabel(
                text="No recommendations found. Please try again.",
                theme_text_color="Error",
                font_style="H6",
                halign="center"
            )
            self.content_layout.add_widget(error_label)
            return
        
        # Clear previous recommendations
        self.recommendations_layout.clear_widgets()
        
        # Add new recommendations
        for track in recommendations:
            card = SongCard(track)
            self.recommendations_layout.add_widget(card)
        
        self.content_layout.add_widget(self.scroll_view)
    
    def go_back(self):
        """Go back to mood selection"""
        self.app_instance.screen_manager.current = "mood_screen"
    
    def refresh_recommendations(self):
        """Refresh recommendations"""
        if hasattr(self.app_instance, 'selected_mood'):
            self.app_instance.load_recommendations(self.app_instance.selected_mood)

class MoodifyApp(MDApp):
    """Main application class"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Moodify"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        self.selected_mood = None
        self.spotify_client = None
        self.mood_classifier = None
    
    def build(self):
        """Build the app interface"""
        # Initialize clients
        self.init_clients()
        
        # Create screen manager
        from kivymd.uix.screenmanager import MDScreenManager
        self.screen_manager = MDScreenManager()
        
        # Add screens
        mood_screen = MoodScreen(self)
        recommendations_screen = RecommendationsScreen(self)
        
        self.screen_manager.add_widget(mood_screen)
        self.screen_manager.add_widget(recommendations_screen)
        
        return self.screen_manager
    
    def init_clients(self):
        """Initialize Spotify client and mood classifier"""
        try:
            self.spotify_client = SpotifyClient()
            print("Spotify client initialized successfully")
        except Exception as e:
            print(f"Failed to initialize Spotify client: {e}")
        
        # Load mood classifier if available
        self.mood_classifier = MoodClassifier()
        if os.path.exists('models/mood_classifier.pkl'):
            self.mood_classifier.load_model()
            print("Mood classifier loaded successfully")
        else:
            print("Mood classifier not found, using default recommendations")
    
    def load_recommendations(self, mood):
        """Load recommendations for selected mood"""
        if not self.spotify_client:
            self.show_error("Spotify client not available")
            return
        
        # Switch to recommendations screen and show loading
        recommendations_screen = self.screen_manager.get_screen("recommendations_screen")
        recommendations_screen.show_loading()
        self.screen_manager.current = "recommendations_screen"
        
        # Load recommendations in background thread
        threading.Thread(
            target=self._load_recommendations_thread,
            args=(mood, recommendations_screen)
        ).start()
    
    def _load_recommendations_thread(self, mood, screen):
        """Load recommendations in background thread"""
        try:
            # Get recommendations
            track_ids = self.spotify_client.get_mood_based_recommendations(mood, limit=20)
            
            recommendations = []
            for track_id in track_ids:
                track_info = self.spotify_client.get_track_info(track_id)
                if track_info:
                    recommendations.append(track_info)
            
            # Update UI on main thread
            Clock.schedule_once(
                lambda dt: screen.show_recommendations(recommendations),
                0
            )
            
        except Exception as e:
            print(f"Error loading recommendations: {e}")
            Clock.schedule_once(
                lambda dt: screen.show_recommendations([]),
                0
            )
    
    def show_error(self, message):
        """Show error popup"""
        popup = Popup(
            title="Error",
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        )
        popup.open()

if __name__ == "__main__":
    MoodifyApp().run()
