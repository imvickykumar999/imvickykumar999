
from datetime import datetime
from bson.json_util import dumps
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO, join_room, leave_room
from pymongo.errors import DuplicateKeyError

from vicks.db import get_user, save_user, save_room, add_room_members, get_rooms_for_user, get_room, is_room_member, \
    get_room_members, is_room_admin, update_room, remove_room_members, save_message, get_messages

# from flask_sqlalchemy import SQLAlchemy
import requests, os
# import pyperclip
from bs4 import BeautifulSoup as bs
from werkzeug.utils import secure_filename

from vicks.encrypt import encryptpdf as enc, imgtopdf as imf
from flask import Flask, flash, jsonify, url_for, session, request, redirect, render_template, send_from_directory
# from vicks import terminal

from flask_qrcode import QRcode
from PIL import Image
import ast, json, urllib.request as ur

UPLOAD_FOLDER = 'uploads'
try:
    os.mkdir('uploads')
except Exception as e:
    print(e)
    pass

try:
    os.mkdir('uploads/videos')
except Exception as e:
    print(e)
    pass

try:
    import os
    os.mkdir('uploads/vixtify')
except Exception as e:
    print(e)
    pass

try:
    os.mkdir('uploads/reels')
except Exception as e:
    print(e)
    pass

try:
    os.mkdir('uploads/mashup')
except Exception as e:
    print(e)
    pass

try:
    os.mkdir('uploads/audio')
except Exception as e:
    print(e)
    pass

try:
    os.mkdir('uploads/news')
except Exception as e:
    print(e)
    pass

app = Flask(__name__)
app.secret_key = "secret key"

socketio = SocketIO(app)
login_manager = LoginManager()

login_manager.login_view = 'login'
login_manager.init_app(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# db = SQLAlchemy(app)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def callviews():
    from vicks import crud
    obj1 = crud.vicks('@Hey_Vicks', link = 'https://home-automation-336c0-default-rtdb.firebaseio.com/')
    pageviews = obj1.pull(child = 'Views')
    pageviews += 1
    obj1.push(data = pageviews, child = 'Views')
    return pageviews

@app.route('/pre tests/reels/dist/<filename>')
def send_reels(filename):
    return send_from_directory("pre tests/reels/dist", filename)

# pageviews = callviews()

# ====================================================================================

# import cv2
# from flask import Response

# camera = cv2.VideoCapture(0)  # use 0 for web camera
# camera = cv2.VideoCapture('http://192.168.0.65:8080/video')  # use 0 for web camera
# camera = cv2.VideoCapture('rtsp://freja.hiof.no:1935/rtplive/_definst_/hessdalen03.stream')  # use 0 for web camera
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)

# def gen_frames():  # generate frame by frame from camera
#     camera = cv2.VideoCapture('http://192.168.0.65:8080/video')
#     # camera = cv2.VideoCapture(0)
#     while True:
#         # Capture frame-by-frame
#         success, frame = camera.read()  # read the camera frame
#         if not success:
#             break
#         else:
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
#
#
# @app.route('/live')
# def live():
#     #Video streaming route. Put this in the src attribute of an img tag
#     return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
#
#
# @app.route('/livestream')
# def livestream():
#     """Video streaming home page."""
#     return render_template('live.html')

# ======================================================

@app.route("/reels")
def reels():
    pageviews = callviews()
    return render_template('reels.html',
                           scroll='vickscroll',
                           pageviews=pageviews,
                           path='uploads/reels/1631081300.mp4'
                            )



@app.route('/uploads/reels/<filename>')
def send_exe(filename):
    return send_from_directory("uploads/reels", filename)

# https://github.com/csuhan/ReDet/issues/14#issuecomment-914544044

@app.route("/downloaded_reels", methods=['POST', 'GET'])
def vicks_reels():
    try:
        from flask import request as req
        vid = req.form['reels']

        from vicks import reels
        path = reels.download(vid)
        print(path)

        pageviews = callviews()
        return render_template('reels.html',
                                path=path,
                                scroll='vickscroll',
                                pageviews=pageviews,
                                )

    except Exception as e:
        return render_template("404.html", message = f'{e}')

# ==========================---------=========================

@app.route("/vixtify")
def vixtify():
    pageviews = callviews()
    return render_template('vixtify.html',
                           scroll='vickscroll',
                           pageviews=pageviews,
                           type='playlist',
                           ids=['1Wo3nhrw15u8kiiS5mxKGe'],
                           path=[],
                           )

@app.route('/uploads/vixtify/<filename>')
def send_vixtify(filename):
    return send_from_directory("uploads/vixtify", filename)


@app.route("/downloaded_vixtify", methods=['POST', 'GET'])
def vicks_vixtify():
    try:
        import shutil
        shutil.rmtree('uploads/vixtify')
    except Exception as e:
        print(e)
        pass

    try:
        import os
        os.mkdir('uploads/vixtify')
    except Exception as e:
        print(e)
        pass

    try:
        import spotipy
        from flask import request as req
        from spotipy.oauth2 import SpotifyClientCredentials
        import urllib.request

        client_id = '4a05ec0273d64243990bfee317f48246'
        client_secret = 'ff69fdebe3ea4e61a58f0f0497022c00'

        ClientCredentials = SpotifyClientCredentials( client_id = client_id,
                                                      client_secret = client_secret )

        sp = spotipy.Spotify( auth_manager = ClientCredentials )
        results = sp.search(q=req.form['vixtify'], limit=10)

        app, ids = [], []
        for i in results['tracks']['items']:
            if i['preview_url']:
                print(i['preview_url'])
                app.append(i['preview_url'])
                ids.append(i['album']['external_urls']['spotify'].split('/')[4])

        for i in app[:3]:
            print(i)
            urllib.request.urlretrieve(i, f"uploads/vixtify/{i.split('/')[4].split('?')[0]}.mp3")

        import os
        files = os.listdir('uploads/vixtify')
        print(files)
        spname = []
        for file in files:
            spname.append(file)

        pageviews = callviews()
        return render_template('vixtify.html',
                                path= spname,
                                ids=ids,
                                type='album',
                                scroll='vickscroll',
                                pageviews=pageviews,
                                )

    except Exception as e:
        return render_template("404.html", message = f'{e}')

# =============================================================

