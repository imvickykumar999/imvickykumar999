
# https://www.pythonanywhere.com/user/imvickykumar999/tasks_tab/
# https://api.telegram.org/bot6057376731:AAEARe5XwGAt_-h8p7nBd4FunjU1o2WXaz0/getUpdates

# https://newsapi.org/v2/top-headlines/sources?apiKey=e1b57251b1b94ed894f3c60d25551eb2
# https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=5f69434d32434ea8bdb16b347f71cca2

import requests, random

def send_link(bot_message):
  # bot_token = '6057376731:AAEARe5XwGAt_-h8p7nBd4FunjU1o2WXaz0' # Production API

  bot_token = '6297291074:AAFzpuG7i3GNqUgx9Wj5JNxHF6WF_TCufhk' # Test API
  # https://t.me/BotFather

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

def send_news(bot_token):
  # https://newsapi.org/account

  source = ['bbc-news', 'cnn', 'the-verge', 'time', 'the-wall-street-journal']
  source = random.choice(source)
  print(source)

  bot_message = f'''
Good morning ☀️
Here is today's news from {source.upper()}

https://imvickykumar999.pythonanywhere.com/

Reply me with any sticker to continue daily.
'''

  send_link(bot_message)
  gets = f'https://newsapi.org/v1/articles?source={source}&sortBy=top&apiKey={bot_token}'

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

try:
  print('1st')
  send_news('efeaccf474364acfb573910a77456493')
except:
  try:
    print('2nd')
    send_news('e1b57251b1b94ed894f3c60d25551eb2')
  except:
    try:
      print('3rd')
      send_news('5f69434d32434ea8bdb16b347f71cca2')
    except:
      print('4th')
      send_news('87623b8db3254e8698e239abc51a9c10')
