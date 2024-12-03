import streamlit as st
import streamlit.components.v1 as components

def get_youtube_video_id(url: str) -> str:
    """Extract video ID from YouTube URL"""
    if 'youtube.com/watch?v=' in url:
        return url.split('watch?v=')[1].split('&')[0]
    elif 'youtu.be/' in url:
        return url.split('youtu.be/')[1].split('?')[0]
    return url

def init_player_styles():
    """Initialize player styles once"""
    st.markdown("""
        <style>
        .video-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.9);
            z-index: 9999;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .video-content {
            width: 90%;
            max-width: 800px;
            background: #1E1E1E;
            border-radius: 8px;
            padding: 20px;
        }
        .video-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .video-title {
            color: white;
            margin: 0;
            font-size: 1.2em;
        }
        .close-button {
            background: none;
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
            padding: 0;
        }
        .video-wrapper {
            position: relative;
            padding-bottom: 56.25%;
            height: 0;
            overflow: hidden;
        }
        .video-wrapper iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
        }
        </style>
    """, unsafe_allow_html=True)

def create_video_player(video_id: str, video_title: str):
    """Create an embedded video player"""
    html_content = f"""
        <div class="video-modal" id="videoModal">
            <div class="video-content">
                <div class="video-header">
                    <h3 class="video-title">{video_title}</h3>
                    <button class="close-button" onclick="closeVideoModal()">×</button>
                </div>
                <div class="video-wrapper">
                    <iframe
                        src="https://www.youtube.com/embed/{video_id}?autoplay=1&rel=0"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowfullscreen
                    ></iframe>
                </div>
            </div>
        </div>
        <script>
            function closeVideoModal() {{
                document.getElementById('videoModal').remove();
                window.parent.postMessage({{type: 'closeVideo'}}, '*');
            }}
            
            // Handle ESC key
            document.addEventListener('keydown', function(event) {{
                if (event.key === 'Escape') {{
                    closeVideoModal();
                }}
            }});
            
            // Handle click outside modal
            document.querySelector('.video-modal').addEventListener('click', function(event) {{
                if (event.target.classList.contains('video-modal')) {{
                    closeVideoModal();
                }}
            }});
        </script>
    """
    # Use a larger height to ensure the modal is fully visible
    components.html(html_content, height=1000, scrolling=False)

def create_video_button(video_title: str, video_url: str, key: str):
    """Create a button that opens the video player"""
    if st.button("Play Video", key=key, use_container_width=True):
        video_id = get_youtube_video_id(video_url)
        st.session_state.current_video = {
            'id': video_id,
            'title': video_title
        }
        st.experimental_rerun()