
import requests, random

def send_link(bot_message):
  gets = f'https://api.telegram.org/bot{bot_token}/getUpdates'
  req = requests.get(gets)

  show = req.json()
  lst = list(show.values())[1]
  unique = []

  for i in lst:
    bot_chatID = i['message']['chat']['id']
    unique.append(bot_chatID)

  for i in set(unique):
    sets = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={i}&parse_mode=Markdown&text={bot_message}'
    requests.post(sets)

def send_news(news_api):
  source = ['bbc-news', 'cnn', 'the-verge', 'time', 'the-wall-street-journal']
  source = random.choice(source)

  bot_message = f'''
Good morning ☀️
Here is today's news from {source.upper()}

https://imvickykumar999.pythonanywhere.com/

Reply me with any sticker to continue daily.
'''

  send_link(bot_message)
  gets = f'https://newsapi.org/v1/articles?source={source}&sortBy=top&apiKey={news_api}'

  req = requests.get(gets)
  box = req.json()['articles']

  for i in box:
    if i['description'] == None:
      i['description'] = 'Read More'

    bot_message = f'''
➡️ {i['title']}

{i['description']}

{i['url']}
'''
    send_link(bot_message)

if __name__ == '__main__':
    news_api = '*******************************' # https://newsapi.org/account
    bot_token = '*******************************' # https://t.me/BotFather

    try: send_news(news_api)
    except Exception as e: print(e)
