import time
from instascrape import Reel
# import requests

# https://github.com/csuhan/ReDet/issues/14#issuecomment-914544044

def download(link):
    path = f"uploads/reels/{int(time.time())}.mp4"

    try:
        if (link):

            SESSIONID = "7015147780%3ATmIQHL0SAB86as%3A10"
            headers = {
            # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43",
            "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
            "cookie":f'sessionid={SESSIONID};'
            }

            google_reel=Reel(link)
            google_reel.scrape(headers=headers)
            google_reel.download(fp=path)

            # link = link.split('/')[4]
            # link = f'https://www.instagram.com/reel/{link}/?__a=1'
            # response = requests.get(link)
            #
            # response.raise_for_status()  # raises exception when not a 2xx response
            # if response.status_code != 204:
            #     link = response.json()
            # print(link)

        else:
            print("Empty field","Please fill out the field")

    except Exception as e:
        print('@@@@@@@@@@@@@@@----> ',e)

    return path

# download('https://www.instagram.com/reel/CTjI5hJI-uA/?utm_source=ig_web_copy_link')
