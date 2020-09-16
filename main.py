import search

def main():
    query = {
      'q': 'farrakhan',
      'max_results': '200',
      'videoDuration': 'long',
      'type': 'video'
    }
    search.youtube_search(query)

if __name__ == "__main__":
    main()