@app.route("/memeapi")
def memeapi():
    import requests
    data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
    images = [{'name':image['name'],'url':image['url'],'id':image['id'],
               'box_count':image['box_count']} for image in data]

    return render_template('memeapi.html',
                        images=images,
                        range100=range(100),
                           )

@app.route("/vixmemes")
def vixmemes():
    pageviews = callviews()
    # file = 'drake.jpg'

    import requests
    import random

    data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
    images = [{'name':image['name'],'url':image['url'],'id':image['id'],
               'box_count':image['box_count']} for image in data]

    ran = random.randint(0,100)
    file = images[ran]

    return render_template('vixmemes.html',
                           scroll='vickscroll',
                           file=file['url'],
                           pageviews=pageviews,
                           )

@app.route("/downloaded_vixmemes", methods=['POST', 'GET'])
def vicks_vixmemes():
    try:
        from vicks import defmeme as dm
        from flask import request as req

        idno = req.form['idno']
        text0 = req.form['text0']
        text1 = req.form['text1']

        if text0 == '' or text1 == '':
            text0 = 'C++'
            text1 = 'Python'

        file = dm.memers(idno = int(idno), text0 = text0, text1 = text1)
        # file = dm.pilmeme(text0 = text0, text1 = text1)
        print('============>', file[0])

        # try:
        #     from vicks import instaupload as iu
        #     f = iu.instaup(file[0])
        #     print(f)
        #
        # except Exception as e:
        #     print('/////////--> ', e)

        pageviews = callviews()
        return render_template('vixmemes.html',
                                scroll='vickscroll',
                                file=file[0],
                                pageviews=pageviews,
                                )

    except Exception as e:
        return render_template("404.html", message = f'{e}')

# =============================================================

try:
    os.mkdir('uploads/mnistvix')
except Exception as e:
    print(e)
    pass

@app.route('/uploads/mnistvix/<filename>')
def send_mnistvix(filename):
    return send_from_directory("uploads/mnistvix", filename)

app.config['UPLOAD_mnist'] = 'uploads/mnistvix'

@app.route("/mnistvix")
def mnistvix():
    pageviews = callviews()

    return render_template('mnistvix.html',
                           scroll='vickscroll',
                           pageviews=pageviews,
                           pred=[],
                           rangex=range(0),
                           filn=[],
                           )

@app.route("/downloaded_mnistvix", methods=['POST', 'GET'])
def vicks_mnistvix():
    try:
        import shutil
        shutil.rmtree('uploads/mnistvix')
    except Exception as e:
        print(e)
        pass

    try:
        os.mkdir('uploads/mnistvix')
    except Exception as e:
        print(e)
        pass

    try:
        loc='uploads/mnistvix/error.txt'
        if request.method == 'POST':
            files = request.files.getlist('myfile')

            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    loc = os.path.join(app.config['UPLOAD_mnist'], filename)
                    file.save(loc)
                    print('==========>>> ', loc)

        from vicks import scan
        tesp = scan.test()
        pred = tesp[0]
        filn = tesp[1]
        print('-------------> ', filn)

        pageviews = callviews()
        return render_template('mnistvix.html',
                                scroll='vickscroll',
                                pred=pred,
                                filn=filn,
                                rangex=range(len(filn)),
                                pageviews=pageviews,
                                )

    except Exception as e:
        return render_template("404.html", message = f'{e}')

# =========================================================


@app.route("/mashup")
def mashup():
    pageviews = callviews()
    return render_template('mashup.html',
                           scroll='vickscroll',
                           pageviews=pageviews,
                           path='uploads/mashup/audio1637349073.mp4'
                            )


@app.route('/uploads/mashup/<filename>')
def send_mashup(filename):
    return send_from_directory("uploads/mashup", filename)

# https://github.com/csuhan/ReDet/issues/14#issuecomment-914544044

@app.route("/downloaded_mashup", methods=['POST', 'GET'])
def vicks_mashup():
    try:
        from flask import request as req
        vid = req.form['video']
        aud = req.form['audio']

        from vicks import reels
        import time

        vname = vid.split('/')[4]
        aname = aud.split('/')[4]

        vpath = f"uploads/mashup/{vname}.mp4"
        apath = f"uploads/mashup/{aname}.mp4"

        vpath = reels.download(vid, vpath)
        apath = reels.download(aud, apath)

        # from moviepy.editor import VideoFileClip, AudioFileClip
        import moviepy.editor as mpe

        videoclip = mpe.VideoFileClip(vpath)
        vidur = videoclip.duration
        background_music = mpe.AudioFileClip(apath)
        audur = background_music.duration

        dur = min(audur, vidur)
        print('\n**************-->', dur)
        videoclip = videoclip.subclip(0, dur)
        background_music = background_music.subclip(0, dur)

        new_clip = videoclip.set_audio(background_music)
        new_clip.write_videofile(apath)

        pageviews = callviews()
        return render_template('mashup.html',
                                path=apath,
                                scroll='vickscroll',
                                pageviews=pageviews,
                                )

    except Exception as e:
        return render_template("404.html", message = f'{e}')


# ======================================================

@app.route("/maps")
def maps():

    import re
    import json
    from urllib.request import urlopen

    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    data = json.load(response)

    site_json = {'alt': {},
                 'elevation': {},
                 'latt': '27.17312',
                 'longt': '78.04137',
                 'standard': {'addresst': 'Taj Mahal Internal Path',
                              'city': 'Agra',
                              'confidence': '0.7',
                              'countryname': 'India',
                              'latt': '27.17312',
                              'longt': '78.04137',
                              'postal': '282006',
                              'prov': 'IN',
                              'region': 'Uttar Pradesh',
                              'stnumber': '1'}}

    tablejson = site_json['standard']

    return render_template('maps.html',
                            check='no error',
                            site_json = site_json,
                            tablejson = tablejson,
                            data=data,
                            scroll='vickscroll',
                        )


