import requests
from typing import List, Dict
import re

# YouTube API (free tier, get key from Google Cloud)
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"  # Replace with actual key

# Curated free resource database (no API needed for demo)
FREE_RESOURCES = {
    "python_basics": {
        "youtube": [
            {"title": "Python for Beginners (Full Course)", "url": "https://youtu.be/_uQrJ0TkZlc", "duration": 60},
            {"title": "Python in 1 Hour", "url": "https://youtu.be/kqtD5dpn9C8", "duration": 60}
        ],
        "nptel": [
            {"title": "NPTEL: Python Programming", "url": "https://nptel.ac.in/courses/106106182"}
        ],
        "docs": [
            {"title": "Official Python Tutorial", "url": "https://docs.python.org/3/tutorial/"}
        ],
        "github": [
            {"title": "Awesome Python Learning", "url": "https://github.com/trending/python?since=monthly"}
        ]
    },
    "functions": {
        "youtube": [
            {"title": "Python Functions Tutorial", "url": "https://youtu.be/9Os0o3wzS_I", "duration": 15}
        ],
        "docs": [
            {"title": "Python Functions Docs", "url": "https://docs.python.org/3/tutorial/controlflow.html#defining-functions"}
        ]
    },
    "loops": {
        "youtube": [
            {"title": "For Loops Explained", "url": "https://youtu.be/94UHCEmprCY", "duration": 12}
        ],
        "github": [
            {"title": "Loop Practice Problems", "url": "https://github.com/learning-zone/python-basics/blob/master/loops.md"}
        ]
    },
    "lists": {
        "youtube": [
            {"title": "Python Lists Tutorial", "url": "https://youtu.be/W8KRzm-aUcc", "duration": 20}
        ]
    },
    "dictionaries": {
        "youtube": [
            {"title": "Dictionaries in Python", "url": "https://youtu.be/daefaLgNkw0", "duration": 15}
        ]
    },
    "conditionals": {
        "youtube": [
            {"title": "If-Else Statements", "url": "https://youtu.be/Z1Yd7upQsXY", "duration": 10}
        ]
    }
}

def get_resources_for_topic(topic: str, resource_type: str = "youtube") -> List[Dict]:
    """Fetch free resources for a specific topic"""
    
    if topic in FREE_RESOURCES:
        if resource_type in FREE_RESOURCES[topic]:
            return FREE_RESOURCES[topic][resource_type]
    
    # Fallback to YouTube search (if API key is set)
    if YOUTUBE_API_KEY != "YOUR_YOUTUBE_API_KEY" and resource_type == "youtube":
        try:
            url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={topic}+programming+tutorial&maxResults=3&key={YOUTUBE_API_KEY}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return [{
                    "title": item["snippet"]["title"],
                    "url": f"https://youtu.be/{item['id']['videoId']}",
                    "duration": "unknown"
                } for item in data.get("items", [])]
        except:
            pass
    
    # Default fallback
    return [{
        "title": f"Learn {topic} - Search on YouTube",
        "url": f"https://www.youtube.com/results?search_query={topic}+programming+tutorial",
        "duration": "search"
    }]