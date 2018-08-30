## 记录python开发集成的工具，以便使用  

+ ***Loader*** 

**用于Http请求的工具，在requests库上进行二次封装**
1. 多线程处理下载任务
2. 多线程下载同一资源  

**使用方式：**  

```
#导入
from Loader import *

# 初始化 ，可传参数，参数为开启线程数，默认为3
myrequests.init(3)

#Get Post 比较与requests多了个回调，其他参数按照requests方式传递即可
myrequests.Get(url,callback,省略)
myrequests.Post(url,callback,省略)

#多线程下载资源 threadNum 同时下载启动线程数 Get Post
myrequests.GetMultiDown(url, callback,threadNum = 2, 省略)
myrequests.GetMultiDown(url, callback,threadNum = 2, 省略)

#停止
myrequests.Stop()

```  

+ ***FileOperate***  

**文件操作工具**  
1. 多线程写入文件 

**使用方法:**  
```

```  
**注意:** 对于请求网络数据，多线程可能能够提高效率，但是对于本地磁盘 IO 操作，多线程大部分时候反而会降低性能，原因在于机械硬盘写入数据时候磁头需要不断移动定位。