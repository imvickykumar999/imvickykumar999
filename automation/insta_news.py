
import requests, random, os, json
from instagrapi import Client
from PIL import ImageDraw
from PIL import ImageFont
from PIL import Image

def fetch_news(news_api):
    source = [
        ('bbc-news', '@bbcnewsindia'), 
        ('cnn', '@cnn'), 
        ('the-verge', '@verge'), 
        ('time', '@time'), 
        ('the-wall-street-journal', '@wsj')
    ]
    source = random.choice(source)
    gets = f'https://newsapi.org/v1/articles?source={source[0]}&sortBy=top&apiKey={news_api}'

    req = requests.get(gets)
    box = req.json()['articles']
    return box, source

def make_square(im, j, min_size=256, fill_color=(255,255,255,0)):
    img = Image.open(im)
    x, y = img.size

    size = max(min_size, x, y)
    new_im = Image.new('RGB', (size, size), fill_color)

    new_im = new_im.convert("RGB")
    new_im.paste(img, (int((size - x) / 2), int((size - y) / 2)))

    I1 = ImageDraw.Draw(new_im)
    myFont = ImageFont.truetype("arial.ttf", 30)

    I1.text((15, 15), f'[ {j+1} ]', font=myFont, fill=(0, 0, 0))
    new_im.save(im)

def upload_news(user, passwd):
    box, source = fetch_news(news_api)
    cap = []

    for j, i in enumerate(box):
        tweet = f'({j+1}). {i["title"]}\n'
        cap.append(tweet)
        img = i['urlToImage']
        r = requests.get(img, allow_redirects=True)

        path = f'images/{j}.jpg'
        open(path, 'wb').write(r.content)
        make_square(path, j)

    bot = Client()
    bot.login(username = user, password = passwd)
    album_path = ['images/'+i for i in os.listdir('images')]

    url = 'https://imvickykumar999.pythonanywhere.com/news'
    text = f'{source[1]} \nRead More:\n {url}/{source[0]}\n\n'

    post_url = bot.album_upload(
        album_path,
        caption = text + '\n'.join(cap)
    )

    bot.photo_upload_to_story(album_path[0])
    media_id = json.loads(post_url.json())['id']

    comment = bot.media_comment(
        media_id, 
        f"MediaID = (PostID_UserID) : {media_id}"
    )
    bot.comment_like(comment.pk)

    reply = bot.media_comment(
        media_id, 
        f"Comment ID : {comment.pk}", 
        replied_to_comment_id=comment.pk
    )
    bot.comment_like(reply.pk)
    print(f'\nUploaded ...\n https://www.instagram.com/{user}/', source)

if __name__ == '__main__':
    try: os.mkdir('images')
    except: pass

    news_api = '*******************************' # https://newsapi.org/account
    insta_user = '*******************************'
    insta_passwd = '*******************************'

    try: upload_news(insta_user, insta_passwd)
    except Exception as e: print(e)