@app.route("/vicks_maps", methods=['POST', 'GET'])
def vicks_maps():

    try:
        import re
        import json
        from urllib.request import urlopen

        url = 'http://ipinfo.io/json'
        response = urlopen(url)
        data = json.load(response)

        from urllib import request
        from flask import request as req
        from bs4 import BeautifulSoup
        import json

        from pprint import pprint as p
        from urllib.parse import quote

        loc = req.form['maps']
        text_encoded = quote(loc)
        url = f'https://geocode.xyz/{text_encoded}?json=1'

        html = request.urlopen(url).read()
        soup = BeautifulSoup(html,'html.parser')

        site_json = json.loads(soup.text)
        check = list(site_json.keys())[0]
        print('-------------->', check)

        try:
            tablejson = site_json['standard']
        except:
            tablejson = site_json

        return render_template('maps.html',
                               scroll='vickscroll',
                               site_json=site_json,
                               data=data,
                               tablejson=tablejson,
                               check=check,
                               )
    except:
        site_json = {'alt': {},
                     'elevation': {},
                     'latt': '27.17312',
                     'longt': '78.04137',
                     'standard': {'addresst': 'Taj Mahal Internal Path',
                                  'city': 'Agra',
                                  'confidence': '0.7',
                                  'countryname': 'India',
                                  'latt': '27.17312',
                                  'longt': '78.04137',
                                  'postal': '282006',
                                  'prov': 'IN',
                                  'region': 'Uttar Pradesh',
                                  'stnumber': '1'}}

        tablejson = site_json['standard']

        return render_template('maps.html',
                                check='no error',
                                data=data,
                                site_json = site_json,
                                tablejson = tablejson,
                                scroll='vickscroll',
                            )

@app.route("/movies")
def movies():
    pageviews = callviews()
    return render_template('movies.html',
                           applied='yes',
                           movixcode='movixcode',
                           scroll='vickscroll',
                           pageviews=pageviews,
                           passbell='notshow',
                           )

@app.route('/vicks_movies', methods=['POST', 'GET'])
def converted_movies():
    pageviews = callviews()
    movixcode = request.form['movixcode']

    kotaurl = [
       '1KAy0PK9ONvm1yh6nxC6X9jkOb7Km8PD0',
       '1MZOVH1DgkGeNq2WfikG-BueFjpkgOHfv',
       '1Sjr6S66ZUAOSfJTplMWECzdn_yL_LSqU',
       '11I61nhEGrCoRqWkv7E7LJZU71SVfj6ib',
       '17glJSEk5_bmp-_LUh24IJPUagPROwSlu',
       ]

    return render_template('movies.html',
                           movixcode=movixcode,
                           kota25=range(4),
                           kotaurl=kotaurl,
                           pageviews=pageviews,
                           scroll='vickscroll',
                           passbell='showing',
                           applied='no',
                           )

# ===================================================

@app.route("/covid19")
def covid19():
    pageviews = callviews()
    return render_template('covid19.html',
                           ifsent=0,
                           scroll='vickscroll',
                           pageviews=pageviews,
                           l=[
                              {'1key1':'1value1', '1key2':'1value2'},
                              {'2key1':'2value1', '2key2':'2value2'}
                             ],
                           )

@app.route('/converted_covid19', methods=['POST', 'GET'])
def converted_covid19():
    try:
        pageviews = callviews()
        import urllib.request
        import json
        from datetime import datetime

        dnow = datetime.now()
        s = str(dnow).split()[0].split('-')

        # --------------------------------
        y = int(s[0])
        m = int(s[1])
        d = int(s[2])

        date = f'{d}-{m}-{y}'
        pin = request.form['pin']

        if pin == '':
            pin = '302020'

        vaccine = ['COVISHIELD', 'COVAXIN', ][0]
        min_age_limit = request.form['age']
        print('****age*****-> ', min_age_limit)

        if min_age_limit == '':
            min_age_limit = 18
        else:
            min_age_limit = int(min_age_limit)

        # toaddr = request.form['email']
        # if toaddr == '':
        #     toaddr = "imvickykumar999@gmail.com"

        # filename = f"{toaddr.split('@')[0]}.xlsx"
        # ----------------------------------
        # print('.....step 1')

        try:
            url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={pin}&date={date}'

            headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
             'Referer': 'https://cssspritegenerator.com',
             'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
             'Accept-Encoding': 'none',
             'Accept-Language': 'en-US,en;q=0.8',
             'Connection': 'keep-alive'}

            url_request=urllib.request.Request(url, None, headers) #The assembled request
            response = urllib.request.urlopen(url_request)
            f = response.read() # The data u need
            data = json.loads(f.decode('utf-8'))['sessions']
            print(data)

            # with urllib.request.urlopen(f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={pin}&date={date}') as f:
            #     data = json.loads(f.read().decode('utf-8'))['sessions']

        except urllib.error.URLError as e:
            print(e.reason)
            # data = [{'1key1': '1value1', '1key2': '1value2'}, {'2key1': '2value1', '2key2': '2value2'}]

        # print('.....step 2')

        l=[]
        for i, j in enumerate(data):
            if j['available_capacity_dose2']:
                # if j['available_capacity_dose1']:
                    if j['vaccine'] == vaccine:
                        if j['min_age_limit'] == min_age_limit:
                            l.append(j)

        # print(l)
        if l:
            ifsent = 1
            # from vicks import covidmail as cov
            # ifsent = cov.covail(l=l,
            #           toaddr = toaddr,
            #           filename = filename,
            #           )
        else:
            ifsent = 0
            print(l, '...............Email not sent................')

        # import pandas as pd
        # df = pd.DataFrame(data=l)
        # df = df.fillna(' ').T
        # dfhtml = df.to_html()

        return render_template('covid19.html', l=l,
                               ifsent = ifsent,
                               scroll='vickscroll',
                               pageviews=pageviews,
                               # dfhtml = dfhtml,
                               )
    except Exception as e:
        return render_template("404.html", message = f'{e}')

# =====================================================

@app.route('/dist/<filename>')
def send_py2exe(filename):
    return send_from_directory("dist", filename)

# try:
#     os.mkdir('uploads/py2exe')
# except Exception as e:
#     print(e)
#     pass

@app.route("/py2exe")
def py2exe():
    return render_template('py2exe.html', py2exe='None')

@app.route('/converted_py2exe', methods=['POST'])
def converted_py2exe():
    py2exe = request.form['executable']
    print('***************\n', py2exe)

    file = open('hello.txt','w')
    file.write('''
import os
os.system("cls")

''')
    file.write(py2exe)
    file.write('''

input("Press enter to exit.")
''')
    file.close()

    from vicks import runme
    runme.run()

    return render_template('py2exe.html', py2exe=py2exe)

# =====================================================

# Certificate

