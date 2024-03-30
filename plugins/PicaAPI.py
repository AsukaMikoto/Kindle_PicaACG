import requests
import json
from plugins.PicaHeaders import *

proxy = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

def httpPost(url, data, headers):
    return requests.post(url, data=data, headers=headers, verify=False, proxies=proxy)

def httpGet(url, headers):
    return requests.get(url, headers=headers, verify=False, proxies=proxy)

def pica_login(email, password):
    url = PICA_API_URL + 'auth/sign-in'
    data = {'email':email, 'password':password}
    response = json.loads(httpPost(url, json.dumps(data), getHeaders('POST', None, url)).text)
    if response['code'] == 400:
        response = {'status':-1, 'token':''}
    elif response['code'] == 200:
        response = {'status':1, 'token':response['data']['token']}
    return response

def pica_getUserFavorite(token, page, newToOld):
    url = PICA_API_URL + 'users/favourite?s={}&page={}'.format('dd' if newToOld == True else 'da', page)
    response = json.loads(httpGet(url, getHeaders('GET', token, url)).text)
    return response

def pica_getMostNewMostHotManga(token, page):
    url = PICA_API_URL + 'comics?page={}&s=dd'.format(page)
    response = json.loads(httpGet(url, getHeaders('GET', token ,url)).text)
    return response