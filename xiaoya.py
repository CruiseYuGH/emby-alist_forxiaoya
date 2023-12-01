# -*- coding: utf-8 -*-
##echo "zx9876541" | sudo -S chmod 777 -R /volume1/docker/xiaoya_media/xiaoya/同步更新/
from webdav3.client import Client
import os
import time
import requests
import shutil

def list_files(client, path="/"):
    all_files = []
    #wenjian = []
    q = 1
    print(path)
    while 1:
            try:
                # 获取WebDAV服务器上的文件列表
                files = client.list(path)
            except Exception as e:

                print(f'连接失败，{q}秒后重试... 错误信息: {e}')
                time.sleep(q)
                q += 1
                if q > 120:
                        break
            else:
                #print('重连成功...')
                break

    for _file in files:
        full_path = os.path.join(path,_file)#f"{path}/{file}"
        if _file[-1] == '/':
            # 如果是目录，则递归获取该目录下的所有文件
            subdirectory_files = list_files(client, full_path)
            all_files.extend(subdirectory_files)
        else:
            all_files.append(full_path)
    return all_files

def delete_local_folders(local_path, webdav_folders):
    # 获取本地目录下的所有文件夹
    local_folders = [f for f in os.listdir(local_path) if os.path.isdir(os.path.join(local_path, f))]
    
    # 找到本地多余的文件夹并删除
    for folder in local_folders:
        if folder + "/" not in webdav_folders:
            folder_path = os.path.join(local_path, folder)
            print(f"删除本地文件夹: {folder_path}")
            try:
                shutil.rmtree(folder_path)
            except Exception as e:
                print(f"删除文件夹失败: {folder_path}, 错误信息: {e}")


if __name__ == "__main__":
    webdav_url = 'http://192.168.5.216:5678/'
   
    username = 'guest'
    password = 'guest_Api789'
    options = {
        'webdav_hostname': webdav_url,
        'webdav_login': username,
        'webdav_password': password,
        'webdav_root': r"/"
    }
    client = Client(options)
    client.webdav.disable_check = True
    # 获取文件列表
    for xiaoya_dir in ["同步更新","每日更新/电影/中国/","每日更新/电影/欧美/"]:
        if xiaoya_dir== "同步更新":
            save_mulu = '/volume1/docker/xiaoya_media/xiaoya/同步更新/'
            webdav_url = "/dav/电视剧/中国/同步更新中/"
        #if xiaoya_dir== "每日更新/电影/中国/":
        #    save_mulu = '/volume1/docker/xiaoya_media/xiaoya/每日更新/电影/中国/'
        #    webdav_url = "/dav/每日更新/电影/中国/"
        #elif xiaoya_dir== "每日更新/电影/欧美/":
        #    save_mulu = '/volume1/docker/xiaoya_media/xiaoya/每日更新/电影/欧美/'
        #    webdav_url = "/dav/每日更新/电影/欧美/"
        #elif xiaoya_dir== "每日更新/电视剧/国产剧/":
        #    save_mulu = '/volume1/docker/xiaoya_media/xiaoya/每日更新/电视剧/国产剧/'
        #    webdav_url = "/dav/每日更新/电视剧/国产剧/"
        else:
            continue
        #l_0, l_1 = list_files(client,webdav_url)
        #print(l_0)
        #print(l_1)
        #if xiaoya_dir== "同步更新":# 删除本地多余文件夹
        #    delete_local_folders(save_mulu, l_0)
        wenjian_all = list_files(client,webdav_url)

        for b in wenjian_all:
            file_extension = os.path.splitext(b)[-1].upper()
            if file_extension in ['.MP4', '.MKV', '.FLV', '.AVI']:
                strm_file_path = os.path.join(save_mulu, b.replace(webdav_url, '')[:-3] + 'strm')
                #print(save_mulu, b.replace(webdav_url, '')[:-3] + 'strm',strm_file_path)
                #break
                if not os.path.exists(strm_file_path):
                    print('正在处理：' + b.replace(webdav_url, ''))
                    print(strm_file_path)
                    try:
                        os.makedirs(os.path.dirname(strm_file_path), exist_ok=True)
                        with open(strm_file_path, "w", encoding='utf-8') as f:
                            f.write('http://192.168.5.216:4567'+b.replace('/dav', '/d').replace(' ', '%20'))
                    except Exception as e:
                        print(f"{b.replace(webdav_url, '')}处理失败，错误信息: {e}")
            elif file_extension in ['.ASS', '.SRT', '.SSA']:
                srt_file_path = os.path
