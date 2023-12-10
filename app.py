
from flask import (Flask, 
    render_template, 
    request
)

import requests, random
app = Flask(__name__)

def get_news(source, api_key='*******************************'):
    try:
        bot_token = '*******************************'
        gets = f'https://newsapi.org/v1/articles?source={source}&sortBy=top&apiKey={bot_token}'
        
        req = requests.get(gets) 
        box = req.json()['articles']

    except:
        try:
            bot_token = '*******************************'
            gets = f'https://newsapi.org/v1/articles?source={source}&sortBy=top&apiKey={bot_token}'
            
            req = requests.get(gets) 
            box = req.json()['articles']

        except:
            bot_token = '*******************************'
            gets = f'https://newsapi.org/v1/articles?source={source}&sortBy=top&apiKey={api_key}'
            
            req = requests.get(gets) 
            box = req.json()['articles']

    ha,ia,ba,la = [],[],[],[]

    for i in range(len(box)):
        h = box[i]['title']
        m = box[i]['urlToImage']
        b = box[i]['description']

        try: l = box[i]['url']
        except: l = 'link not found'

        ha.append(h)
        ia.append(m)
        ba.append(b)
        la.append(l)

    return ha, ia, ba, la

@app.route('/news/<source>')
def one_news(source):
    try:
        ha, ia, ba, la = get_news(source)
        return render_template('news.html', 
                                ha=ha, 
                                ia=ia, 
                                ba=ba, 
                                la=la,
                                len = len(ha))
    except:
        return render_template('home.html', api_key=False)

@app.route('/home', methods=['POST', 'GET'])
def home():
    try:
        if request.method == 'POST':
            api_key = request.form['api_key']
            source = ['bbc-news', 'cnn', 'the-verge', 'time', 'the-wall-street-journal']
            source = random.choice(source)

            ha, ia, ba, la = get_news(source, api_key)
            return render_template('news.html', 
                                    ha=ha, 
                                    ia=ia, 
                                    ba=ba, 
                                    la=la,
                                    len = len(ha))
        else:
            return render_template('home.html', api_key=True)
    except: return render_template('404.html')

@app.route('/')
def news():
    source = ['bbc-news', 'cnn', 'the-verge', 'time', 'the-wall-street-journal']
    source = random.choice(source)

    try:
        ha, ia, ba, la = get_news(source)
        return render_template('news.html', 
                                ha=ha, 
                                ia=ia, 
                                ba=ba, 
                                la=la,
                                len = len(ha))
    except:
        return render_template('home.html', api_key=False)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(
        host="0.0.0.0", 
        debug=True
    )
