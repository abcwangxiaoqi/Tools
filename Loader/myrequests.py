import queue
import threading
from Loader import requestClasses
import uuid
import time

__loopExist = False

__queueLock = threading.Lock()
__reqQueue = queue.Queue()
__cbMap = {}
__threads = []

def init(threadNum=3):

    global __loopExist

    if __loopExist == True :
        print('已经初始化过，没必要再次初始化')
        return

    __loopExist = True

    for i in range(threadNum):
        channel = threading.Thread(target=__Loop)
        __threads.append(channel)

    for t in __threads:
        t.start()

    return

def __Loop():
    while __loopExist == True :
        time.sleep(1)
        if __queueLock.acquire():
            if __reqQueue.empty() == False :
                req = __reqQueue.get()
                req.Run()

                if __cbMap.get(req.id) != None:
                    __cbMap.get(req.id)(req)
            __queueLock.release()
    return

def __getid():
    return uuid.uuid1()

def Get(url,callback=None,params=None, **kwargs):

    id = __getid()

    if callback!= None :
        __cbMap[id]=callback

    req = requestClasses.Get(id,url,params,**kwargs)
    __reqQueue.put(req)

    return

def Post(url,callback=None, data=None, json=None, **kwargs):
    id = __getid()

    if callback != None:
        __cbMap[id] = callback

    req = requestClasses.Post(id,url,data,json,**kwargs)
    __reqQueue.put(req)
    return

def GetMultiDown(url,callback=None,threadNum = 2,params=None, **kwargs):
    id = __getid()

    if callback != None:
        __cbMap[id] = callback

    req = requestClasses.GetMultiDown(id, url,threadNum, params, **kwargs)
    __reqQueue.put(req)
    return

def PostMultiDown( url,callback=None,threadNum = 2, data=None, json=None, **kwargs):
    id = __getid()

    if callback != None:
        __cbMap[id] = callback

    req = requestClasses.PostMultiDown(id, url,threadNum, data,json, **kwargs)
    __reqQueue.put(req)
    return


def Stop():
    global __loopExist
    __loopExist = False
    return

def Running():
    return __loopExist


'''

def cb(reponse):
    print(reponse.url)
    print(reponse.success)
    f = open('scene.zip','+wb')
    f.write(reponse.finalContent)
    f.close()
    return

init()
url = 'http://192.168.10.105:8090/file/zip/Scene_01.zip'
#url = 'http://127.0.0.1:5000/api/down/txt/1.txt'
GetMultiDown(url, cb,2, stream=True, timeout=5)
Stop()

'''
