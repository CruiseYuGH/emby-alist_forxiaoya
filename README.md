# emby-alist_forxiaoya
小雅emby 刮削后，定时爬取更新本地emby的文件系统

emby挂载alist媒体库

一、前提
配置好的Alist服务端和Emby服务端
Emby的strm文件应用参考：https://emby.media/support/articles/Strm-Files.html

二、总体思路
我们需要获取Alist服务器上指定目录下的视频文件名称、路径、播放链接，然后在Emby媒体库路径下生成相同的路径、文件名（后缀改为strm，内容为播放链接）的文本文件，同时也可以把字幕文件一起复制过来。效果如下图：

Alist文件
![Image text](https://github.com/CruiseYuGH/emby-alist_forxiaoya/blob/main/1.png)

群晖对应地址（Emby媒体库）
![Image text](https://github.com/CruiseYuGH/emby-alist_forxiaoya/blob/main/2.png)

ps：为了方便emby 能够获取root权限（高级设置中我们将UID和GID的用户数值修改为0，然后点击保存。（数字0代表root用户，如果介意的可以使用ssh工具登录群晖，在用户界面输入id即可获取对应用户的UID和GID值））
![Image text](https://github.com/CruiseYuGH/emby-alist_forxiaoya/blob/main/3.png)

需要修改 webdav_url 为你对应的IP +端口号
webdav_url = 'http://192.168.5.216:5678/' 

考虑到多个文件夹更新，save_mulu与webdav_url 需要对应配置：
本地保存位置：save_mulu = '/volume1/docker/xiaoya_media/xiaoya/同步更新/'
小雅 Alist上对应的位置：webdav_url = "/dav/电视剧/中国/同步更新中/"

生成strm的代码中的 'http://192.168.5.216:5678' 要对齐，我这里就懒得改了，你们手动配置下吧，（提醒下在strm 需要用"%20"替换空格）
f.write('http://192.168.5.216:5678'+b.replace('/dav', '/d').replace(' ', '%20'))
