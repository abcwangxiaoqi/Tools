
import threading

__fileLock = threading.Lock()

def __writefile(file,start,end,content):

    if __fileLock.acquire():
        f = open(file,'wb')
        f.seek(start)
        f.write(content[start:end+1])
        f.close()
        __fileLock.release()

    return

def MultiThreadWrite(file,content,threadNum = 2):

    if threadNum < 2 :
        threadNum = 2

    fileSize = len(content)
    everySize = int(fileSize / threadNum)

    threads = []
    start = [threadNum]
    end = [threadNum]

    for i in range(threadNum):
        if i + 1 == threadNum:
            start[i] = i * everySize
            end[i] = fileSize - 1
            continue
        start.insert(i, i * everySize)
        end.insert(i, (i + 1) * everySize - 1)

    for n in range(threadNum):
        t = threading.Thread(target=__writefile,args=[file,start[n],end[n],content])
        threads.append(t)

    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()

    return

def writefile(file,content):

    f = open(file, 'wb')
    f.write(content)
    f.close()

    return
