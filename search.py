import argparse
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = 'AIzaSyAPMQGPSVdZVhr1xRvq3AZQEzWI8MaqE0o'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  search_response = youtube.search().list(
    q=options['q'],
    part='id,snippet',
    maxResults=options['max_results'],
    videoDuration=options['videoDuration'],
    type=options['type'],
    pageToken="CGQQAA"
  ).execute()

  nextPageToken = search_response.get('nextPageToken')
  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  while nextPageToken != '':
    search_response = youtube.search().list(
      q=options['q'],
      part='id,snippet',
      maxResults=options['max_results'],
      videoDuration=options['videoDuration'],
      type=options['type'],
      pageToken=nextPageToken
    ).execute()
    nextPageToken = search_response.get('nextPageToken')
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
      data["videoResults"].append(videos)
      write_json(data, 'video_results.json')

    with open('log_file.json') as json_file:
      data = json.load(json_file)
      data["logs"].append({
        "token": nextPageToken,
        "dateCreated": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
      })
      write_json(data, 'log_file.json')

def write_json(data, filename):
    with open(filename,'w') as f: 
        json.dump(data, f, indent=2)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--q', help='Search term', default='Google')
  parser.add_argument('--max-results', help='Max results', default=25)
  args = parser.parse_args()

  try:
    youtube_search(args)
  except(HttpError, e):
    print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))