@app.route("/form")
def form():
    return render_template('form.html',
                            message='Generate Certificate',
                            )

@app.route('/converted_form', methods=['POST', 'GET'])
def converted_form():

    return render_template('form.html',
                           message = 'Here is your Certificate',
                           )

# -------------------------------------------------

@app.route("/vickstube", methods=['GET'])
def vickstube():

    vid = 'k-Tks_Y-VIA'
    tm=0
    prefill = request.args.get('list')

    if prefill == None:
        prefill = request.args.get('vix')
        if prefill == None:
            prefill = ''

    print('-------------> ', prefill)
    if len(prefill) == 11:
        vid = prefill
        tm = request.args.get('t')
        if tm==None:
            tm=0
        print(tm)
        # https://youtu.be/KgbAStrUBNY?t=25

    from vicks import ytc
    dict = ytc.comments(vid)
    info = ytc.tvl(vid)

    # from vicks import crud as c
    # import pandas as pd
    #
    # obj = c.vicks('@Hey_Vicks',
    #     link = 'https://quickstart-1578034411252.firebaseio.com/')
    #
    # obj.add(vid, 'Video/Views')
    # vlist = list(obj.pull('Video/Views').values())
    #
    # counts = pd.Series(vlist).value_counts()
    # print('####################### -> ', counts)
    # vdict = dict(counts.items())
    #
    # recommend = list(vdict.keys())
    # print(recommend)

    pageviews = callviews()
    return render_template("ytc.html",
                            dict=dict,
                            tm=tm,
                            ap=0,
                            prefill = prefill,
                            len = len(prefill),
                            title='None',
                            video_type="0",
                            vidlist = [],
                            vid=vid,
                            range10=range(1,11),
                            # recommend=recommend,
                            recommend=[],
                            pageviews=pageviews,
                            # rangerec=range(recommend),
                            info=info,
                            scroll='vickscroll',
                            )

@app.route('/uploads/videos/<filename>')
def send_videos(filename):
    return send_from_directory("uploads/videos", filename)

@app.route('/uploads/audio/<filename>')
def send_audio(filename):
    return send_from_directory("uploads/audio", filename)

@app.route('/converted_vickstube', methods=['POST'])
def converted_vickstube():

    from vicks import ytc
    from youtube_search import YoutubeSearch

    vidlist = []
    url = request.form['ytc']
    if url == '':
        url = 'https://www.youtube.com/watch?v=Cpc_rHf1U6g'

    pid = vid = None
    try:
        pid = url.split('list=')[1].split('&')[0]
        tm = 945
    except:
        s = url.split('/')
        tm=0

        if s[0] != 'https:':
            vidict = YoutubeSearch(s[0], max_results = 10).to_dict()
            vidlist = []
            for i in vidict:
                vidlist.append(i['id'])
            vid = vidlist[0]
            # print('.....---------', vidlist)

        else:
            if s[2] == 'www.youtube.com':
                vid = s[3].split('=')[1].split('?')[0]

            elif s[2] == 'youtu.be':
                vid = s[3].split('?')[0]

            else:
                vid = 'Cpc_rHf1U6g'
                tm = 945
                print("Sorry... Code couldn't be extracted !!!")

    info = (None, None, None)
    try:
        com = ytc.comments(vid)
        info = ytc.tvl(vid)
    except:
        com = {
            "Comments": ["...are Disabled by user !", "Sorry ...or,", ],
            "Playlist" : ["...do not support Comments !",],
        }

    print(com)
    title = "None"
    video_type = request.form['customRadio'].upper()
    print('............', video_type)

    # if requests.status_code == 429: # ...shifted 404.html
    #     import shutil
    #     shutil.rmtree('uploads/videos')
    #     os.mkdir('uploads/videos')

    from vicks import ytdownload as ytd
    ts = request.form['vts']
    te = request.form['vte']

    if ts=='':
        ts=0
    if te=='':
        te=600

    try:
        ts = int(ts.split(':')[0])*60 + int(ts.split(':')[1])
        te = int(te.split(':')[0])*60 + int(te.split(':')[1])
        print('@@@@@@@@ time @@@@@@@-> ', ts, te)
    except:
        pass

    if pid == None:
        if video_type == "V":
            title = ytd.yt_video(vid, int(ts), int(te))

        elif video_type == "A":
            title = ytd.yt_audio(vid, int(ts), int(te))
        else:
            video_type = "0"
    else:
        video_type = "P"

    # print(title, pid)
    print(vidlist)

    from vicks import crud as c
    import pandas as pd

    obj = c.vicks('@Hey_Vicks',
        link = 'https://quickstart-1578034411252.firebaseio.com/')

    obj.add(vid, 'Video/Views')
    vlist = list(obj.pull('Video/Views').values())

    counts = pd.Series(vlist).value_counts()
    print('####################### -> ', counts)
    vdict = dict(counts.items())

    recommend = list(vdict.keys())[:10]
    print(recommend)

    pageviews = callviews()
    return render_template("ytc.html",
                            dict=com,
                            tm=tm,
                            ap=1,
                            title=title,
                            video_type=video_type,
                            vidlist=vidlist,
                            recommend=recommend,
                            pid = pid,
                            range10=range(1,11),
                            rangerec=range(len(recommend)),
                            info=info,
                            pageviews=pageviews,
                            vid=vid,
                            scroll='vickscroll',
                            )

# ========================================================

# https://myaccount.google.com/u/3/lesssecureapps?pli=1&rapt=AEjHL4MpjjYh8Z-01vJ5GRsQXICYQsXHG0PweSjWenlbAJfes6qNKbHKs_CfCVh0d5qUO58qFeeB0sYCbA3GANLf-965469dVA

@app.route("/vicksmail")
def vicksmail():
    return render_template("mailsent.html", sent='no')

@app.route("/mail_sent", methods=['POST'])
def mail_sent():
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    fromaddr = "sagar.sws2000@gmail.com"
    toaddr = request.form['credentials']

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr

    msg['Subject'] = "Vicks OTP"
    import random
    otp = str(random.randint(1000,9999))
    # otp = '7639'

    file1 = open("otp.txt", "w")
    file1.write(otp)
    file1.write(toaddr)
    file1.close()

    body = f'''\
        <html>
          <head>Vicks Quotes</head>
          <body>

            <h2 style="color:green;">
               Hi, <br> {''.join(toaddr.split('@')[0])}
            </h2>
            <br>

           <h1>
               Here is the OTP you wanted.
               <br><br> {otp}
           </h1>

          </body>
        </html>
    '''
    msg.attach(MIMEText(body, 'html'))

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, "gjkF@%$TLLHgehnJ354bgfgb5gdf")

    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()
    return render_template("mailsent.html", sent='yes')

