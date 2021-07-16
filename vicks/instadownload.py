import requests, os
import urllib.request
import datetime, json

now = datetime.datetime.now()

def save(image_url = 'https://instagram.fjai3-1.fna.fbcdn.net/v/t51.2885-19/s320x320/82888920_1296419967225198_347951591459913728_n.jpg?_nc_ht=instagram.fjai3-1.fna.fbcdn.net&_nc_ohc=wmUoiJcFkwAAX_jOXsJ&tp=1&oh=9a7f00defe2a53e5d8a1ca83aed0a4cb&oe=5FF96D7C',
        save_name = 'downloaded.jpg'):
    urllib.request.urlretrieve(image_url, save_name)

def download(username = 'yashrajmukhate'):
    try:
        os.system(f'mkdir post\{username}')
    except:
        pass
    link = f'https://www.instagram.com/{username}/?__a=1'

    dinsta = requests.get(link).json()
    post = dinsta['graphql']['user']['edge_owner_to_timeline_media']

    urllib.request.urlretrieve(dinsta['graphql']['user']['profile_pic_url_hd'],
                                f'DP_{username}.jpg')

    for i in range(len(post['edges'])):
        if not post['edges'][i]['node']['is_video']:
            url = post['edges'][i]['node']['display_url']
            ext = 'jpg'
        else:
            url = post['edges'][i]['node']['video_url']
            ext = 'mp4'
        loc = f'post/{username}/{now.strftime("%Y%m%d%H%M%S")}_{i+1}.{ext}'
        save(url,loc)

download()
