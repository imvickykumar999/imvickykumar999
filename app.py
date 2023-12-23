
from flask import (Flask,
    render_template,
    request, redirect,
    url_for, flash,
    session,
)

from functools import wraps
import secrets, gspread
import sqlite3 as sql
import requests, random

app = Flask(__name__)
secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key

def get_news(source, api_key='39e270768fef4cfe848af36d98107e82'):
    try:
        gets = f'https://newsapi.org/v1/articles?source={source}&sortBy=top&apiKey={api_key}'
        req = requests.get(gets) 
        box = req.json()['articles']

    except:
        pass

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
			return redirect(url_for('login'))
	return wrap

@app.route('/news/<source>')
@is_logged_in
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

@app.route('/login',methods=['POST','GET'])
def login():
    status=True
    con=sql.connect("db_sample.db")

    if request.method=='POST':
        email=request.form["email"]
        pwd=request.form["upass"]

        cur=con.cursor()
        cur.execute("select UNAME from users where EMAIL=? and UPASS=?",(email,pwd))
        data=cur.fetchone()

        print(data)
        if data:
            session['logged_in']=True
            session['username']=data[0]
            flash('Login Successfully','success')
            return redirect('/')
        else:
            flash('Invalid Login. Try Again','danger')
    return render_template("login.html")

def is_logged_in(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash('Unauthorized, Please Login','danger')
			return redirect(url_for('login'))
	return wrap

@app.route('/reg',methods=['POST','GET'])
def reg():
    status=False
    con=sql.connect("db_sample.db")

    if request.method=='POST':
        name=request.form["uname"]
        email=request.form["email"]
        pwd=request.form["upass"]
        newsletter = request.form.get('newsletter')

        if newsletter:
            row_data = [email]
            spreadsheet_id = '1akZpxtRhFIm97X9ZIdlAm10nfs0_drWTo40rVvkI6zs'
            worksheet_name = 'Sheet1'
            unique_col_index = 0 

            gc = gspread.service_account(filename='automation/ideationology-lab-b60654e44e37.json')
            sh = gc.open_by_key(spreadsheet_id)
            worksheet = sh.worksheet(worksheet_name)

            existing_data = worksheet.get_all_values()
            unique_element_exists = any(row_data[unique_col_index] == row[unique_col_index] for row in existing_data)

            if not unique_element_exists:
                worksheet.append_row(row_data)

        cur=con.cursor()
        cur.execute("insert into users(UNAME,UPASS,EMAIL) values(?,?,?)",(name,pwd,email))
        con.commit()
        cur.close()

        flash('Registration Successfully. Login Here...','success')
        return redirect('login')
    return render_template("reg.html",status=status)

@app.route("/logout")
def logout():
	session.clear()
	flash('You are now logged out','success')
	return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(
        # host="0.0.0.0", 
        debug=True
    )
