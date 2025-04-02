import os
import time
import torch
import whisper

current_path = os.path.dirname(os.path.abspath(__file__))

def get_text(save_path, text_title, model_size="large-v3"):
  '''解析获取文案'''
  """
    使用 Whisper 模型识别文件夹中的音频文件，并输出字幕文件到指定文件夹。

    :param input_folder: 输入音频文件所在的文件夹路径。
    :param output_folder: 输出字幕文件保存的文件夹路径。
    :param model_size: Whisper 模型大小 (如 "tiny", "base", "small", "medium", "large")。
  """
    # 先从视频提取音频
  audio_dir = os.path.join(current_path, 'data' ,'audio_data')
  if not os.path.exists(audio_dir):
      os.makedirs(audio_dir)
  
  audio_address = r"E:\GitHub\Repositories\my_item\learn\小项目\爬取youtube视频\audio\汪苏泷这段rap.wav"

  # 加载 Whisper 模型
  print(f"加载 Whisper 模型: {model_size}...")
  model = whisper.load_model(model_size)

  start_time = time.time()
  # 检查是否为音频文件
  if audio_address.endswith(('.wav', '.mp3', '.m4a', '.flac')):
      print(f"正在处理: {audio_address}")
      try:
          # 识别音频内容
          result = model.transcribe(
            audio_address, 
            language="zh",        # 明确指定中文
            fp16=True,           # CPU用户关闭FP16
            initial_prompt="以下是一首歌曲，请帮我生成对应歌词",  # 上下文提示
            temperature=0.2,      # 降低随机性
            beam_size=5,           # 增强解码稳定性
            word_timestamps=True,  # 启用词语级时间戳
            condition_on_previous_text=False  # 防止错误累积
          )
          return result["text"]
      except Exception as e:
          print(f"处理失败: {audio_address}，错误信息: {e}")
  print("所有文件处理完成！")
  end_time = time.time()
  print(f"处理完成，耗时: {end_time - start_time:.2f}秒")

if __name__ == "__main__":
  # 添加CUDA优化配置
  torch.backends.cudnn.benchmark = True
  torch.set_float32_matmul_precision('high')
  text = get_text(r'learn\小项目\爬取youtube视频\text','test')
  print(text)
  with open(r'learn\小项目\爬取youtube视频\text\test.txt', 'w', encoding='utf-8') as f:
    f.write(text)
  