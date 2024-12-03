# YouTube Channel Video Explorer

#### Last Updated: 2024-12-03

Created by [@darmacode](https://github.com/darmacode) with ❤️

## Prerequisites

Before running this application, make sure you have:

1. Python 3.8 or higher installed
2. A Google Cloud Platform account with YouTube Data API v3 enabled
3. An OpenAI API key for the query suggestion feature
4. Git installed (for cloning the repository)

## Installation Instructions

1. Clone the repository:

```bash
git clone https://github.com/darmacode/youtube-explorer.git
cd youtube-explorer
```

2. Create and activate a virtual environment (recommended):

```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install required packages:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add your API keys:

```env
YOUTUBE_API_KEY=your_youtube_api_key_here
OPEN_AI_API_KEY=your_openai_api_key_here
```

## Running the Application

1. Make sure your virtual environment is activated
2. Run the Streamlit app:

```bash
streamlit run streamlit_ui.py
```

3. Open your browser and navigate to `http://localhost:8501`

## Programming rules :

1. Use Pandas to handle the data to CSV file.
2. The logic should be on seperate file ( youtubeSearch.py )
3. The UI should be on seperate file ( streamlit_ui.py )

## CSV file include the following columns:

1. Video Title
2. Video Description
3. Video Views
4. Video Likes
5. Video Comments
6. Video Link
7. Video tumbnail

## UI Rules :

1. Use Pandas to handle the data to CSV file.
2. Use Streamlit to display the data to web app ( in seperate file )

## Overview

This project provides a streamlined way to explore and discover YouTube channel content without algorithmic bias. It features:

- Streamlit-powered data visualization, and a simple UI
- Video ranking system based on views and likes
- CSV data export functionality

## Motivation

The primary goal of this project is to enhance understanding of the YouTube API while addressing a specific challenge: discovering authentic, inspiring content without the influence of personalized algorithms.

## Troubleshooting

Common issues and solutions:

1. API Key Issues:

   - Ensure your YouTube API key has the YouTube Data API v3 enabled
   - Check your daily quota limits
   - Verify the API keys are correctly set in the `.env` file

2. Installation Issues:

   - Make sure you're using Python 3.8+
   - Try upgrading pip: `pip install --upgrade pip`
   - If you encounter package conflicts, try creating a fresh virtual environment

3. Runtime Issues:
   - Check your internet connection
   - Verify that all required packages are installed
   - Ensure you're running the application from the project root directory

## Contact

I welcome collaboration and feature suggestions! Feel free to reach out:

- 📧 Email: wayandarma377@gmail.com
- 🐙 GitHub: [@darmacode](https://github.com/darmacode)
