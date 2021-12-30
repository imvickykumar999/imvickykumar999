def memers(idno = 2, text0 = 'C++', text1 = 'Python'):
    import requests
    import urllib
    # import pandas as pd

    username = 'imvickykumar999'
    password = 'Hellovix999@'
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'

    data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
    images = [{'name':image['name'],'url':image['url'],'id':image['id'],
               'box_count':image['box_count']} for image in data]

    # df = pd.DataFrame(images)
    # df.index += 1
    # df[['name', 'box_count', 'url']].to_csv('memes.csv', index = False)

#     idno = 2
#     text0 = 'C++'
#     text1 = 'Python'

    URL = 'https://api.imgflip.com/caption_image'
    params = {
        'username': username,
        'password': password,
        'template_id':images[idno-1]['id'],
        'text0':text0,
        'text1':text1,
    }
    response = requests.request('POST', URL, params=params).json()
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', userAgent)
    filename, headers = opener.retrieve(response['data']['url'],
                                        '../uploads/vixmemes/' + images[idno-1]['name']+'.jpg')
    return filename, headers
