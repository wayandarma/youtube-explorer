from googleapiclient.discovery import build
from typing import Dict, List
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

class YouTubeExplorer:
    def __init__(self):
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
    
    def get_channel_id(self, channel_name: str) -> str:
        """Get channel ID from channel name"""
        request = self.youtube.search().list(
            q=channel_name,
            type='channel',
            part='id',
            maxResults=1
        )
        response = request.execute()
        
        if response['items']:
            return response['items'][0]['id']['channelId']
        return None

    def get_channel_videos(self, channel_id: str, max_results: int = 50) -> List[Dict]:
        """Get videos from channel ID"""
        videos = []
        
        request = self.youtube.search().list(
            channelId=channel_id,
            part='id,snippet',
            order='date',
            maxResults=max_results,
            type='video'
        )
        response = request.execute()
        
        for item in response['items']:
            video_id = item['id']['videoId']
            video_stats = self.get_video_stats(video_id)
            
            video_data = {
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'views': video_stats.get('viewCount', 0),
                'likes': video_stats.get('likeCount', 0),
                'comments': video_stats.get('commentCount', 0),
                'link': f'https://youtube.com/watch?v={video_id}',
                'thumbnail': item['snippet']['thumbnails']['high']['url']
            }
            videos.append(video_data)
            
        return videos

    def get_video_stats(self, video_id: str) -> Dict:
        """Get video statistics"""
        request = self.youtube.videos().list(
            part='statistics',
            id=video_id
        )
        response = request.execute()
        
        if response['items']:
            return response['items'][0]['statistics']
        return {}

    def save_to_csv(self, videos: List[Dict], filename: str = 'youtube_videos.csv'):
        """Save videos data to CSV file"""
        df = pd.DataFrame(videos)
        df.to_csv(filename, index=False)
        return filename

    def search_videos(self, query: str, max_results: int = 50) -> List[Dict]:
        """Search videos by query"""
        videos = []
        
        request = self.youtube.search().list(
            q=query,
            part='id,snippet',
            order='relevance',
            maxResults=max_results,
            type='video'
        )
        response = request.execute()
        
        for item in response['items']:
            video_id = item['id']['videoId']
            video_stats = self.get_video_stats(video_id)
            
            video_data = {
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'channel': item['snippet']['channelTitle'],
                'views': int(video_stats.get('viewCount', 0)),
                'likes': int(video_stats.get('likeCount', 0)),
                'comments': int(video_stats.get('commentCount', 0)),
                'link': f'https://youtube.com/watch?v={video_id}',
                'thumbnail': item['snippet']['thumbnails']['high']['url']
            }
            videos.append(video_data)
            
        return videos

    def search_videos(self, query: str, max_results: int = 50) -> List[Dict]:
        """Search videos by query"""
        videos = []
        
        request = self.youtube.search().list(
            q=query,
            part='id,snippet',
            order='relevance',
            maxResults=max_results,
            type='video'
        )
        response = request.execute()
        
        for item in response['items']:
            video_id = item['id']['videoId']
            video_stats = self.get_video_stats(video_id)
            
            video_data = {
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'channel': item['snippet']['channelTitle'],
                'views': int(video_stats.get('viewCount', 0)),
                'likes': int(video_stats.get('likeCount', 0)),
                'comments': int(video_stats.get('commentCount', 0)),
                'link': f'https://youtube.com/watch?v={video_id}',
                'thumbnail': item['snippet']['thumbnails']['high']['url']
            }
            videos.append(video_data)
            
        return videos 