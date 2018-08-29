import queue
import threading
import RequestGet
import uuid
import time

class MyRequests:

    threadNum = 3

    def __init__(self):

        self.loopExist = True

        self.queueLock = threading.Lock()
        self.reqQueue = queue.Queue()
        self.cbMap = {}
        self.threads = []

        for i in range(self.threadNum):
            channel = threading.Thread(target=self.Loop)
            self.threads.append(channel)

        for t in self.threads:
            t.start()

        return

    def Loop(self):
        while self.loopExist :
            time.sleep(1)
            if self.queueLock.acquire():
                if self.reqQueue.empty() == False :
                    req = self.reqQueue.get()
                    r = req.Run()

                    if self.cbMap.get(req.id) != None:
                        self.cbMap.get(req.id)(r)
                self.queueLock.release()
        return

    def __getid(self):
        return uuid.uuid1()

    def Get(self,url,callback=None,params=None, **kwargs):

        id = self.__getid()

        if callback!= None :
            self.cbMap[id]=callback

        req = RequestGet.RequestGet(id,url,params,**kwargs)
        self.reqQueue.put(req)

        return

    def Post(self):
        return

    def GetDown(self,url,callback=None,threadNum = 2,params=None, **kwargs):
        id = self.__getid()

        if callback != None:
            self.cbMap[id] = callback

        req = RequestGet.MultiDown(id, url,threadNum, params, **kwargs)
        self.reqQueue.put(req)
        return

    def PostDown(self):
        return

def cb(url,success,content):
    print(url)
    print(success)
    f = open('test.zip', "wb")
    f.write(content)
    f.close()

    return


mreq = MyRequests()
url = 'http://192.168.10.105:8090/file/zip/Scene_01.zip'
mreq.GetDown(url, cb,2, stream=True, timeout=5)