def plot_url(data):
    import matplotlib.pyplot as plt
    import io, base64

    def countFreq(arr, n):
        mp = dict()
        for i in range(n):
            if arr[i] in mp.keys():
                mp[arr[i]] += 1
            else:
                mp[arr[i]] = 1
        return mp

    arr = list(data.values())
    n = len(arr)
    mp = countFreq(arr, n)
    print('\n************---> ', mp)

    img = io.BytesIO()
    y = list(mp.values())
    x = list(mp.keys())

    fig = plt.figure(figsize = (5, 5))
    plt.bar(x, y, color ='red', width = 0.4)

    plt.xlim(0,5)
    plt.grid(True)

    plt.xlabel("Options  --->")
    plt.ylabel("No. of Votes  --->")
    plt.title("Favourite ice Cream Flavour : Poll Result\n")

    plt.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

@app.route("/poll")
def poll():
    from vicks import crud

    obj1 = crud.vicks('@Hey_Vicks',
     link = 'https://new-project-ab9c7-default-rtdb.firebaseio.com/')

    data = obj1.pull('Group/Chat')
    if data == None:
        obj1.push()
    data = obj1.pull('Group/Chat')

    pageviews = callviews()
    return render_template("poll.html",
                           scroll='vickscroll',
                           pageviews=pageviews,
                           data1 = plot_url(data),
                           data2=data,
                           )

@app.route('/converted_poll', methods=['POST'])
def converted_poll():
    from vicks import crud

    credentials = '@Hey_Vicks'
    otp = request.form['otp'].strip()

    f=open("otp.txt",'r')
    f = f.read()
    getotp = f[:4]
    person = f[4:].split('@')[0]

    f = open("otp.txt", "w")
    f.write('-')
    f.close()

    if otp == getotp and otp != '-':
        if person == '':
            obj1 = crud.vicks(credentials, link = 'https://new-project-ab9c7-default-rtdb.firebaseio.com/')
        else:
            obj1 = crud.vicks(credentials, name = person,
            link = 'https://new-project-ab9c7-default-rtdb.firebaseio.com/')

        message = int(request.form['message'])
        if message == '':
            obj1.push()
        else:
            obj1.push(message, child = f'Group/Chat/{person}')

        data = obj1.pull('Group/Chat')
        print('------------------------->', data)
        pageviews = callviews()

        return render_template("poll.html",
                               scroll='vickscroll',
                               pageviews=pageviews,
                               data1 = plot_url(data),
                               data2=data,
                               )
    else:
        return render_template("404.html", message = 'Wrong OTP')

# ------------------------------------------------------

@app.route("/yourquotes")
def yourquotes():
    # https://console.firebase.google.com/u/0/project/chatting-c937e/database/chatting-c937e-default-rtdb/data
    from vicks import crud
    obj1 = crud.vicks('@Hey_Vicks')

    data = obj1.pull('Group/Chat')
    # print('=============================', data)

    if data == None:
        obj1.push()

    data = obj1.pull('Group/Chat')
    print('------------------------->', data)
    pageviews = callviews()
    return render_template("yourquotes.html",
                           # scroll='vickscroll',
                           pageviews=pageviews,
                           data = data,
                           )


@app.route('/converted_yourquotes', methods=['POST'])
def converted_yourquotes():
    from vicks import crud

    credentials = request.form['credentials']
    otp = request.form['otp'].strip()

    if credentials != '@Hey_Vicks':
        return render_template("404.html", message = 'Wrong Credentials')

    f=open("otp.txt",'r')
    f = f.read()
    getotp = f[:4]
    person = f[4:].split('@')[0]
    # print('%%%%%%%%%%%-> ', getotp, person)

    f = open("otp.txt", "w")
    f.write('-')
    f.close()

    if otp == getotp and otp != '-':
        if person == '':
            obj1 = crud.vicks(credentials)
        else:
            # print(credentials)
            obj1 = crud.vicks(credentials, name = person)

        message = f'''
        {request.form['message']}
        '''
        if message == '':
            obj1.push()
        else:
            obj1.push(message)

        data = obj1.pull('Group/Chat')
        # data = {v: k for k, v in data.items()}
        print('------------------------->', data)
        pageviews = callviews()

        return render_template("yourquotes.html",
                               # scroll='vickscroll',
                               pageviews=pageviews,
                               data = data,
                               )
    else:
        return render_template("404.html", message = 'Wrong OTP')

# ====================================================


@app.route('/iotcar')
def iotcar():

    from firebase import firebase
    firebase_obj = firebase.FirebaseApplication('https://iot-car-parking-da247-default-rtdb.firebaseio.com/', None)

    result1 = firebase_obj.get('/slot1', None)
    data1="{}".format(result1)

    result2 = firebase_obj.get('/slot2', None)
    data2="{}".format(result2)

    # list_result = list(result.values())[-11:-1]
    # is_occupied = sum(list_result)/10

    # with open('YOLO/data1.txt', "r") as myfile:
    #     slot1 = myfile.read().splitlines()
    # a = [len(i) for i in slot1]
    # i = a.index(max(a))
    # car1 = slot1[i].strip()
    #
    # with open('YOLO/data2.txt', "r") as myfile:
    #     slot2 = myfile.read().splitlines()
    # a = [len(i) for i in slot2]
    # i = a.index(max(a))
    # car2 = slot2[i].strip()

    if result1 == 1:
        img1="static/screenshots/present.png"
    else:
        img1="static/screenshots/absent.png"

    if result2 == 1:
        img2="static/screenshots/present.png"
    else:
        img2="static/screenshots/absent.png"

    return render_template("iotcar.html",
                            data=[data1, data2],
                            car=['MH01AE8017', 'AS 9527XZ'],
                            img=[img1, img2],
                            len=2
                          )

    # return redirect(url_for('iotcar'),
    #                         # data=[data1, data2],
    #                         # img=[img1, img2],
    #                         # len=2
    #                       )

@app.route("/share")
def share():
    return render_template("share.html")

