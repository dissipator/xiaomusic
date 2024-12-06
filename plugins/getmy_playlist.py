import requests,re,json

# 功能： 从网易云账号读取歌单，并生成播放url
# type: 歌单来源类型
# api_host： api服务器地址
# playlist_id： 歌单ID，uid：网易云账号用户id
# 落雪 source https://github.com/ZxwyWebSite/lx-source/releases/download/vv1.0.3.0622/lx-source-linux-amd64v2.zip
# f"{api_host}/song/url?id={music['id']}&br=350000&realIP=211.161.244.70&proxy=HTTP:%2F%2F127.0.0.1:8080"
# 此链接是使用了 UnblockNeteaseMusic 解锁灰色的 NeteaseMusicApi的播放链接 要使用此链接还需要在 httpserver.py 中做下修改：
# @app.get("/musicinfo")
# async def musicinfo(
#    name: str, musictag: bool = False, Verifcation=Depends(verification)
# ):
#    url = xiaomusic.get_music_url(name)
# +    if("song/url" in url):
# +        jsons = await downloadfile(url,"json")
# +        url = jsons['data'][0]['url']


async def getmy_playlist(type="netease",api_host="http://127.0.0.1:3000", playlist_ids=[],uid=None,br=128):
    """
    Purpose:
    """
    global log, xiaomusic
    if type == "netease":
        if uid:
            api_url = f"{api_host}/user/playlist?uid={uid}"
            # 发起请求
            response = requests.get(api_url, timeout=5)  # 增加超时以避免长时间挂起
            response.raise_for_status()  # 如果响应不是200，引发HTTPError异常
            # log.info(f"getmy_playlist url:{api_url} response:{response.text}")

            music_list = response.json()
            for item in music_list["playlist"]:
                list_name = item.get("name") + "-WY"

                log.info(f"getmy_playlist name:{list_name}")
                # if item.get("id") in [12709941656,]:
                songs_url = f"{api_host}/playlist/detail?id={item['id']}"
                # 发起请求
                response = requests.get(
                    songs_url, timeout=5
                )  # 增加超时以避免长时间挂起
                response.raise_for_status()  # 如果响应不是200，引发HTTPError异常
                # log.info(f"getmy_playlist url:{api_url} response:{response.text}")
                musics = response.json()
                one_music_list = []
                for music in musics["playlist"]["tracks"]:
                    if not music:
                        continue
                    # try:
                    name = music["name"]
                    picUrl = music["al"]["picUrl"]
                    artist = music["ar"][0]["name"]
                    album = music["al"]["name"]

                    name = music.get("name")
                    url = f"{api_host}/song/url?id={music['id']}&br={br}000&realIP=211.161.244.70&proxy=HTTP:%2F%2F127.0.0.1:8080"
                    if (not name) or (not url):
                        continue
                    xiaomusic.all_music[name] = url
                    xiaomusic.all_music_tags[name] = {
                        "title": name,
                        "artist": artist,
                        "album": album,
                        "year": "",
                        "genre": "",
                        "picture": picUrl,
                        "lyrics": "",
                    }

                    one_music_list.append(name)
                    log.debug(f"getmy_playlist name:{list_name}")
                log.debug(one_music_list)
                # 歌曲名字相同会覆盖
                xiaomusic.music_list[list_name] = one_music_list
                xiaomusic.try_save_tag_cache()
                log.debug(xiaomusic.all_music)
                log.debug(xiaomusic.music_list)
            return
        if playlist_ids:
            for playlist_id in playlist_ids:
                songs_url = f"{api_host}/playlist/detail?id={playlist_id}"
                # 发起请求
                response = requests.get(songs_url, timeout=5)  # 增加超时以避免长时间挂起
                response.raise_for_status()  # 如果响应不是200，引发HTTPError异常
                # log.info(f"getmy_playlist url:{api_url} response:{response.text}")
                musics = response.json()
                list_name = musics['playlist']['name']
                one_music_list = []
                for music in musics['playlist']['tracks']:
                    if (not music):
                        continue
                    # try:
                    name = music['name']
                    picUrl = music['al']['picUrl']
                    artist = music['ar'][0]['name']
                    album = music['al']['name']

                    name = music.get("name")
                    url = f"{api_host}/song/url?id={music['id']}&br={br}000&realIP=211.161.244.70&proxy=HTTP:%2F%2F127.0.0.1:8080"
                    if (not name) or (not url):
                        continue
                    xiaomusic.all_music[name] = url
                    xiaomusic.all_music_tags[name] =  {
                            "title": name,
                            "artist": artist,
                            "album": album,
                            "year": "",
                            "genre": "",
                            "picture": picUrl,
                            "lyrics": ""
                        }
                    one_music_list.append(name)
                log.debug(f"getmy_playlist name:{list_name}")
                log.debug(one_music_list)
                # 歌曲名字相同会覆盖
                xiaomusic.music_list[list_name] = one_music_list
                xiaomusic.try_save_tag_cache()
                log.debug(xiaomusic.all_music)
                log.debug(xiaomusic.music_list)
            return
    if type == "qq":
        for playlist_id in playlist_ids:
            index = 0
            url = f"http://i.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg?type=1&utf8=1&disstid={playlist_id}&loginUin=0"
            headers = {
                "Referer": "https://y.qq.com/n/yqq/playlist",
                "Cookie": "uin=",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
            }
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # 如果请求出现4xx、5xx等错误状态码则抛出异常
            # print(response.text)
            result = response.text
            
            # Remove callback function wrapper and parse JSON
            json_data = re.sub(r'^callback\(|MusicJsonCallback\(|jsonCallback\(|\)$', '', result)
            res = json.loads(json_data)
            one_music_list = []
            # Extract songlist and format music items (implement formatMusicItem function)
            log.debug(f"getmy_playlist result:{result}")
            if 'cdlist' in res and len(res['cdlist']) > 0:
                # print(res['cdlist'][0]['songlist'])
                list_name = res['cdlist'][0]['dissname'] + "-QQ"
                for music in res['cdlist'][0]['songlist']:
                    name = music["songname"]
                    log.info(f"getmy_playlist name:{name}")
                    picUrl = ""
                    artist = music["singer"][0]["name"]
                    album = music["albumname"]
                    songmid = music["songmid"]
                    # url = f"https://lxmusicapi.onrender.com/url/tx/{songmid}/128k"
                    url = f"http://127.0.0.1:1011/url/tx/{songmid}/{br}k?key=n3Oyzh5QNRtD0JI0AXHFaw=="
                    lxurl = url
                    apiurl = ""
                    try:
                        search_url = f"{api_host}/cloudsearch?keywords={name}({artist})&limit=10&type=1"
                        log.info(f"getmy_playlist search_url: {search_url}")
                        response = requests.get(search_url,timeout=2)
                        response.raise_for_status()  # 如果请求出现4xx、5xx等错误状态码则抛出异常
                        for song in response.json()['result']['songs']:
                            apiurl = f"{api_host}/song/url?id={song['id']}&br={br}000&proxy=HTTP:%2F%2F127.0.0.1:8080"
                            if song['name'] == name and song['ar'][0]['name'] == artist:
                                url = apiurl
                                lxurl = ""
                                picUrl = song["al"]["picUrl"]
                                log.info(f"getmy_playlist api_url:{url}")
                                break
                        # response = requests.get(url,timeout=2)
                        # response.raise_for_status()  # 如果请求出现4xx、5xx等错误状态码则抛出异常
                        # url = response.json()['data'][0]['url']
                    except:
                        # response = requests.get(url, headers=headers,timeout=30)
                        # response.raise_for_status()  # 如果请求出现4xx、5xx等错误状态码则抛出异常
                        # lxurl = response.json()['url']
                        pass
                    log.info(f"getmy_playlist url: {url}")
                    if (not name) or (not url):
                        continue
                    xiaomusic.all_music[name] = url
                    xiaomusic.all_music_tags[name] = {
                        "title": name,
                        "artist": artist,
                        "album": album,
                        "year": "",
                        "genre": "",
                        "picture": picUrl,
                        "lyrics": "",
                        "apiurl": apiurl,
                        "xlurl":lxurl,
                    }
                    one_music_list.append(name)
                    if index > 100:
                        break
                    index += 1
                log.debug(f"getmy_playlist name:{list_name}")
                log.debug(one_music_list)
                # 歌曲名字相同会覆盖
                xiaomusic.music_list[list_name] = one_music_list
                xiaomusic.try_save_tag_cache()
        return

    log.error(f"getmy_playlist type:{type} not support")


if __name__ == '__main__':
    getmy_playlist(api='qq',playlist_id=9381106378)