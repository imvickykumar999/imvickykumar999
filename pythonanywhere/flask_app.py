
from flask import (Flask,
    render_template,
    request, redirect,
    url_for, flash,
    session,
    send_from_directory
)

from functools import wraps
import secrets
import gspread
import sqlite3 as sql
import requests, random
import datetime

app = Flask(__name__)
secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key

def good_day():
    currentTime = datetime.datetime.now() + datetime.timedelta(hours=6)

    if currentTime.hour < 12:
        return 'Good morning'
    elif 12 <= currentTime.hour < 18:
        return 'Good afternoon'
    else:
        return 'Good evening'


def get_news(source, api_key='87623b8db3254e8698e239abc51a9c10'):
    try:
        gets = f'https://newsapi.org/v1/articles?source={source}&sortBy=top&apiKey={api_key}'
        req = requests.get(gets)
        box = req.json()['articles']

    except:
        gets = f'https://newsapi.org/v1/articles?source={source}&sortBy=top&apiKey=5f69434d32434ea8bdb16b347f71cca2'
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

def is_logged_in(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash('Unauthorized, Please Login','danger')
			return redirect(url_for('login', next=request.url))
	return wrap

@app.route('/news/<source>')
@is_logged_in
def one_news(source):
    try:
        ha, ia, ba, la = get_news(source)
        return render_template('news.html',
                                good=good_day(),
                                ha=ha,
                                ia=ia,
                                ba=ba,
                                la=la,
                                len = len(ha))
    except:
        return render_template('index.html', api_key=False)

@app.route('/templates/assets/<path:path>')
def send_report(path):
    return send_from_directory('./templates/assets/', path)

@app.route('/home', methods=['POST', 'GET'])
def home():
    try:
        if request.method == 'POST':
            api_key = request.form['api_key']
            source = ['bbc-news', 'cnn', 'the-verge', 'time', 'the-wall-street-journal']
            source = random.choice(source)

            ha, ia, ba, la = get_news(source, api_key)
            return render_template('news.html',
                                    good=good_day(),
                                    ha=ha,
                                    ia=ia,
                                    ba=ba,
                                    la=la,
                                    len = len(ha))
        else:
            return render_template('index.html', api_key=True)
    except: return render_template('404.html')

@app.route('/')
def news():
    source = ['bbc-news', 'cnn', 'the-verge', 'time', 'the-wall-street-journal']
    source = random.choice(source)

    try:
        ha, ia, ba, la = get_news(source)
        return render_template('news.html',
                                good=good_day(),
                                ha=ha,
                                ia=ia,
                                ba=ba,
                                la=la,
                                len = len(ha))
    except:
        return render_template('index.html', api_key=False)

@app.route('/login',methods=['POST','GET'])
def login():
    con=sql.connect("pythonanywhere/db_sample.db")

    if request.method=='POST':
        email=request.form["email"]
        pwd=request.form["upass"]
        next_url = request.form.get("next")

        session['email']=email
        row_data = [email]

        spreadsheet_id = '1akZpxtRhFIm97X9ZIdlAm10nfs0_drWTo40rVvkI6zs'
        worksheet_name = 'Sheet1'
        unique_col_index = 0

        gc = gspread.service_account(filename='pythonanywhere/ideationology-lab-b60654e44e37.json')
        sh = gc.open_by_key(spreadsheet_id)
        worksheet = sh.worksheet(worksheet_name)

        existing_data = worksheet.get_all_values()
        unique_element_exists = any(row_data[unique_col_index] == row[unique_col_index] for row in existing_data)

        if not unique_element_exists:
            worksheet.append_row(row_data)

        cur=con.cursor()
        cur.execute("select UNAME from users where EMAIL=? and UPASS=?",(email,pwd))
        data=cur.fetchone()

        if data:
            session['logged_in']=True
            session['username']=data[0]

            if next_url:
                return redirect(next_url)
        
            flash('Login Successfully','success')
            return redirect('/')
        else:
            flash('Invalid Login. Try Again','danger')
    return render_template("login.html")

@app.route('/reg',methods=['POST','GET'])
def reg():
    status=False
    con=sql.connect("pythonanywhere/db_sample.db")

    if request.method=='POST':
        name=request.form["uname"]
        email=request.form["email"]
        pwd=request.form["upass"]

        cur=con.cursor()
        cur.execute("SELECT * FROM users WHERE EMAIL=?", (email,))
        existingInfo = cur.fetchone()

        if existingInfo is not None:
            flash('Email already exist, choose different email.','danger')
            return redirect('reg')

        cur.execute("insert into users(UNAME,UPASS,EMAIL) values(?,?,?)",(name,pwd,email))
        con.commit()
        cur.close()

        flash('Registration Successfully. Login Here...','success')
        return redirect('login')
    return render_template("reg.html", status=status)

@app.route("/logout")
def logout():
    try:
        gc = gspread.service_account(filename='pythonanywhere/ideationology-lab-b60654e44e37.json')
        sh = gc.open_by_key('1akZpxtRhFIm97X9ZIdlAm10nfs0_drWTo40rVvkI6zs')
        worksheet = sh.worksheet('Sheet1')

        cell_list = worksheet.get_all_values()
        row_to_delete = None

        for i, row in enumerate(cell_list):
            if row[0] == session['email']:
                row_to_delete = i + 1
                break

        if row_to_delete:
            worksheet.delete_rows(row_to_delete)
            print(f"Row {row_to_delete} deleted.")
        else:
            print("Element not found, no row deleted.")

        session.clear()
    except:
        pass
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(
        # host="0.0.0.0",
        debug=True
    )
