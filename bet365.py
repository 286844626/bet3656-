# coding:utf-8
import re
import sys
import time
import execjs
import os
import requests
from autobahn.twisted.websocket import connectWS, WebSocketClientFactory, WebSocketClientProtocol

from autobahn.websocket.compress import (
    PerMessageDeflateOffer,
    PerMessageDeflateResponse,
    PerMessageDeflateResponseAccept,
)
from autobahn.twisted.util import sleep
from twisted.protocols.policies import TimeoutMixin
from twisted.python import log
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet import reactor, ssl
from twisted.internet.protocol import ReconnectingClientFactory
# ReconnectingClientFactory.maxDelay = 10
# ReconnectingClientFactory.clock=10
# ReconnectingClientFactory.delay=10
# ReconnectingClientFactory.resetDelay()
from txaio import start_logging, use_twisted

datagramRecieved = True
timeout = 30.0 # One second

def proxy(req):
    tunnel = "tps176.kdlapi.com:15818"

    # 用户名密码方式
    username = "t10143317794250"
    password = "2jqjjhhy"
    proxies = {
        "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel},
        "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
    }

    req.proxies=proxies


def decryptToken(t):
    n = ""
    i = ""
    o = len(t)
    r = 0
    s = 0
    MAP_LEN = 64
    charMap = [["A", "d"], ["B", "e"], ["C", "f"], ["D", "g"], ["E", "h"], ["F", "i"], ["G", "j"], ["H", "k"], ["I", "l"], ["J", "m"], ["K", "n"], ["L", "o"], ["M", "p"], ["N", "q"], ["O", "r"], ["P", "s"], ["Q", "t"], ["R", "u"], ["S", "v"], ["T", "w"], ["U", "x"], ["V", "y"], ["W", "z"], ["X", "a"], ["Y", "b"], ["Z", "c"], ["a", "Q"], ["b", "R"], ["c", "S"], ["d", "T"], ["e", "U"], ["f", "V"], [
        "g", "W"], ["h", "X"], ["i", "Y"], ["j", "Z"], ["k", "A"], ["l", "B"], ["m", "C"], ["n", "D"], ["o", "E"], ["p", "F"], ["q", "0"], ["r", "1"], ["s", "2"], ["t", "3"], ["u", "4"], ["v", "5"], ["w", "6"], ["x", "7"], ["y", "8"], ["z", "9"], ["0", "G"], ["1", "H"], ["2", "I"], ["3", "J"], ["4", "K"], ["5", "L"], ["6", "M"], ["7", "N"], ["8", "O"], ["9", "P"], ["\n", ":|~"], ["\r", ""]]
    for r in range(0, o):
        n = t[r]
        for s in range(0, MAP_LEN):
            if ":" == n and ":|~" == t[r:3]:
                n = "\n"
                r = r + 2
                break
            if n == charMap[s][1]:
                n = charMap[s][0]
                break
        i = i+n
    return i
def get_token():
    head = """
       function aaa () {
           const jsdom = require("jsdom");
           const { JSDOM } = jsdom;
           const dom = new JSDOM(`<!DOCTYPE html><p>Hello world</p>`);
           window = dom.window;
           document = window.document;
           XMLHttpRequest = window.XMLHttpRequest;
           location=window.Location;
           navigator=window.navigator;
           var ue=[];
           var de=[];
           var gh=(function() {
                           var e = 0
                             , t = 0
                             , n = 0;
                           return function(o) {
                               e > 0 && e % 2 == 0 && (2 > t ? ue[t++] = o : 3 > n && (de[n++] = o)),
                               e++
                           }
                       })();
       """
    tail = 'return [ue,de];}'
    a = requests.get("https://www.365-868.com/")
    # print(a.text)
    js = head + a.text.split("(boot||(boot={}));(function(){")[1].split('''</script>''')[0][:-6] + tail
    # print(js)
    e = execjs.compile(js.replace("boot['gh']", 'gh'), cwd=r'C:\Users\X6TI\AppData\Roaming\npm\node_modules')
    res = e.call('aaa')
    res[0].append('.')
    token1 = ''
    for i in res:
        for j in i:
            token1 += j

    return decryptToken(token1)

# use_twisted()

# start_logging(level='debug')
log.startLogging(sys.stdout)
occurred_eventids = []
checklist = {}
language = 'cn'  # en or cn
sport_type = 'football'  # football or basketball

