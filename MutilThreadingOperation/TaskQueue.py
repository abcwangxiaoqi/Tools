'''
多线程操作类
自定义方法
'''

import queue
import threading
import time

# 任务队列
taskQueue = queue.Queue()
queueLock = threading.Lock()
initFlag = False
__threadItems = []

# 单个线程中 操作对象
class OperateItem:

    # 是否完成状态参数
    finished = False

    def __init__(self,func):

        # 操作方法
        self.actionFun = func

        return

    def Run(self):
        self.actionFun(self)
        return


class ThreadItem(threading.Thread):

    global taskQueue
    global queueLock

    __currentTask = None

    def __init__(self,threadid, *args, **kwargs):

        super(ThreadItem, self).__init__(*args,**kwargs)

        self.threadID = threadid
        self.__flag = threading.Event()  # 用于暂停线程的标识
        self.__flag.set()  # 设置为True
        self.__running = threading.Event()  # 用于停止线程的标识
        self.__running.set()  # 将running设置为True


        return

    def __getNew(self):

        # get new task
        if queueLock.acquire():
            if taskQueue.empty() == False:
                print ("thread %d : get new task" % self.threadID)
                self.__currentTask = taskQueue.get()
                self.__currentTask.Run()
            else:
                print ("thread %d : stop task" % self.threadID)
                self.pause()
            queueLock.release()

    def Loop(self):

        if self.__currentTask == None:
            self.__getNew()
        elif self.__currentTask.finished == True :
            self.__getNew()
        else:
            print("thread %d : wait one sec"%self.threadID)
            time.sleep(1)
        
        
        return

    def run(self):
        while self.__running.isSet():
            self.__flag.wait()      # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            #print(time.time())
            #time.sleep(1)
            self.Loop()

    def pause(self):
        self.__flag.clear()     # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()    # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()        # 设置为False


def init(threadNum=3):

    global initFlag
    global __threadItems

    if initFlag == True :
        print('已经初始化过，没必要再次初始化')
        return

    initFlag = True

    for i in range(threadNum):

        threaditem = ThreadItem(i)
        __threadItems.append(threaditem)
        threaditem.start()


def Add(operate):

    global initFlag

    if initFlag == False:
        print ("还没有实例化，请先实例化")
        return

    print ("add queue")

    taskQueue.put(operate)

    for th in __threadItems:
        th.resume()

    return

#回收所有线程
def Dispose():

    global initFlag

    if initFlag == False:
        return

    global __threadItems

    for th in __threadItems:
        th.stop()

    __threadItems = []
    initFlag = False

    return



#.......................测试.................................
'''
init(3)

def op1Action(item):
    print ("op1Action")
    time.sleep(1)
    item.finished = True
    return

def op2Action(item):
    print ("op2Action")
    time.sleep(1)
    item.finished = True
    return

def op3Action(item):
    print ("op3Action")
    time.sleep(1)
    item.finished = True
    return

op1 = OperateItem(op1Action)
op2 = OperateItem(op2Action)
op3 = OperateItem(op3Action)

Add(op1)
Add(op2)
Add(op3)

time.sleep(8)

# 停止
Dispose()
'''