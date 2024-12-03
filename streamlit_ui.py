import streamlit as st
import pandas as pd
from youtubeSearch import YouTubeExplorer
from ai_suggestions import QuerySuggestionEngine

def get_query_suggestions(query: str = "") -> None:
    """Handle query suggestions UI logic"""
    suggestion_engine = QuerySuggestionEngine()
    
    col1, col2, col3 = st.columns(3)
    
    # First column - Random Query
    with col1:
        if st.button("Get Random Query Idea"):
            with st.spinner("Generating random query idea..."):
                suggestion = suggestion_engine.get_random_query()
                st.session_state.search_query = suggestion.strip('"\'')
                st.rerun()
    
    # Second column - Clear Query
    with col2:
        if st.button("Clear Query"):
            st.session_state.search_query = ""
            st.rerun()
    
    # Third column - Related Queries
    with col3:
        # Store the "Get Related Query Ideas" button state in session state
        if 'show_related_queries' not in st.session_state:
            st.session_state.show_related_queries = False
            
        if not query:
            st.button("Get Related Query Ideas", disabled=True)
        else:
            # Toggle the show_related_queries state
            if st.button("Get Related Query Ideas", key="related_query_btn"):
                st.session_state.show_related_queries = True
                st.session_state.related_suggestions = suggestion_engine.get_related_queries(query)
                st.rerun()
    
    # Display related queries if they exist in session state
    if st.session_state.get('show_related_queries', False):
        st.write("Related Query Ideas:")
        suggestions = st.session_state.get('related_suggestions', [])
        
        # Create columns for suggestions
        suggestion_cols = st.columns(len(suggestions))
        
        # Display each suggestion in its own column
        for idx, (suggestion, col) in enumerate(zip(suggestions, suggestion_cols)):
            clean_suggestion = suggestion.strip('"\'')
            with col:
                if st.button(f"Use: {clean_suggestion}", key=f"use_suggestion_{idx}"):
                    st.session_state.search_query = clean_suggestion
                    st.session_state.show_related_queries = False  # Hide suggestions after selection
                    st.rerun()

def main():
    st.title("YouTube Channel Video Explorer")
    st.write("Explore YouTube channels without algorithmic bias")
    
    # Initialize session state for search query
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ""
    
    # Input section
    max_results = st.slider("Maximum number of videos to fetch", 1, 50, 10)
    
    # Use session state for the search query
    search_query = st.text_input(
        "Enter Search Query",
        value=st.session_state.search_query,
        key="search_input"
    )
    
    # Update session state when input changes
    st.session_state.search_query = search_query
    
    # Add Query Ideas feature
    st.markdown("---")
    st.subheader("Need inspiration?")
    get_query_suggestions(search_query)
    st.markdown("---")

    if st.button("Fetch Videos"):
        explorer = YouTubeExplorer()
        
        with st.spinner("Fetching data..."):
            if not search_query:
                st.error("Please enter a search query or get a suggestion!")
                return
            videos = explorer.search_videos(search_query, max_results)
            
            if not videos:
                st.warning("No videos found!")
                return
                
            df = pd.DataFrame(videos)
            
            # Display data
            st.subheader("Videos")
            st.dataframe(df)
            
            # Display statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Views", df['views'].sum())
            with col2:
                st.metric("Total Likes", df['likes'].sum())
            with col3:
                st.metric("Total Comments", df['comments'].sum())
            
            # Download button for CSV
            st.download_button(
                "Download CSV",
                df.to_csv(index=False).encode('utf-8'),
                "youtube_videos.csv",
                "text/csv",
                key='download-csv'
            )
            
            # Display thumbnails
            st.subheader("Video Thumbnails")
            for idx, video in enumerate(videos):
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(video['thumbnail'])
                with col2:
                    st.write(f"**{video['title']}**")
                    st.write(f"Channel: {video.get('channel', 'Unknown')}")
                    st.write(f"Views: {video['views']} | Likes: {video['likes']} | Comments: {video['comments']}")
                    st.markdown(f"[Watch Video]({video['link']})")

if __name__ == "__main__":
    main()