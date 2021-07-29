from flask import Flask
from flask import request
from flask import render_template
import time

app = Flask(__name__)

def long_load(typeback):
    time.sleep(5) #just simulating the waiting period
    return "You typed: %s" % typeback

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def form(display=None):
    query = request.form['anything']
    outcome = long_load(query)
    return render_template("done.html", display=outcome)

if __name__ == '__main__':
    #app.debug = True
    app.run()
