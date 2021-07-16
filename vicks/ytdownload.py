
# youtube_video_url = 'https://youtu.be/GbqGmNsWDaE?list=RDMM'

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip as vix
from pytube import YouTube
import moviepy.editor as mp
import os

# def yt_audio(vid = 'KBtk5FUeJbk'):
#     try:
#         youtube_video_url = 'https://youtu.be/' + vid
#         yt_obj = YouTube(youtube_video_url)
#         yt_obj.title = vid
#
#         audio = yt_obj.streams.filter(only_audio=True).first()
#         # out_file = audio.download(output_path=r"C:\Users\Vicky\Desktop\Vicks Tube\Audio")
#         out_file = audio.download(output_path="uploads/audio/")
#
#         base, ext = os.path.splitext(out_file)
#         new_file = base + '.mp3'
#
#         os.rename(out_file, new_file)
#         print(yt_obj.title + " has been successfully downloaded.")
#
#     except Exception as e:
#         print(e)
#
#     return vid

# ---------------------------------------------------------


def yt_video(vid = 'KBtk5FUeJbk', ts=60, te=600, folder = "uploads/videos/"):
    try:
        youtube_video_url = 'https://youtu.be/' + vid
        yt_obj = YouTube(youtube_video_url)

        # yt_obj.title = ''.join([i for i in yt_obj.title if i.isalpha()])
        yt_obj.title = vid
        filters = yt_obj.streams.filter(progressive=True, file_extension='mp4')

        # filters.get_highest_resolution().download(r"C:\Users\Vicky\Desktop\Vicks Tube\Video")
        filters.get_highest_resolution().download(folder)

        vix(folder+vid+'.mp4', ts, te, targetname=folder+vid+'_trimmed.mp4')
        print(yt_obj.title + ' has Downloaded Successfully')
        os.remove(folder+vid+'.mp4')

    except Exception as e:
        print(vid)
        print(e)

    return vid

# ---------------------------------------------------------

def yt_audio(vid = 'KBtk5FUeJbk', ts=60, te=600):
    try:
        folder = "uploads/audio/"
        yt_video(vid = vid, ts=ts, te=te, folder = folder)

        clip = mp.VideoFileClip(folder+vid+"_trimmed.mp4")
        # clip = clip.subclip(ts, te)

        clip.audio.write_audiofile(folder+vid+"_trimmed.mp3")
        # os.remove(folder+vid+'_trimmed.mp4')

    except Exception as e:
        print(e)

    return vid