HEADERS = {
    'Cookie': 'rmbs=3; aps03=cf=N&cg=2&cst=0&ct=42&hd=N&lng=10&oty=2&tzi=27; session=processform=0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'
}

PROTOCOLS = ['zap-protocol-v1']
URL_WSS = 'wss://premws-pt3.365lpodds.com/zap/'
URL_SESSION_ID = 'https://www.365-868.com/defaultapi/sports-configuration'
URL_NST_TOKEN = 'https://www.365-868.com/'

# 发送指令参数
req=requests.session()
# proxy(req)

token=get_token()
print(token)

D_NST_TOKEN = token#token2
COMMAND_TOKEN = ''
OVM21_TOKEN = ''
GET_MATCH_TOKEN = 'qoFYVl'

# 初始化
ODATA = {}
EV = {}

# bytes
_ENCODINGS_NONE = u'\x00'
_DELIMITERS_RECORD = u'\x01'
_DELIMITERS_FIELD = u'\x02'
_DELIMITERS_HANDSHAKE = u'\x03'
_DELIMITERS_MESSAGE = u'\x08'

_TYPES_TOPIC_LOAD_MESSAGE = u'\x14'
_TYPES_DELTA_MESSAGE = u'\x15'
_TYPES_SUBSCRIBE = u'\x16'
_TYPES_PING_CLIENT = u'\x19'
_TYPES_TOPIC_STATUS_NOTIFICATION = u'\x23'

_MAP_LEN = 64
_charMap = [
    ["A", "d"], ["B", "e"], ["C", "f"], ["D", "g"], ["E", "h"], ["F", "i"], ["G", "j"],
    ["H", "k"], ["I", "l"], ["J", "m"], ["K", "n"], ["L", "o"], ["M", "p"], ["N", "q"], ["O", "r"],
    ["P", "s"], ["Q", "t"], ["R", "u"], ["S", "v"], ["T", "w"], ["U", "x"], ["V", "y"], ["W", "z"],
    ["X", "a"], ["Y", "b"], ["Z", "c"], ["a", "Q"], ["b", "R"], ["c", "S"], ["d", "T"], ["e", "U"],
    ["f", "V"], ["g", "W"], ["h", "X"], ["i", "Y"], ["j", "Z"], ["k", "A"], ["l", "B"], ["m", "C"],
    ["n", "D"], ["o", "E"], ["p", "F"], ["q", "0"], ["r", "1"], ["s", "2"], ["t", "3"], ["u", "4"],
    ["v", "5"], ["w", "6"], ["x", "7"], ["y", "8"], ["z", "9"], ["0", "G"], ["1", "H"], ["2", "I"],
    ["3", "J"], ["4", "K"], ["5", "L"], ["6", "M"], ["7", "N"], ["8", "O"], ["9", "P"],
    ["\n", ":|~"], ["\r", ""]
]


def toJson(string):
    try:
        dic = {}
        data = string[:-1].split(';')
        for item in data:
            arr = item.split('=')
            dic[arr[0]] = arr[1]
    except Exception as e:
        # print(e)
        pass
    return dic


