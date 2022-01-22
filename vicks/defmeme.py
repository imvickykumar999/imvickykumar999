def memers(idno = 2, text0 = 'C++', text1 = 'Python'):
    import requests

    username = 'imvickykumar999'
    password = 'Hellovix999@'

    data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
    images = [{'name':image['name'],'url':image['url'],'id':image['id'],
               'box_count':image['box_count']} for image in data]

    URL = 'https://api.imgflip.com/caption_image'
    params = {
        'username': username,
        'password': password,
        'template_id':images[idno-1]['id'],
        'text0':text0,
        'text1':text1,
    }
    response = requests.request('POST', URL, params=params).json()
    print('#####------> ', response)
    return response['data']['url'], images


def pilmeme(text0 = '''
    Pay
    for
    Movie
    ''', text1 = '''
    Use
    Telegram
    '''):

    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont

    img = Image.open('drake.jpg')
    w,h = img.size

    I1 = I2 = ImageDraw.Draw(img)
    myFont = ImageFont.truetype('PlayfairDisplaySC-Bold.otf', 65)

    I1.text((100 + w/2, h/4 - 200), text0,
            font=myFont, fill =(0, 0, 0))

    I2.text((100 + w/2, h*3/4 - 200), text1,
            font=myFont, fill =(0, 0, 0))

    # img.show()
    img.save("news.png")
    return ["news.png"]
