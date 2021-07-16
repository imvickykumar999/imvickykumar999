from pytube import YouTube

youtube_video_url = 'https://www.youtube.com/watch?v=DkU9WFj8sYo'

try:
    yt_obj = YouTube(youtube_video_url)

    filters = yt_obj.streams.filter(progressive=True, file_extension='mp4')

    # download the highest quality video
    filters.get_highest_resolution().download()
    print('Video Downloaded Successfully')
except Exception as e:
    print(e)

# ---------------------------------------------

from pytube import YouTube

youtube_video_url = 'https://www.youtube.com/watch?v=DkU9WFj8sYo'

try:
    yt_obj = YouTube(youtube_video_url)

    yt_obj.streams.get_audio_only().download(output_path='/Users/pankaj/temp', filename='audio')
    print('YouTube video audio downloaded successfully')
except Exception as e:
    print(e)

# ------------------------------------------

rom pytube import Playlist

try:
    playlist = Playlist('https://www.youtube.com/playlist?list=PLcow8_btriE11hzMbT3-B1sBg4YIc-9g_')

    playlist.download_all(download_path='/Users/pankaj/temp')

except Exception as e:
    print(e)