def dataParse(self, string):
    inPlayDatas = string.split('|CL;')
    footballDatas = ""
    basketballDatas = ""
    if len(inPlayDatas) >= 2:
        # soccerDatas = inPlayDatas[1]
        for inPlayData in inPlayDatas:
            if 'ID=1;' in inPlayData and 'CD=1;' in inPlayData:
                footballDatas = inPlayData
            elif 'ID=18;' in inPlayData:
                basketballDatas = inPlayData
    else:
        return  # End generator
    if sport_type == 'football':
        sportDatas = footballDatas
    elif sport_type == 'basketball':
        sportDatas = basketballDatas
    else:
        sportDatas = ''

    competitions = sportDatas.split('|CT;')
    if len(competitions) > 0:
        competitions = competitions[1:]
    else:
        competitions = []
    for comp in competitions:
        data = comp.split('|EV;')
        league = toJson(data[0]).get('NA')
        for item in data[1:]:
            MA = toJson(item.split('|MA;')[0])
            eventid = MA['ID'][:8]
            score = MA['SS']
            # print(item.split('|MA;')[0])
            PA0 = item.split('|PA;')[0]
            PA0Json = toJson(PA0)
            TU = PA0Json['TU']
            TT = int(PA0Json['TT'])
            TS = int(PA0Json['TS'])
            TM = int(PA0Json['TM'])
            begints = time.mktime(time.strptime(TU, '%Y%m%d%H%M%S'))
            nowts = time.time() - 8 * 60 * 60
            # The match has not started. TT=0 means the match has not started or paused, TM=45 means in the midfield.
            if TM == 0 and TT == 0:
                retimeset = '00:00'
            else:
                if TT == 1:
                    retimeset = str(int((nowts - begints) / 60.0) + TM) + \
                                ':' + str(int((nowts - begints) % 60.0)).zfill(2)
                else:
                    retimeset = '45:00'
            details = item.split('|PA;')[1:]
            if len(details) >= 2:
                hometeam = toJson(details[0]).get('NA')
                awayteam = toJson(details[1]).get('NA')
            else:
                hometeam = ''
                awayteam = ''
            yield league, hometeam, awayteam, score, retimeset, eventid
    time.sleep(3)
    # if language == 'en':  # English
    #     req = u'\x16\x00CONFIG_1_3,OVInPlay_1_3,Media_L1_Z3,XL_L1_Z3_C1_W3\x01'.encode('utf-8')
    # elif language == 'cn':  # Chinese
    #     req = u'\x16\x00CONFIG_10_0,OVInPlay_10_0\x01'.encode('utf-8')
    # else:
    #     req = ''
    # self.sendMessage(req)
    return


@inlineCallbacks
def search(league, hometeam, awayteam, score, retimeset, eventid):
    yield sleep(0.3)
    global occurred_eventids
    global checklist
    occurred_eventids.append(eventid)
    checklist[eventid] = {
        'league': league,
        'hometeam': hometeam,
        'awayteam': awayteam,
        'score': score,
        'retimeset': retimeset
    }
    print(league, hometeam, awayteam, score, retimeset, eventid)
    req = u'\x16\x006V{}C1A_10_0\x01'.format(eventid).encode('utf-8')
    returnValue(req)


class MyClientProtocol(WebSocketClientProtocol):
    @inlineCallbacks
    def subscribeGames(self, msg):
        for league, hometeam, awayteam, score, retimeset, eventid in dataParse(self, msg):
            try:
                req = yield search(league, hometeam, awayteam, score, retimeset, eventid)
            except Exception as e:
                print('error!')
                print(e)
                self.sendClose(100)
            else:

                self.sendMessage(req)

    def updateGameData(self, msg):
        for m in msg.split('|\x08'):
            d = m.split('\x01U|')
            IT = d[0].replace('\x15', '')
            if len(d) > 1 and IT in ODATA.keys():
                dic = toJson(d[1])
                for k in dic.keys():
                    ODATA[IT][k] = dic[k]
                # print('update ', IT, dic)
        return

    def newGameDataParse(self, msg):
        data = msg.split('|')
        EVC = {}
        MGC = {}
        MAC = {}
        MAC['PA']=[]
        EVC["ST"] = []
        for item in data:
            if item.startswith('EV;'):
                dic = toJson(item[3:])
                IT = dic.get('IT')
                ODATA[IT] = dic
                EVC = dic
                EVC["ST"] = []
                EVC["MG"] = []
                EV[EVC["FI"]] = EVC
            if item.startswith('ST;'):
                dic = toJson(item[3:])
                EVC["ST"].append(dic)
                IT = dic.get('IT')
                ODATA[IT] = dic
            if (item.startswith('MG;')):
                MGC = toJson(item[3:])
                EVC["MG"].append(MGC)
                MGC["MA"] = []
                IT = dic.get('IT')
                ODATA[IT] = MGC
            if (item.startswith('MA;')):
                MAC = toJson(item[3:])
                MGC["MA"].append(MAC)
                MAC["PA"] = []
                IT = dic.get('IT')
                ODATA[IT] = MAC
            if (item.startswith('PA')):
                dic = toJson(item[3:])
                MAC["PA"].append(dic)
                IT = dic.get('IT')
                ODATA[IT] = dic
        print({'data':EV})

        import json
        req.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",}
        f=req.post("http://123.57.142.178:1234/updata" ,data=json.dumps({'data':EV}))#123.57.142.178
        print(f.status_code)
        # exit()
        # print(ODATA)

    def sendMessage(self, message):
        print("Send: ", message)
        super().sendMessage(message)

    def onOpen(self):
        req = str('\x23\x03P\x01__time,S_{},D_{}\x00'.format(self.factory.session_id, D_NST_TOKEN)).encode('utf-8')
        self.sendMessage(req)

    @inlineCallbacks
    def onMessage(self, payload, isBinary):

        msg = payload.decode('utf-8')
        datagramRecieved=msg
        print('on Message:' + msg)


        if msg.startswith('100'):
            if language == 'en':  # English
                connectReq = u'\x16\x00CONFIG_1_3,OVInPlay_1_3,Media_L1_Z3\x01'.encode('utf-8')
            elif language == 'cn':  # Chinese
                connectReq = u'\x16\x00CONFIG_10_0,OVInPlay_10_0\x01'.encode('utf-8')
            else:
                connectReq = ''
            self.sendMessage(connectReq)

            # commandReq = str('\x02\x00command\x01nst\x01{}\x02SPTBK'.format(COMMAND_TOKEN)).encode('utf-8')
            # self.sendMessage(commandReq)
            return

        if msg.find('__time') == 1:
            return

        if msg.find('CONFIG_') == 1:
            getMatchReq = str('\x16\x00{}\x01'.format(GET_MATCH_TOKEN)).encode('utf-8')
            self.sendMessage(getMatchReq)
            ovmReq = str('\x16\x00{}M1_1,6v93894836C1A_10_0\x01'.format(OVM21_TOKEN)).encode('utf-8')
            self.sendMessage(ovmReq)
            return

        if language == 'en':  # English
            msg_header = 'OVInPlay_1_3'
        elif language == 'cn':  # Chinese
            msg_header = 'OVInPlay_10_0'

        if msg_header in msg:
            # print(55)
            yield self.subscribeGames(msg)
        else:
            matched_id1 = msg.split('F|EV;')[0][-17:-9]
            matched_id2 = msg.split('F|EV;')[0][-16:-8]

            if matched_id1 not in occurred_eventids and matched_id2 not in occurred_eventids:

                self.updateGameData(msg)
            else:
                self.newGameDataParse(msg)


