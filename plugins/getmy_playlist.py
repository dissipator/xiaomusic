import requests

# 功能： 从网易云账号读取歌单，并生成播放url
# type: 歌单来源类型
# api_host： api服务器地址
# playlist_id： 歌单ID，uid：网易云账号用户id
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


async def getmy_playlist(
    type="netease", api_host="http://127.0.0.1/api", playlist_id=None, uid=None
):
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
                list_name = item.get("name")

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
                    url = f"{api_host}/song/url?id={music['id']}&br=350000&realIP=211.161.244.70&proxy=HTTP:%2F%2F127.0.0.1:8080"
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
        if playlist_id:
            songs_url = f"{api_host}/playlist/detail?id={playlist_id}"
            # 发起请求
            response = requests.get(songs_url, timeout=5)  # 增加超时以避免长时间挂起
            response.raise_for_status()  # 如果响应不是200，引发HTTPError异常

            musics = response.json()
            list_name = musics["playlist"]["name"]
            log.info(f"getmy_playlist list_name:{list_name} ")
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
                url = f"{api_host}/song/url?id={music['id']}&br=350000&proxy=HTTP:%2F%2F127.0.0.1:8080"
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
            return
    else:
        log.error(f"getmy_playlist type:{type} not support")