# ================================================


@app.route('/adafruit')
def adafruit():

    from vicksbase import firebase as vix
    firebase_obj = vix.FirebaseApplication('https://home-automation-336c0-default-rtdb.firebaseio.com/', None)

    from Adafruit_IO import Client, Data

    aio = Client('imvickykumar999', 'aio_uOXe85j28wfog5Ix3SE8Np0nO4Ke')
    feed = 'ledswitch'

    data = aio.receive(feed).value
    if data == 'ON':
        d=1
    else:
        d=0

    firebase_obj.put('A/B/C','Switch', d)
    result1 = firebase_obj.get('A/B/C/Switch', None)
    data1="{}".format(result1)

    if data1 == '1':
        img = 'static/logo/bulbon.jpg'
    else:
        img = 'static/logo/bulboff.jpg'

    return render_template("adafruit.html",
                            data=data1,
                            img = img
                          )

# -------------------------------------------

@app.route('/')
def iotled():

    # from vicksbase import firebase as vix
    # firebase_obj = vix.FirebaseApplication('https://home-automation-336c0-default-rtdb.firebaseio.com/', None)
    # result1 = firebase_obj.get('A/B/C/Switch', None)

    import multivicks.crud as c
    obj = c.vicks('@Hey_Vicks', 'Vicky', 'https://home-automation-336c0-default-rtdb.firebaseio.com/')
    result1 = obj.pull('A/B/C/Switch')
    if result1 == '':
        result1 = None

    data1="{}".format(result1)
    print(data1)

    if data1 == '1':
        img = 'static/logo/bulbon.jpg'
    elif data1 == '0':
        img = 'static/logo/bulboff.jpg'
    else:
        img = 'static/logo/error.png'

    pageviews = callviews()
    return render_template("iotled.html",
                            data=data1,
                            pageviews=pageviews,
                            scroll='vickscroll',
                            img = img,
                          )


@app.route('/converted_iotled', methods=['POST'])
def converted_iotled():

    import multivicks.crud as c

    credentials = request.form['credentials']
    obj = c.vicks(credentials, 'Vicky', 'https://home-automation-336c0-default-rtdb.firebaseio.com/')

    data = request.form['turn']
    if data == '':
        data = None
    else:
        data = int(data)
    obj.push(data, 'A/B/C/Switch')

    result1 = obj.pull('A/B/C/Switch')
    data1="{}".format(result1)
    # print(data1)

    if data1 == '1':
        img = 'static/logo/bulbon.jpg'
    elif data1 == '0':
        img = 'static/logo/bulboff.jpg'
    else:
        img = 'static/logo/error.png'

    pageviews = callviews()
    return render_template("iotled.html",
                            data=data1,
                            pageviews=pageviews,
                            scroll='vickscroll',
                            img = img,
                          )

# --------------------------------------------

@app.route("/playfair_cipher")
def playfair_cipher():

    data0 = "security, monarchy"
    data1 = "eiioqoyldc, instruments"
    data2 = "stalxlings, gatlmzclrqtx"

    return render_template("playfair_cipher.html",
                            data0=data0,
                            data1=data1,
                            data2=data2
                            )


@app.route('/converted_playfair_cipher', methods=['POST'])
def converted_playfair_cipher():

    from vicks import playfair_cipher as vix
    key = request.form['playfair_cipher_key']
    text = request.form['playfair_cipher_text']
    data = vix.encrypt(key, text)

    return render_template("playfair_cipher.html",
                            data0=key.upper(),
                            data1=data[0],
                            data2=data[1]
                            )

# -------------------------------------------------


@app.route("/qrcode")
def qrcode():
    data = "https://api.whatsapp.com/send/?phone=918239957923&text=Hi%20Vicky,%20I%20want%20to%20buy%20you%20coffee!"
    img = "static\screenshots\donate.png"
    return render_template("qrcode.html",
                            data=data,
                            img=img)

@app.route('/converted_qrcode', methods=['POST'])
def converted_qrcode():

    data = request.form['qrcode']
    qrcode = QRcode()
    img = qrcode(data, border=10)

    return render_template("qrcode.html",
                            img=img,
                            data=data)

@app.route("/ipynb")
def ipynb():
    return render_template("ipynb.html", infolist = [["Output"]])

@app.route('/converted_ipynb', methods=['POST'])
def convert_ipynb():

    def ipynbinfo(info, file_name):
        def call(file_name):

            if 'http' == file_name[0:4]:
                print('\nPlease WAIT, content is loading from URL...\n')
                su = ur.urlopen(str(file_name)).read().decode('ascii')

            elif '{' == file_name[0]:
                su = file_name

            elif '\\' or '/' in file_name:
                su = open(file_name).read()

            try:
                y = json.loads(str(su))
            except:
                y = su
            return ast.literal_eval(str(y))

        def recdict(d):
            try:
                box.append(d[info])
            except Exception as e:
                pass

            for i in list(d.values()):
                if type(i) == list:
                    for j in i:

                        if type(j) == dict:
                            recdict(j)

                if type(i) == dict:
                    recdict(i)
            return box
        return recdict(call(file_name))

    n, box = 130, []
    file_name = request.form['ipynb']

    if file_name == '':
        file_name = 'https://raw.githubusercontent.com/imvickykumar999/vixtor/master/vixtor.ipynb'

    infolist = ipynbinfo('source', file_name)
    # for i in infolist:
    #     for j in i:
    #         print(j)
    #     print('='*n, end='\n\n')

    return render_template('ipynb.html', infolist = infolist, range = range(40))

@app.route("/morse")
def morse():
    return render_template("morse.html", text = "Output")

