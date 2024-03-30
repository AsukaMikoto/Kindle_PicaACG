from flask import Flask, session, make_response,render_template
from flask import request
from plugins.PicaAPI import *

import base64

app = Flask(__name__)
app.secret_key = PICA_API_KEY

## custom filter
# image get
def imageGet(url, uri):
    if str(url).find('https://storage1.picacomic.com')!=-1:
        picUrl = '{}/{}'.format(str(url).replace('https://storage1.picacomic.com', 'https://storage1.picacomic.com/static'), uri)

    if str(uri).find('tobeimg/')!=-1:
        url = 'https://img.picacomic.com'
        picUrl = '{}/{}'.format(url, str(uri).replace('tobeimg/', ''))
    else:
        picUrl = '{}/{}'.format(url, str(uri).replace('tobs/', 'static/'))
    print(picUrl)
    headers = {'host': str(url).replace('https://','')}
    response = httpGet(picUrl, headers)
    picBase64 = base64.b64encode(response.content).decode('utf-8')
    # print(picBase64)
    return 'data:image/jpeg;base64,{}'.format(picBase64)

#Default
@app.route('/', methods = ['GET'])
def index():
    # return render_template('home.html', title = 'PicaACG for Kindle - Index')
    if 'token' in session:
        print('token=>{}'.format(session['token']))
        newManga = pica_getMostNewMostHotManga(session['token'], 1)
        newMangaList = newManga['data']['comics']['docs']
        print(newManga)
        favorite = pica_getUserFavorite(session['token'], 1, True)
        favoriteList = favorite['data']['comics']['docs']
        return render_template('home.html', title = 'PicaACG for Kindle - Index', newMange = newMangaList, favoriteList = favoriteList, imageGet = imageGet)
    return render_template("login.html", title = 'PicaACG for Kindle - User Login')

@app.route('/login', methods = ['GET'])
def login_page():
    if 'token' in session:
        return render_template('home.html', title = 'PicaACG for Kindle - Index')
    return render_template("login.html", title = 'PicaACG for Kindle - User Login')

@app.route('/login', methods = ['POST'])
def login_api():

    # result
    result = {}

    json_data = request.get_json()
    if json_data['email'] == None or json_data['email']=='':
        session['status'] = -1
    elif json_data['password'] == None or json_data['password'] == '':
        session['status'] = -2
    else:
        email = json_data['email']
        password = json_data['password']
        result = pica_login(email, password)
        if result['status'] !=1:
            session['status'] = -3
        else:
            result.update({'token': result['token']})
            session['token'] = result['token']
            session['status'] = 0
    
    result.update({'status':session['status']})
    return result

# 给扫描机器人使用的请求 所有不存在的URI都返回403
@app.route('/<path>',methods = ['GET','POST'])
def noAuthentication(path = ''):
    return '',403

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 9100
    app.run(host=host,port=port)