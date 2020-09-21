from pytube import YouTube
import json


class Download:
    currentVideoFileSize = 0
    fileName = ''

    def run(self):
        videos = self.read_video_result_file()
        for video in videos:
            try:
                yt = YouTube(
                    video['url'], on_progress_callback=self.show_progress_bar)
                self.currentVideoFileSize = yt.streams.first().filesize
                self.fileName = video['title']
                yt.streams.first().download(output_path='./videos')
            except:
                with open('log_file.json') as json_file:
                    data = json.load(json_file)
                    data['logs'].append({
                        'error': f'Invalid cipher provided by YouTube for video {video["title"]}',
                        'url': video['url']
                    })
                    self.write_json(data, 'log_file.json')

    def read_video_result_file(self):
        with open('video_results.json') as json_file:
            data = json.load(json_file)
            return data["videos"]

    def show_progress_bar(self, stream, chunk, bytes_remaining):
        progress = round(
            (1 - bytes_remaining / self.currentVideoFileSize) * 100)
        progress_message = f'{self.fileName} is {progress}% complete...'
        print(progress_message)

    def write_json(self, data, filename):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)