@app.route('/converted_morse', methods=['POST'])
def convert_morse():

    decrypted = [' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6',
                 '7', '8', '9', '0', ',', '?', '(', ')', '!']

    encrypted = ['/', '.-', '-...', '-.-.', '-..', '.', '..-.', '--.',
                 '....', '..', '.---', '-.-', '.-..', '--', '-.', '---',
                 '.--.', '--.-', '.-.', '...', '-', '..-', '...-', '.--',
                 '-..-', '-.--', '--..', '.----', '..---', '...--', '....-',
                 '.....', '-....', '--...', '---..', '----.', '-----', '--..--',
                 '..--..', '-.--.', '-.--.-', '-.-.--']

    morse_enc = dict(zip(decrypted, encrypted))
    morse_dec = dict([(encrypted, decrypted) for decrypted,
                      encrypted in morse_enc.items()])

    test = request.form['morse']
    # test = input('Enter Morse Code or, Simple Text (or, just Press Ok/Enter for default entry) : ')
    if test == '':
        test = '- .... . / -.. ..- .-. .- - .. --- -. / --- ..-. / .- / -.. .- ... .... / .. ... / - .... .-. . . / - .. -- . ... / - .... . / -.. ..- .-. .- - .. --- -. / --- ..-. / .- / -.. --- - --..-- / . .- -.-. .... / -.. --- - / --- .-. / -.. .- ... .... / .-- .. - .... .. -. / .- / -.-. .... .- .-. .- -.-. - . .-. / .. ... / ..-. --- .-.. .-.. --- .-- . -.. / -... -.-- / .--. . .-. .. --- -.. / --- ..-. / ... .. --. -. .- .-.. / .- -... ... . -. -.-. . --..-- / -.-. .- .-.. .-.. . -.. / .- / ... .--. .- -.-. . --..-- / . --.- ..- .- .-.. / - --- / - .... . / -.. --- - / -.. ..- .-. .- - .. --- -. --..-- / - .... . / .-.. . - - . .-. ... / --- ..-. / .- / .-- --- .-. -.. / .- .-. . / ... . .--. .- .-. .- - . -.. / -... -.-- / .- / ... .--. .- -.-. . / --- ..-. / -.. ..- .-. .- - .. --- -. / . --.- ..- .- .-.. / - --- / - .... .-. . . / -.. --- - ... --..-- / .- -. -.. / - .... . / .-- --- .-. -.. ... / .- .-. . / ... . .--. .- .-. .- - . -.. / -... -.-- / .- / ... .--. .- -.-. . / . --.- ..- .- .-.. / - --- / ... . ...- . -. / -.. --- - ... /'

    test = test.replace("_", "-").upper()
    test_list = test.split(' ')

    decrypt = []
    def convert(j):
        for i in j:
            try:
              decrypt.append((morse_enc[i]))
            except:
              try:
                decrypt.append((morse_dec[i]))
              except:
                pass

    if not any(ele in encrypted for ele in test_list):
        box=[]
        for i in test_list:
            box.append(i+' ')
        test_list = box

        for j in test_list:
            convert(j)
            text = ' '.join(decrypt)
    else:
        convert(test_list)
        text = ''.join(decrypt)

#     pyperclip.copy(text)
#     flash(f'Note: Output of {test} is copied in clipboard !!!')
    return render_template('morse.html', text = text)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    loc='uploads/error.txt'
    if request.method == 'POST':

        # check if the post request has the files part
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')
        password = request.form['unique']

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                loc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(loc)

                try:
                    loc = enc(loc, password)
                except:
                    try:
                        loc = enc(imf(loc), password)
                    except:
                        pass
        # return render_template('complete.html', aloc=aloc)

#         pyperclip.copy(loc)
        flash(f'Shareable link is https://imvickykumar999.herokuapp.com/{loc}')
        return redirect(f'/{loc}')

# def redirect(loc):
#     return redirect(f'/{loc}')

@app.route('/uploads/<filename>')
def send_image(filename):
    return send_from_directory("uploads", filename)

@app.route('/<filename>')
def send_all(filename):
    return send_from_directory(".", filename)

@app.route('/hacker_vicky')
def hacker_vicky():
    image_names = os.listdir('./uploads')

    from pathlib import Path
    paths = sorted(Path('./uploads').iterdir(),
                        key=os.path.getmtime)
    dist = sorted(Path('.').iterdir(),
                        key=os.path.getmtime)
    audio_path = sorted(Path('./uploads/audio').iterdir(),
                        key=os.path.getmtime)
    news_path = sorted(Path('./uploads/news').iterdir(),
                        key=os.path.getmtime)
    video_path = sorted(Path('./uploads/videos').iterdir(),
                        key=os.path.getmtime)
    reels_path = sorted(Path('./uploads/reels').iterdir(),
                        key=os.path.getmtime)
    # py2exe = sorted(Path('./uploads/py2exe').iterdir(),
    #                     key=os.path.getmtime)

    return render_template("gallery.html",
                            dist=dist,
                            # py2exe=py2exe,
                            image_names=image_names,
                            reels_path=reels_path,
                            audio_path=audio_path,
                            news_path=news_path,
                            video_path=video_path,
                            paths=paths,
                            )

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/skills')
def skills():
    return render_template('skills.html')

# =======================================================

@app.route('/news')
def news():
    from gtts import gTTS
    try:
        pageviews = callviews()
        print('= = = = = = = => ', pageviews)

        link = 'https://inshorts.com/en/read'
        req = requests.get(link)

        soup = bs(req.content, 'html5lib')
        box = soup.findAll('div', attrs = {'class':'news-card z-depth-1'})

        ha,ia,ba,la,ta,sa = [],[],[],[],[],[]
        for i in range(len(box)):
            h = box[i].find('span', attrs = {'itemprop':'headline'}).text

            m = box[i].find('div', attrs = {'class':'news-card-image'})
            m = m['style'].split("'")[1]

            s = box[i].find('div', attrs = {'class':'news-card-title news-right-box'}).a['href']
            s = 'https://inshorts.com' + s

            b = box[i].find('div', attrs = {'itemprop':'articleBody'}).text
            tts = gTTS(b)
            t = ''.join([i for i in h if i.isalpha()])

            l='link not found'
            try:
                l = box[i].find('a', attrs = {'class':'source'})['href']
            except:
                pass

            ha.append(h)
            ia.append(m)
            ba.append(b)
            la.append(l)
            ta.append(t)
            sa.append(s)

        return render_template('news.html',
                                ha=ha,
                                ia=ia,
                                ba=ba,
                                la=la,
                                ta=ta,
                                sa=sa,
                                listen=0,
                                pageviews=pageviews,
                                range_ha = range(len(box)),
                                )
    except Exception as e:
        print(e)
        return render_template('404.html')


