import time
from instascrape import Reel

def download(link):
    path = f"uploads/reels/{int(time.time())}.mp4"

    try:
        if (link):

            SESSIONID = "18614737527%3ApTLwFoXv5BZohu%3A4"
            headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43",
            "cookie":f'sessionid={SESSIONID};'
            }

            google_reel=Reel(link)
            google_reel.scrape(headers=headers)
            google_reel.download(fp=path)

        else:
            print("Empty field","Please fill out the field")

    except Exception as e:
        print('@@@@@@@@@@@@@@@----> ',e)

    return path
