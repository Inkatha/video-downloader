import search
import download

def main():
  downloader = download.Download()
  downloader.run()
  
def query():
  query = {
    'q': 'Honorable Minister Louis Farrakhan',
    'max_results': '200',
    'videoDuration': 'long',
    'type': 'video'
  }
  search.youtube_search(query)

if __name__ == "__main__":
    main()