@app.route('/listen_news', methods=['POST'])
def listen_news():
    from gtts import gTTS

    # empty = False
    # if len(os.listdir('uploads/news')) == 0:
    #     empty = True

    try:
        listen = request.form['customRadio']
        print('======================>', listen)

        link = 'https://inshorts.com/en/read'
        req = requests.get(link)

        soup = bs(req.content, 'html5lib')
        box = soup.findAll('div', attrs = {'class':'news-card z-depth-1'})

        ha,ia,ba,la,ta,sa = [],[],[],[],[],[]
        if listen == '0':
            range_ha = len(box)
        else:
            range_ha = 10

        for i in range(range_ha):
            h = box[i].find('span', attrs = {'itemprop':'headline'}).text

            m = box[i].find('div', attrs = {'class':'news-card-image'})
            m = m['style'].split("'")[1]

            s = box[i].find('div', attrs = {'class':'news-card-title news-right-box'}).a['href']
            s = 'https://inshorts.com' + s

            b = box[i].find('div', attrs = {'itemprop':'articleBody'}).text
            tts = gTTS(b)

            t = ''.join([i for i in h if i.isalpha()])

            # if empty:
            if listen == '1':
                tts.save(f'uploads/news/{t}.mp3')

            l='link not found'
            try:
                l = box[i].find('a', attrs = {'class':'source'})['href']
            except:
                pass

            ha.append(h)
            ia.append(m)
            ba.append(b)
            la.append(l)
            ta.append(t)
            sa.append(s)

        # try:
        #     entry_id = int(request.args.get('entry_id'))
        #     print(entry_id+1)
        #
        #     import pyttsx3
        #     engine = pyttsx3.init()
        #
        #     rate = engine.getProperty('rate')
        #     engine.setProperty('rate', 150)
        #
        #     voices = engine.getProperty('voices')
        #     engine.setProperty('voice', voices[1].id)
        #
        #     engine.say(f"{ba[entry_id]}")
        #     engine.runAndWait()
        #
        # except:
        #     print('passed...')
        #     pass

        return render_template('news.html',
                                ha=ha,
                                ia=ia,
                                ba=ba,
                                la=la,
                                sa=sa,
                                ta=ta,
                                listen=listen,
                                scroll='vickscroll',
                                range_ha = range(range_ha),
                                )
    except Exception as e:
        print(e)
        return render_template('404.html')

# ==========================================================

@app.route('/uploads/news/<filename>')
def send_news(filename):
    return send_from_directory("uploads/news", filename)

@app.errorhandler(404)
def page_not_found(e):
    try:
        # import shutil
        # shutil.rmtree('uploads/videos')
        os.mkdir('uploads/videos')
    except:
        pass
    return render_template('404.html', message = 'Try Again Later...'), 404

@app.route('/chat')
def chat():
    rooms = []
    if current_user.is_authenticated:
        rooms = get_rooms_for_user(current_user.username)
    return render_template("chat.html", rooms=rooms)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chat'))

    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password_input = request.form.get('password')
        user = get_user(username)

        if user and user.check_password(password_input):
            login_user(user)
            return redirect(url_for('chat'))
        else:
            message = 'Failed to login!'
    return render_template('login.html', message=message)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('chat'))

    message = 'Welcome to Vicks Chat Room'
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            save_user(username, email, password)
            return redirect(url_for('login'))
        except DuplicateKeyError:
            message = "User already exists!"
    return render_template('signup.html', message=message)


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('news'))


@app.route('/create-room/', methods=['GET', 'POST'])
@login_required
def create_room():
    message = ''
    if request.method == 'POST':
        room_name = request.form.get('room_name')
        usernames = [username.strip() for username in request.form.get('members').split(',')]

        if len(room_name) and len(usernames):
            room_id = save_room(room_name, current_user.username)
            if current_user.username in usernames:
                usernames.remove(current_user.username)
            add_room_members(room_id, room_name, usernames, current_user.username)
            return redirect(url_for('view_room', room_id=room_id))
        else:
            message = "Failed to create room"
    return render_template('create_room.html', message=message)


@app.route('/rooms/<room_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_room(room_id):
    room = get_room(room_id)
    if room and is_room_admin(room_id, current_user.username):
        existing_room_members = [member['_id']['username'] for member in get_room_members(room_id)]
        room_members_str = ",".join(existing_room_members)
        message = ''
        if request.method == 'POST':
            room_name = request.form.get('room_name')
            room['name'] = room_name
            update_room(room_id, room_name)

            new_members = [username.strip() for username in request.form.get('members').split(',')]
            members_to_add = list(set(new_members) - set(existing_room_members))
            members_to_remove = list(set(existing_room_members) - set(new_members))
            if len(members_to_add):
                add_room_members(room_id, room_name, members_to_add, current_user.username)
            if len(members_to_remove):
                remove_room_members(room_id, members_to_remove)
            message = 'Room edited successfully'
            room_members_str = ",".join(new_members)
        return render_template('edit_room.html', room=room, room_members_str=room_members_str, message=message)
    else:
        return "Room not found", 404


@app.route('/rooms/<room_id>/')
@login_required
def view_room(room_id):
    room = get_room(room_id)
    if room and is_room_member(room_id, current_user.username):
        room_members = get_room_members(room_id)
        messages = get_messages(room_id)
        return render_template('view_room.html', username=current_user.username, room=room, room_members=room_members,
                               messages=messages)
    else:
        return "Room not found", 404


@app.route('/rooms/<room_id>/messages/')
@login_required
def get_older_messages(room_id):
    room = get_room(room_id)
    if room and is_room_member(room_id, current_user.username):
        page = int(request.args.get('page', 0))
        messages = get_messages(room_id, page)
        return dumps(messages)
    else:
        return "Room not found", 404


@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has sent message to the room {}: {}".format(data['username'],
                                                                    data['room'],
                                                                    data['message']))
    data['created_at'] = datetime.now().strftime("%d %b, %H:%M")
    save_message(data['room'], data['message'], data['username'])
    socketio.emit('receive_message', data, room=data['room'])


@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])


@socketio.on('leave_room')
def handle_leave_room_event(data):
    app.logger.info("{} has left the room {}".format(data['username'], data['room']))
    leave_room(data['room'])
    socketio.emit('leave_room_announcement', data, room=data['room'])


@login_manager.user_loader
def load_user(username):
    return get_user(username)


if __name__ == '__main__':
    socketio.run(app, debug=True)


# from app import app
# from livereload import Server
#
# if __name__ == '__main__':
#     server = Server(app.wsgi_app)
#     server.serve(debug=True)
