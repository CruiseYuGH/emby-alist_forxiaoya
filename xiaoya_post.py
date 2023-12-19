# -*- coding: utf-8 -*-
import time
import requests
import json
import os
import re
def get_token(url_input, alist_username, alist_password):
    url = "{}/api/auth/login".format(url_input)
    
    payload = json.dumps({
       "username": "{}".format(alist_username),
       "password": "{}".format(alist_password)
    })
    headers = {
       'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
       'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    result = response.json()
    print(result)
    if result["code"] != 200:
        print("None")
        return None
    return result.get('data', {}).get('token', None)


def get_files_list(url_input, alist_token,base_path="/"):
    
    files_list = []
    url = "{}/api/fs/list".format(url_input)

    payload = json.dumps({
       "path": "{}".format(base_path),
       "password": "",
       "page": 1,
       "per_page": 0,
       "refresh": False
    })
    headers = {
       'Authorization': ''.format(alist_token),
       'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
       'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    sleep_time = 1
    while response.status_code != 200 or "无法显示目录下文件，请刷新重试" in json.loads(response.content.decode('utf-8'))['message']:
        time.sleep(sleep_time*0.2)
        sleep_time +=1
        response = requests.request("POST", url, headers=headers, data=payload)
        print(f"Failed to retrieve files. Error: {base_path}")
        if sleep_time >60:
            return []
        
    json_data = json.loads(response.content.decode('utf-8'))
    
    if "data" not in json_data.keys() or json_data["data"]  is  None:
        print("None 1 for {}".format(base_path))
        print(json_data['message'])
        return []
    #print(json_data["data"].__class__)
    if "content" not in json_data["data"].keys():
        print("None 2 for {}".format(base_path))
        return []
    content = json_data["data"]["content"]
    if content is None:
        print("None 3 for {}".format(base_path))
        return []
    for item in content:
      if item["is_dir"]:
        # 如果是文件夹，递归获取文件夹内文件
        sub_path = os.path.join(base_path,item['name'])#f"{base_path}/{item['name']}"
        files_list.extend(get_files_list(url_input, alist_token, sub_path))
      else:
        # 如果是文件，添加到文件列表
        files_list.append(os.path.join(base_path,item['name']))
    return files_list

def replace_substrings(input_string):
    # 使用正则表达式匹配 "/A " 到 "/Z "，并替换成 "/"
    result = re.sub(r'/(A |B |C |D |E |F |G |H |I |J |K |L |M |N |O |P |Q |R |S |T |U |V |W |X |Y |Z )| 完结/', '/', input_string)
    return result
	
def cleanup_unmatched_files(directory_A_list, directory_B):
    # 获取目录 A 下的文件列表
    #files_A = set([os.path.join(save_mulu, replace_substrings(b).replace(webdav_url, '')[1:-4].replace("电视剧/中国/同步更新中/", '同步更新/')) for b in directory_A_list])
    files_A = set([replace_substrings(os.path.join(save_mulu, os.path.relpath(b, start= url_path)[:-4])) for b in directory_A_list])
    #print(list(files_A)[0])
    #exit()
    # 遍历目录 B 下的所有文件夹
    for root, dirs, files in os.walk(directory_B, topdown=False):
        for file in files:
            if file in ["season.nfo","tvshow.nfo"]:
                continue
            # 获取文件的相对路径
            relative_path = os.path.relpath(os.path.join(root, file), directory_B)

            # 构建文件的完整路径
            file_path = os.path.join(directory_B, relative_path)

            # 检查文件是否为 strm 或 nfo 格式
            if file.endswith(('.strm', '.nfo')):
                # 提取文件名（不包括后缀）以检查匹配
                file_name_without_extension = os.path.splitext(file)[0]

                # 构建对应的 strm 文件名
                strm_file_name = file_name_without_extension + '.strm'

                ## 构建对应的 nfo 文件名
                #nfo_file_name = file_name_without_extension + '.nfo'

                # 检查 strm 文件和 nfo 文件是否都存在于目录 A
                strm_exists_in_A = file_path.replace(".strm","").replace(".nfo","")  in files_A
                #nfo_exists_in_A = nfo_file_name in files_A
                #print(strm_exists_in_A,strm_file_name,file,file_path[:-5],list(files_A)[0])
                #exit()
                # 如果 strm 文件或 nfo 文件不在目录 A 中，则删除它们
                if not strm_exists_in_A:
                    print(f"Deleting: {file_path}")
                    #os.remove(file_path)  
import shutil

def delete_directory_if_no_strm(directory_path):
    # 检查目录及其子目录是否包含 .strm 文件
    has_strm_files = any(
        file.endswith('.strm') 
        for root, dirs, files in os.walk(directory_path)
        for file in files
    )

    # 如果目录及其子目录下没有 .strm 文件，则删除整个目录
    if not has_strm_files:
        print(f"Deleting directory: {directory_path}")
        try:
            shutil.rmtree(directory_path)
        except OSError as e:
            print(f"Error deleting directory {directory_path}: {e}")
    else:
        # 如果有 .strm 文件，递归检查子目录
        for root, dirs, files in os.walk(directory_path):
            for sub_dir in dirs:
                sub_dir_path = os.path.join(root, sub_dir)
                delete_directory_if_no_strm(sub_dir_path)
# Get the token
webdav_url = 'http://192.168.5.216:4567'
username = 'guest'
password = 'guest_Api789'
alist_token = get_token(webdav_url, username, password)

# Use the token in subsequent requests
#url_path = "/电视剧/中国/同步更新中/"
#save_mulu = '/volume1/docker/xiaoya_media/xiaoya/同步更新/'
# save_mulu 小雅网址下的相对路径
# url_path 本地存储的绝对路径

if alist_token:
    for xiaoya_dir in ["同步更新", "每日更新/电影/中国/", "每日更新/电影/欧美/", "每日更新/电影/日本/", "每日更新/电影/韩国/"]:
        if xiaoya_dir== "同步更新":
            save_mulu = '/volume1/docker/xiaoya_media/xiaoya/同步更新/'
            url_path = "/电视剧/中国/同步更新中/"
        elif xiaoya_dir== "每日更新/电影/中国/":
            save_mulu = '/volume1/docker/xiaoya_media/xiaoya/每日更新/电影/中国/'
            url_path = "/每日更新/电影/中国/"
        elif xiaoya_dir== "每日更新/电影/欧美/":
            save_mulu = '/volume1/docker/xiaoya_media/xiaoya/每日更新/电影/欧美/'
            url_path = "/每日更新/电影/欧美/"
        elif xiaoya_dir== "每日更新/电影/日本/":
            save_mulu = '/volume1/docker/xiaoya_media/xiaoya/每日更新/电影/日本/'
            url_path = "/每日更新/电影/日本/"
        elif xiaoya_dir== "每日更新/电影/韩国/":
            save_mulu = '/volume1/docker/xiaoya_media/xiaoya/每日更新/电影/韩国/'
            url_path = "/每日更新/电影/韩国/"
        else:
            continue
        # 调用函数并打印结果
        files = get_files_list(webdav_url,alist_token,url_path)
        
        # 自己手动决定是否开启，清理废弃的本地的视频文件
        #if xiaoya_dir== "同步更新" and False:
            # 根据小雅的线上url 清理本地的视频文件
            #cleanup_unmatched_files(files,os.path.join(save_mulu))
            # 查看小雅本地的目录，弱不存在视频文件则删除
            #delete_directory_if_no_strm(os.path.join(save_mulu))
        for b in files:
            #print(b)
            file_extension = os.path.splitext(b)[-1].upper()
            if file_extension in ['.MP4', '.MKV', '.FLV', '.AVI']:
                for_save_path =  os.path.relpath(b, start= url_path)
                strm_file_path = replace_substrings(os.path.join(save_mulu, for_save_path[:-3] + 'strm'))
                if not os.path.exists(strm_file_path):
                    print('正在处理：' + b.replace(webdav_url, ''))
                    print(strm_file_path)
                    try:
                        os.makedirs(os.path.dirname(strm_file_path), exist_ok=True)
                        with open(strm_file_path, "w", encoding='utf-8') as f:
                            f.write('http://192.168.5.216:4567/d'+b.replace(' ', '%20'))
                    except Exception as e:
                        print(f"{b.replace(webdav_url, '')}处理失败，错误信息: {e}")
        sleep(30)
