# emby-alist_forxiaoya
小雅emby 刮削后，定时爬取更新本地emby的文件系统

emby挂载alist媒体库

一、前提
配置好的Alist服务端和Emby服务端
Emby的strm文件应用参考：https://emby.media/support/articles/Strm-Files.html

二、总体思路
我们需要获取Alist服务器上指定目录下的视频文件名称、路径、播放链接，然后在Emby媒体库路径下生成相同的路径、文件名（后缀改为strm，内容为播放链接）的文本文件，同时也可以把字幕文件一起复制过来。效果如下图：

Alist文件

本地文件（Emby媒体库）

三、优势和效果
这种方案最大的优势就是节省本地空间，而且比之前挂载的方法稳定，因为读取的就是本地文件，不会存在反复扫描的情况，设备重启后也不用担心掉盘或者需要重启Emby才能识别媒体库。 两千多个视频文件，空间占用只有几百KB：

