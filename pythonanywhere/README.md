># `News on Instagram`
>
>![image](https://github.com/imvickykumar999/imvickykumar999/assets/50515418/8b7a453b-3ff6-4813-ba5e-785fdc23923e)

    https://www.instagram.com/p/C3fiYYKpK6v/?img_index=7

<br>

```python
from instagrapi import Client
from PIL import ImageDraw
from PIL import ImageFont
from PIL import Image
import requests, os

def fetch_news(news_api):
    source = ('the-verge', '@verge')
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
    try:
        news_api = 'efeaccf4743******73910a77456493'
        box, source = fetch_news(news_api)

    except Exception as e:
        print(e)
        news_api = '87623b8db32******8e239abc51a9c10'
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

    bot.album_upload(
        album_path,
        caption = text + '\n'.join(cap)
    )

    bot.photo_upload_to_story(album_path[0])
    print(f'\nUploaded ...\n\n https://www.instagram.com/{user}/', source)

if __name__ == '__main__':
    try: os.mkdir('images')
    except: pass

    try: upload_news('vixbot2023', '******')
    except Exception as e: print(e)
```
