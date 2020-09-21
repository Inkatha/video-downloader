import argparse
import json
import asyncio
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = 'AIzaSyDQPItrgJPi9m_3xxwFn-sSVzuGMUo0mVI'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                developerKey=DEVELOPER_KEY)


def youtube_search(options):
    result = search('', options=options)
    search_response = result['search_response']
    nextPageToken = result['nextPageToken']

    while nextPageToken != None:
        print(nextPageToken)
        write_to_files(search_response=search_response, nextPageToken=nextPageToken)
        result = search(nextPageToken=nextPageToken, options=options)
        search_response = result['search_response']
        nextPageToken = result['nextPageToken']


def search(nextPageToken, options):
    search_response = youtube.search().list(
        q=options['q'],
        part='id,snippet',
        maxResults=options['max_results'],
        videoDuration=options['videoDuration'],
        type=options['type'],
        pageToken=nextPageToken
    ).execute()

    nextPageToken = search_response.get('nextPageToken')
    return {'search_response': search_response, 'nextPageToken': nextPageToken}


def write_to_files(search_response, nextPageToken):
    videos = []
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            result = {
                'title': search_result['snippet']['title'],
                'description': search_result['snippet']['description'],
                'url': f"https://www.youtube.com/watch?v={search_result['id']['videoId']}"
            }
            videos.append(result)

    with open('video_results.json') as json_file:
        data = json.load(json_file)
        data["nextPageToken"] = nextPageToken
        data["videos"].extend(videos)
        write_json(data, 'video_results.json')

    with open('log_file.json') as json_file:
        data = json.load(json_file)
        data["logs"].append({
            "token": nextPageToken,
            "dateCreated": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })
        write_json(data, 'log_file.json')


def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
