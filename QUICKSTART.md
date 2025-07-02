# Moodify Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Setup Spotify Developer Account
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Note down your `Client ID` and `Client Secret`

### Step 2: Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add your Spotify credentials
nano .env
```

### Step 3: Install Dependencies
```bash
# Run the automated setup
python setup.py

# Or manually install
pip install -r requirements.txt
```

### Step 4: Collect Data & Train Model
```bash
# Collect training data (takes 10-15 minutes)
python data_collector.py

# Train the ML model (takes 2-3 minutes)
python train_model.py
```

### Step 5: Launch the App
```bash
# Web version (recommended for testing)
streamlit run streamlit_app.py

# Mobile version (requires additional setup)
python kivy_app.py
```

## 📱 Building for Android

### Prerequisites
```bash
# Install Buildozer
pip install buildozer

# Install Android SDK and NDK (follow Buildozer docs)
```

### Build APK
```bash
# Initialize buildozer (first time only)
buildozer init

# Build debug APK
buildozer android debug

# Build release APK
buildozer android release
```

## 🎯 Testing the App

### Web App Features to Test:
- [ ] Mood selection buttons work
- [ ] Recommendations load for each mood
- [ ] Song previews play (if available)
- [ ] Favorites system works
- [ ] Analytics charts display

### Mobile App Features to Test:
- [ ] App launches without crashes
- [ ] Mood selection screen displays
- [ ] Recommendations screen loads
- [ ] Song cards display properly
- [ ] Navigation works smoothly

## 🔧 Troubleshooting

### Common Issues:

**"Spotify credentials not found"**
- Check your .env file exists and has correct credentials
- Ensure no extra spaces in the credentials

**"Dataset not found"**
- Run `python data_collector.py` first
- Check if data/mood_music_dataset.csv exists

**"Model not found"**
- Run `python train_model.py` after collecting data
- Check if models/ directory has .pkl files

**Kivy app crashes**
- Install KivyMD: `pip install kivymd`
- Check Python version (3.8+ required)

### Getting Help:
- Check the main README.md for detailed documentation
- Review error messages in the console
- Ensure all dependencies are installed correctly

## 🎵 Enjoy Your Personalized Music Experience!

Once everything is set up, you'll have a fully functional emotion-based playlist generator that learns from your music preferences and provides personalized recommendations based on your current mood.
