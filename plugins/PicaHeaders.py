import os, uuid
import hmac, hashlib
from datetime import datetime

# const
PICA_API_URL = 'https://picaapi.picacomic.com/'
PICA_API_KEY = 'C69BAF41DA5ABD1FFEDC6D2FEA56B'
PICA_APP_VERSION = '2.2.1.3.3.4'
PICA_APP_BUILD_VERSION = '45'
PICA_VERSION = 'v1.4.1'

def genUUID():
    _uuid = ''
    if os.path.exists('./plugins/uuid.bin'):
        file = open('./plugins/uuid.bin', 'r')
        _uuid = file.readline()
        file.close()
    else:
        file = open('./plugins/uuid.bin', 'w')
        _uuid = uuid.uuid4()
        file.write(str(_uuid))
        file.close()
    return _uuid

def createNonce():
    return str(genUUID()).replace('-', '')

def createSignature(path, nonce, time, method):
    path = str(path).replace(PICA_API_URL, '')
    print(path)

    key = str(path + time + nonce + method + PICA_API_KEY)
    # tm的每个版本不一样，但是写死的
    data = '~d}$Q7$eIni=V)9\\RK/P.RM4;9[7|@/CA}b~OW!3?EV`:<>M7pddUBL5n|0/*Cn'
    s = key.lower().encode('utf-8')
    f = data.encode('utf-8')
    hmac_sha256 = hmac.new(f, digestmod=hashlib.sha256)
    hmac_sha256.update(s)
    digest = hmac_sha256.hexdigest()
    return digest

def getHeaders(method, token, url):
    nonce = createNonce()
    time = str(datetime.now().timestamp()).split('.')[0]

    if token == None or token == '':
        headers = {
            "api-key": PICA_API_KEY,
            "accept": "application/vnd.picacomic.com.v1+json",
            "app-channel": "2",
            "time": time,
            "nonce": nonce,
            "signature": createSignature(url, nonce, time, "POST"),
            "app-version": PICA_APP_VERSION,
            "app-uuid": genUUID(),
            "app-platform": "android",
            "app-build-version": PICA_APP_BUILD_VERSION,
            "Content-Type": "application/json; charset=UTF-8",
            "User-Agent": "okhttp/3.8.1",
            "version": PICA_VERSION,
            "Host": "picaapi.picacomic.com"
        }
    else:
        headers = {
            "api-key": PICA_API_KEY,
            "authorization": token,
            "accept": "application/vnd.picacomic.com.v1+json",
            "app-channel": "2",
            "time": time,
            "nonce": nonce,
            "signature": createSignature(url, nonce, time, method),
            "app-version": PICA_APP_VERSION,
            "app-uuid": genUUID(),
            "image-quality":"original",
            "app-platform": "android",
            "app-build-version": PICA_APP_BUILD_VERSION,
            "Content-Type": "application/json; charset=UTF-8",
            "User-Agent": "okhttp/3.8.1",
            "version": PICA_VERSION,
            "Host": "picaapi.picacomic.com"
        }
    return headers