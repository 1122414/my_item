
在 Python 中使用 `yt-dlp` 可以轻松实现视频/音频下载功能（如 YouTube、B站等平台的资源）。以下是详细指南：

---

### 1. 安装 yt-dlp
```bash
pip install yt-dlp
```

---

### 2. 基础用法
#### 下载视频
```python
import yt_dlp

url = "https://www.youtube.com/watch?v=视频ID"

# 配置选项（可选）
ydl_opts = {
    'format': 'bestvideo+bestaudio/best',  # 选择最佳画质+音质
    'outtmpl': 'downloads/%(title)s.%(ext)s',  # 保存路径模板
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
```

---

### 3. 进阶功能
#### 仅下载音频
```python
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',  # 提取音频
        'preferredcodec': 'mp3',      # 输出格式
        'preferredquality': '192',    # 音质
    }],
    'outtmpl': 'audio/%(title)s.%(ext)s',
}
```

#### 获取视频信息
```python
with yt_dlp.YoutubeDL() as ydl:
    info = ydl.extract_info(url, download=False)
    print(f"标题: {info['title']}")
    print(f"时长: {info['duration']} 秒")
    print(f"上传者: {info['uploader']}")
```

#### 下载播放列表
```python
ydl_opts = {
    'playliststart': 1,   # 从第1个视频开始
    'playlistend': 5,     # 下载到第5个视频
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/playlist?list=播放列表ID'])
```

---

### 4. 高级配置
#### 自定义代理
```python
ydl_opts = {
    'proxy': 'socks5://127.0.0.1:1080',  # 使用代理
}
```

#### 设置 Cookies（绕过年龄限制）
```python
ydl_opts = {
    'cookiefile': 'cookies.txt',  # 从浏览器导出的 cookies 文件
}
```

---

### 5. 错误处理
```python
try:
    with yt_dlp.YoutubeDL() as ydl:
        ydl.download([url])
except yt_dlp.DownloadError as e:
    print(f"下载失败: {e}")
except yt_dlp.utils.ExtractorError as e:
    print(f"解析链接失败: {e}")
```

---

### 6. 常用参数说明
| 参数                  | 作用                                                        |
| --------------------- | ----------------------------------------------------------- |
| `format`              | 指定视频/音频格式（如 `bestvideo[height<=1080]+bestaudio`） |
| `outtmpl`             | 自定义保存路径和文件名                                      |
| `quiet`               | 静默模式（不输出进度条）                                    |
| `writethumbnail`      | 下载封面（`True`/`False`）                                  |
| `merge_output_format` | 合并后的格式（如 `mp4`）                                    |

---

### 注意事项
1. **遵守法律法规**：确保你有权下载目标内容（避免侵犯版权）。
2. **网站限制**：部分平台可能检测并封禁批量下载行为。
3. **更新维护**：定期更新 `yt-dlp` 以适配网站变更：
   ```bash
   pip install --upgrade yt-dlp
   ```

如果需要更复杂的操作（如字幕下载、HLS流处理等），可参考[官方文档](https://github.com/yt-dlp/yt-dlp)。