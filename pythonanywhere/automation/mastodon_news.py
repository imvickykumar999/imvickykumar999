
import requests, random, json

news_api = '*******************************' # https://newsapi.org/account
access_token = '*******************************' # https://mastodon.social/settings/applications

source = ['bbc-news', 'cnn', 'the-verge', 'time', 'the-wall-street-journal']
source = random.choice(source)
gets = f'https://newsapi.org/v1/articles?source={source}&sortBy=top&apiKey={news_api}'

req = requests.get(gets)
box = req.json()['articles']

for i in box:
    if i['description'] == None:
        i['description'] = 'Read More'

    tweet = f'''➡️ {i['title']}

    {i['urlToImage']}

    {i['description']}

    {i['url']}
'''

    url = 'https://mastodon.social/api/v1/statuses'
    auth = {'Authorization': f'Bearer {access_token}'}

    params = {'status': tweet}
    r = requests.post(url, data=params, headers=auth)

    res = json.loads(r.text)
    print('\n', res['url'])
