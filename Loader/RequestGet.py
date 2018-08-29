import requests
from abc import ABCMeta,abstractmethod
import threading

class RequestGet:

    id = None
    __metaclass__ = ABCMeta

    def __init__(self,id,url,params=None,**kwargs):

        self.url = url
        self.params = params
        self.kwargs = kwargs
        self.id = id
        return

    @abstractmethod
    def Run(self):
        print(self.url)
        rep = requests.get(self.url,self.params,**self.kwargs)

        return rep

class multiDownResponse:

class MultiDown(RequestGet):

    def __init__(self, id, url,threadNum = 2, params=None, **kwargs):
        super().__init__(id,url,params,**kwargs)

        self.threadNum = threadNum

        if threadNum < 2:
            self.threadNum = 2

        self.Reponse = []

        return

    def __downPart(self,start,end,index):

        headers = {"Range": "bytes=%s-%s" % (start, end)}
        rep = requests.get(self.url, self.params, **self.kwargs,headers=headers)

        self.Reponse.insert(index,rep)
        return

    def Run(self):

        print(self.url)

        heads = requests.head(self.url).headers
        fileSize = int(heads['Content-Length'])
        everySize = int(fileSize/self.threadNum)

        start = [self.threadNum]
        end = [self.threadNum]

        for i in range(self.threadNum):
            if i + 1 == self.threadNum:
                start[i] = i * everySize
                end[i] = fileSize - 1
                continue
            start.insert(i,i * everySize)
            end.insert(i,(i + 1) * everySize - 1)

        threads = []
        for i in range(self.threadNum):
            t = threading.Thread(target=self.__downPart,args=[start[i],end[i],i])
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        finalContent = b'' #define bytes
        success = True

        for rep in self.Reponse:
            if rep.status_code != 206:
                success = False
                break
            finalContent += rep.content

        return self.url,success,finalContent
'''
kwargs = {'11':'22','33':'44'}

keys = kwargs.keys()
args = str
for k in keys:
    args.append( str.format('{0}={1}&', k, kwargs[k]))

args = args[:-1]

print(args)
'''

'''
m = []
m.insert(1,2)
m.insert(0,1)
print(m)
'''