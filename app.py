import streamlit as st
import pandas as pd
import joblib
import base64

# Configure page
st.set_page_config(
    page_title="VIBETUNE",
    page_icon="img.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Function to encode GIF to base64
@st.cache_data
def get_base64_gif(gif_path):
    """Convert GIF to base64 string for embedding in CSS"""
    try:
        with open(gif_path, "rb") as f:
            contents = f.read()
        return base64.b64encode(contents).decode("utf-8")
    except FileNotFoundError:
        st.warning(f"GIF file not found at {gif_path}")
        return None

# Get the base64 encoded GIF
gif_path = "statics/hii.gif "  
gif_base64 = get_base64_gif(gif_path)

# Create the background style with or without GIF
if gif_base64:
    background_style = f"""
    background: url("data:image/gif;base64,{gif_base64}") no-repeat center center fixed;
    background-size: cover;
    """
    overlay_style = """
    /* Dark overlay to ensure text readability */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, 
            rgba(20, 25, 40, 0.7) 0%, 
            rgba(30, 40, 60, 0.6) 25%,
            rgba(15, 20, 35, 0.8) 50%,
            rgba(25, 35, 55, 0.6) 75%,
            rgba(10, 15, 30, 0.7) 100%);
        z-index: -1;
        pointer-events: none;
    }
    """
else:
    # Fallback to gradient background
    background_style = """
    background: linear-gradient(135deg, 
        rgba(20, 25, 40, 1) 0%, 
        rgba(30, 40, 60, 1) 25%,
        rgba(15, 20, 35, 1) 50%,
        rgba(25, 35, 55, 1) 75%,
        rgba(10, 15, 30, 1) 100%);
    """
    overlay_style = ""

# Custom CSS for Liquid Glass Design with GIF Background
st.markdown(f"""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global Styles */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

.stApp {{
    {background_style}
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
    position: relative;
}}

{overlay_style}

/* Hide Streamlit elements */
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
header {{visibility: hidden;}}

/* Title Animation */
.main-title {{
    font-size: 4rem;
    font-weight: 700;
    text-align: center;
    margin: 2rem 0;
    background: linear-gradient(135deg, 
        rgba(255, 255, 255, 0.95) 0%,
        rgba(180, 220, 255, 0.9) 25%,
        rgba(255, 255, 255, 0.95) 50%,
        rgba(200, 230, 255, 0.9) 75%,
        rgba(255, 255, 255, 0.95) 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: titleGlow 3s ease-in-out infinite alternate;
    text-shadow: 0 0 30px rgba(255, 255, 255, 0.3);
    position: relative;
    z-index: 1;
}}

@keyframes titleGlow {{
    0% {{
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.4);
        transform: translateY(0px);
    }}
    100% {{
        text-shadow: 0 0 40px rgba(180, 220, 255, 0.6);
        transform: translateY(-2px);
    }}
}}

/* Glass Container */
.glass-container {{
    background: linear-gradient(135deg, 
        rgba(255, 255, 255, 0.15) 0%,
        rgba(255, 255, 255, 0.08) 100%);
    backdrop-filter: blur(25px);
    -webkit-backdrop-filter: blur(25px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 20px;
    padding: 2rem;
    margin: 1rem;
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.4),
        inset 0 1px 0 rgba(255, 255, 255, 0.3);
    animation: containerFloat 6s ease-in-out infinite;
    position: relative;
    z-index: 1;
}}

@keyframes containerFloat {{
    0%, 100% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-5px); }}
}}

/* Input Fields */
.stSelectbox label, .stTextInput label {{
    color: rgba(255, 255, 255, 0.95) !important;
    font-weight: 500;
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}}

.stSelectbox div[data-baseweb="select"] > div,
.stTextInput input {{
    background: rgba(255, 255, 255, 0.12) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 12px !important;
    color: white !important;
    backdrop-filter: blur(15px);
    transition: all 0.3s ease;
}}

.stSelectbox div[data-baseweb="select"] > div:hover,
.stTextInput input:hover {{
    background: rgba(255, 255, 255, 0.18) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    box-shadow: 0 4px 16px rgba(255, 255, 255, 0.15);
}}

/* Recommendation Button */
.stButton > button {{
    background: linear-gradient(135deg, 
        rgba(0, 0, 0, 0.9) 0%,
        rgba(250, 0, 0, 1) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 15px !important;
    padding: 0.8rem 2rem !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    backdrop-filter: blur(10px) !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
    margin: 1rem 0 !important;
    box-shadow: 0 8px 25px rgba(250, 0, 0, 0.4) !important;
}}

.stButton > button:hover {{
    background: linear-gradient(135deg, 
        rgba(0, 0, 0, 0.9) 0%,
        rgba(250, 0, 0, 1) 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(250, 0, 0, 0.4) !important;
}}

/* Song Cards */
.song-card {{
    background: linear-gradient(135deg, 
        rgba(255, 255, 255, 0.12) 0%,
        rgba(255, 255, 255, 0.06) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 15px;
    padding: 1.5rem;
    margin: 0.5rem;
    transition: all 0.4s ease;
    animation: slideIn 0.6s ease-out;
    position: relative;
    overflow: hidden;
    z-index: 1;
}}

.song-card:hover {{
    transform: translateY(-8px) scale(1.02);
    background: linear-gradient(135deg, 
        rgba(255, 255, 255, 0.18) 0%,
        rgba(255, 255, 255, 0.12) 100%);
    box-shadow: 0 15px 40px rgba(255, 255, 255, 0.15);
}}

.song-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, 
        transparent, 
        rgba(255, 255, 255, 0.15), 
        transparent);
    transition: left 0.6s;
}}

.song-card:hover::before {{
    left: 100%;
}}

@keyframes slideIn {{
    from {{
        opacity: 0;
        transform: translateX(-30px);
    }}
    to {{
        opacity: 1;
        transform: translateX(0);
    }}
}}

.song-title {{
    color: rgba(255, 255, 255, 0.95);
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    text-align: center;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}}

.song-artist {{
    color: rgba(255, 255, 255, 0.8);
    font-size: 0.95rem;
    margin-bottom: 1rem;
    text-align: center;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}}

.music-links {{
    display: flex;
    justify-content: center;
    gap: 0.5rem;
    margin-top: 1rem;
}}

.music-link {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 8px;
    text-decoration: none;
    transition: all 0.3s ease;
    border: 1px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
}}

.music-link:hover {{
    transform: scale(1.1);
    background: rgba(255, 255, 255, 0.25);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}}

/* Loading Animation */
.loading {{
    text-align: center;
    padding: 2rem;
    color: rgba(255, 255, 255, 0.9);
    font-size: 1.1rem;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}}

.loading-dots {{
    display: inline-block;
    animation: loadingDots 1.5s infinite;
}}

@keyframes loadingDots {{
    0%, 20% {{ content: '.'; }}
    40% {{ content: '..'; }}
    60%, 100% {{ content: '...'; }}
}}

/* Error Messages */
.stAlert {{
    background: rgba(255, 100, 100, 0.15) !important;
    border: 1px solid rgba(255, 100, 100, 0.4) !important;
    color: rgba(255, 150, 150, 0.95) !important;
    border-radius: 12px !important;
    backdrop-filter: blur(10px) !important;
}}

/* Success Messages */
.success-message {{
    background: rgba(100, 255, 100, 0.15);
    border: 1px solid rgba(100, 255, 100, 0.4);
    color: rgba(150, 255, 150, 0.95);
    border-radius: 12px;
    padding: 1rem;
    margin: 1rem 0;
    text-align: center;
    backdrop-filter: blur(10px);
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}}

/* Ensure all content stays above background */
.main > div {{
    position: relative;
    z-index: 1;
}}
</style>
""", unsafe_allow_html=True)

# Load model and data
@st.cache_resource
def load_model_and_data():
    try:
        model, le_emotion, le_genre = joblib.load('model\vibetune.pkl')
        df = pd.read_csv('song.csv')
        df.columns = df.columns.str.lower()
        return model, le_emotion, le_genre, df
    except Exception as e:
        st.error(f"Error loading model or data: {str(e)}")
        return None, None, None, None

def create_music_links(song_title, artist):
    """Create search URLs for different music platforms"""
    query = f"{song_title} {artist}"

    youtube_query = query.replace(" ", "+")
    spotify_query = query.replace(" ", "+")
    apple_query = query.replace(" ", "%20")
    
    youtube_url = f"https://www.youtube.com/results?search_query={youtube_query}"
    spotify_url = f"https://open.spotify.com/search/{spotify_query}"
    apple_url = f"https://music.apple.com/search?term={apple_query}"
    
    return youtube_url, spotify_url, apple_url

def recommend_songs(emotion, df, n=10, genre=None):
    """Recommend songs based on emotion and optionally genre"""
    filtered_df = df[df['emotion'].str.lower() == emotion.lower()]
    
    if genre and genre != "Any":
        filtered_df = filtered_df[filtered_df['genre'].str.lower() == genre.lower()]
    
    if filtered_df.empty:
        return []
    
    recommendations = filtered_df.sample(min(n, len(filtered_df)))
    return recommendations.to_dict(orient="records")

# Main app
def main():
    # Load model and data
    model, le_emotion, le_genre, df = load_model_and_data()
    
    if model is None:
        st.error("Failed to load model or data. Please check your files.")
        return
    
    # Title
    st.markdown('<h1 class="main-title">VIBETUNE</h1>', unsafe_allow_html=True)
    
    # Input section
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Get unique emotions and genres
        emotions = sorted(df['emotion'].unique())
        genres = ["Any"] + sorted(df['genre'].unique())
        
        # User inputs
        selected_emotion = st.selectbox(
            "Select Your Current Emotion",
            emotions,
            index=0
        )
        
        selected_genre = st.selectbox(
            "Preferred Genre (Optional)",
            genres,
            index=0
        )
        
        # Generate recommendations button
        if st.button("Get My Vibe", key="recommend_btn"):
            with st.spinner("Finding your perfect vibe..."):
                recommendations = recommend_songs(
                    selected_emotion, 
                    df, 
                    n=10, 
                    genre=selected_genre if selected_genre != "Any" else None
                )
            
            if recommendations:
                st.markdown('<div class="song-card"><div class="song-title">YOUR VIBE!</div></div>', 
                          unsafe_allow_html=True)
                st.session_state.recommendations = recommendations
            else:
                st.error("NO VIBE FOR YOU.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display recommendations in 5x2 grid
    if 'recommendations' in st.session_state:
        st.markdown("---")
        recommendations = st.session_state.recommendations
        
        # Create 5 rows with 2 columns each
        for i in range(0, min(10, len(recommendations)), 2):
            col1, col2 = st.columns(2)
            
            # First song
            with col1:
                song = recommendations[i]
                youtube_url, spotify_url, apple_url = create_music_links(
                    song['song'], song['artist']
                )
                
                st.markdown(f"""
                <div class="song-card">
                    <div class="song-title">{song['song']}</div>
                    <div class="song-artist">by {song['artist']}</div>
                    <div class="music-links">
                        <a href="{youtube_url}" target="_blank" class="music-link">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="#FF0000">
                                <path d="M23.498 6.186a2.997 2.997 0 0 0-2.109-2.109C19.505 3.546 12 3.546 12 3.546s-7.505 0-9.389.531A2.997 2.997 0 0 0 .502 6.186C-.031 8.07-.031 12-.031 12s0 3.93.533 5.814a2.997 2.997 0 0 0 2.109 2.109c1.884.531 9.389.531 9.389.531s7.505 0 9.389-.531a2.997 2.997 0 0 0 2.109-2.109C24.031 15.93 24.031 12 24.031 12s0-3.93-.533-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                            </svg>
                        </a>
                        <a href="{spotify_url}" target="_blank" class="music-link">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="#1DB954">
                                <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.481.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.42 1.56-.299.421-1.02.599-1.559.3z"/>
                            </svg>
                        </a>
                        <a href="{apple_url}" target="_blank" class="music-link">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="#000000">
                                <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/>
                            </svg>
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Second song (if exists)
            if i + 1 < len(recommendations):
                with col2:
                    song = recommendations[i + 1]
                    youtube_url, spotify_url, apple_url = create_music_links(
                        song['song'], song['artist']
                    )
                    
                    st.markdown(f"""
                    <div class="song-card">
                        <div class="song-title">{song['song']}</div>
                        <div class="song-artist">by {song['artist']}</div>
                        <div class="music-links">
                            <a href="{youtube_url}" target="_blank" class="music-link">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="#FF0000">
                                    <path d="M23.498 6.186a2.997 2.997 0 0 0-2.109-2.109C19.505 3.546 12 3.546 12 3.546s-7.505 0-9.389.531A2.997 2.997 0 0 0 .502 6.186C-.031 8.07-.031 12-.031 12s0 3.93.533 5.814a2.997 2.997 0 0 0 2.109 2.109c1.884.531 9.389.531 9.389.531s7.505 0 9.389-.531a2.997 2.997 0 0 0 2.109-2.109C24.031 15.93 24.031 12 24.031 12s0-3.93-.533-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                                </svg>
                            </a>
                            <a href="{spotify_url}" target="_blank" class="music-link">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="#1DB954">
                                    <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.481.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.42 1.56-.299.421-1.02.599-1.559.3z"/>
                            </svg>
                        </a>
                        <a href="{apple_url}" target="_blank" class="music-link">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="#000000">
                                <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/>
                            </svg>
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":

    main()

