from Loader import *
from FileOperate import *

def cb(reponse):
    print(reponse.url)
    print(reponse.success)

    filewrite.MultiThreadWrite('scene.zip',reponse.finalContent)
    #filewrite.writefile('scene.zip',reponse.finalContent)

    #f = open('scene.zip','+wb')
    #f.write(reponse.finalContent)
    #f.close()

    return

myrequests.init()

#myrequests.Get(url,callbakc,params,kwargs)
#myrequests.Post(url,)

url = 'http://192.168.10.105:8090/file/zip/Scene_01.zip'
#url = 'http://127.0.0.1:5000/api/down/txt/1.txt'
myrequests.GetMultiDown(url, cb,2, stream=True, timeout=5)
myrequests.Stop()