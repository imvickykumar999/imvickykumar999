
# https://stackoverflow.com/a/57864823/11493297

from flask import Flask, flash, jsonify, url_for, session, request, redirect, render_template, send_from_directory

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def app_home():
    return render_template("passarg.html",
                            variable_here = ['1','2','3','4','5'],
                            range5 = range(5),
                            )

@app.route("/getData", methods=['GET'])
def getData():

    entry1Value = request.args.get('entry1_id')
    print(entry1Value)

    import pyttsx3
    engine = pyttsx3.init()

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

    engine.say(f"Hello, I am speaking title {entry1Value}")
    engine.runAndWait()

    return jsonify({ 'var1': str(entry1Value) })


@app.route('/linkedin')
def linkedin():
    return render_template("linkedin.html")

@app.route('/uploads/<filename>')
def send_videos(filename):
    return send_from_directory("uploads", filename)

@app.route('/instagram/<username>')
def instagram(username):

    import data.crud as c

    obj = c.vicks('@Hey_Vicks', 'Vicky', 'https://home-automation-336c0-default-rtdb.firebaseio.com/')
    obj.push(1, 'A/B/C/Switch')

    result = obj.pull('A/B/C/Switch')
    data="{}".format(result)
    print(data)

    return render_template("instagram.html",
                            username=username,
                            data=data,
                            )


if __name__ == '__main__':
   app.run(debug=True)