class MyFactory(WebSocketClientFactory, ReconnectingClientFactory):

    maxDelay = 5
    maxRetries = 5

    def startedConnecting(self, connector):
        print('Started to connect.')
    def clientConnectionFailed(self, connector, reason):
        print('failed retry!')
        self.retry(connector)
    def clientConnectionLost(self, connector, reason):#与主机失去连接
        print('lost retry!')
        self.retry(connector)

# 获取session_id
def get_session_id():
    req=requests.session()
    proxy(req)
    response = req.get(url=URL_SESSION_ID, headers=HEADERS)

    # print(response.text)
    session_id = response.cookies['pstk']
    # print(session_id)
    return session_id



# UDP code here

def testTimeout():
    global datagramRecieved
    if not datagramRecieved:
        reactor.retry()
    datagramRecieved = False


if __name__ == '__main__':
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"

    factory = MyFactory(
        URL_WSS, useragent=USER_AGENT, protocols=PROTOCOLS)

    factory.protocol = MyClientProtocol
    factory.headers = {}
    # nst_token = _get_nst_token()
    # factory.nst_token = 'IHiBXw==.p7RoMdzczpn70iG6dg77uROPHOB1IuNSQG5jGmlP7SI='
    factory.session_id = get_session_id()
    # print('session_id: '+factory.session_id)

    def accept(response):
        if isinstance(response, PerMessageDeflateResponse):
            return PerMessageDeflateResponseAccept(response)



    factory.setProtocolOptions(perMessageCompressionAccept=accept)
    factory.setProtocolOptions(serverConnectionDropTimeout=5,failByDrop=5)
    factory.setProtocolOptions(perMessageCompressionOffers=[PerMessageDeflateOffer(
        accept_max_window_bits=True,
        accept_no_context_takeover=True,
        request_max_window_bits=0,
        request_no_context_takeover=True,

    )])
    # reactor.callFromThread(connectWS, factory)
    # reactor.run()
    if factory.isSecure:
        contextFactory = ssl.ClientContextFactory()
    else:
        contextFactory = None
    connectWS(factory, contextFactory)
    # from twisted.internet import task
    # l = task.LoopingCall(testTimeout)
    # l.start(timeout)  # call every second
    # f=TimeoutMixin()
    # f.setTimeout(20)
    reactor.run()
