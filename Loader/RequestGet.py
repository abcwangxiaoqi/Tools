import requests
from abc import ABCMeta,abstractmethod
import threading

class Request:

    __metaclass__ = ABCMeta

    reponse = None
    id = None
    url = None

    def __init__(self,id,url):
        self.id = id
        self.url = url


    @abstractmethod
    def Run(self):
        return

class RequestGet(Request):

    def __init__(self,id,url,params=None,**kwargs):

        super().__init__(id,url)

        self.params = params
        self.kwargs = kwargs

        return

    def Run(self):

        self.reponse = requests.get(self.url,self.params,**self.kwargs)

        return

class RequestPost(Request):
    def __init__(self,id,url, data=None, json=None, **kwargs):
        super().__init__(id,url)
        self.data = data
        self.json = json
        self.kwargs = kwargs
        return

    def Run(self):

        self.reponse = requests.post(self.url,self.data,self.json,**self.kwargs)

        return





class MultiDown:

    __metaclass__ = ABCMeta
    threadReponses = None
    finalContent = b''
    success = True

    def __init__(self,threadNum = 2):

        self.threadNum = threadNum

        if threadNum < 2:
            self.threadNum = 2

        self.threadReponses = []
        return

    @abstractmethod
    def __down(self,start,end,index):
        return

    def multiThreadRun(self):

        heads = requests.head(self.url).headers
        fileSize = int(heads['Content-Length'])
        everySize = int(fileSize / self.threadNum)

        start = [self.threadNum]
        end = [self.threadNum]

        for i in range(self.threadNum):
            if i + 1 == self.threadNum:
                start[i] = i * everySize
                end[i] = fileSize - 1
                continue
            start.insert(i, i * everySize)
            end.insert(i, (i + 1) * everySize - 1)

        threads = []
        for i in range(self.threadNum):
            t = threading.Thread(target=self.__down, args=[start[i], end[i], i])
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        #self.finalContent = b''  # define bytes
        #self.success = True

        for rep in self.threadReponses:
            if rep.status_code != 206:
                success = False
                break
            self.finalContent += rep.content

        return

class MultiGetDown(Request,MultiDown):

    def __init__(self, id, url,threadNum = 2, params=None, **kwargs):

        MultiDown.__init__(self,threadNum)
        Request.__init__(self,id,url)

        self.params = params
        self.kwargs = kwargs

        return

    def __down(self,start,end,index):

        headers = {"Range": "bytes=%s-%s" % (start, end)}
        rep = requests.get(self.url, self.params, **self.kwargs,headers=headers)

        self.threadReponses.insert(index,rep)
        return

class MultiPostDown(Request,MultiDown):

    def __init__(self, id, url,threadNum = 2, data=None, json=None, **kwargs):

        MultiDown.__init__(self,threadNum)
        Request.__init__(self,id,url)

        self.data = data
        self.json = json
        self.kwargs = kwargs

        return

    def __down(self,start,end,index):

        headers = {"Range": "bytes=%s-%s" % (start, end)}

        rep = requests.post(self.url, self.data, self.json, **self.kwargs,headers = headers)

        self.threadReponses.insert(index,rep)

        return