import yt_dlp
from comtypes.client import CreateObject
import sys
 
url = 'https://www.youtube.com/shorts/3XWUMrJhrOI'
ydl_opts = {
    'outtmpl': r'learn\小项目\爬取youtube视频\videos\%(title)s.%(ext)s',  # 下载的视频将被存储到videos文件夹，文件名为视频标题
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print("视频下载成功!已保存在videos文件夹中")