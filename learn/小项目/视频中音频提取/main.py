import os
import subprocess

now_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(now_path)

def extract_audio_from_videos(input_folder, output_folder):
    """
    从指定文件夹中的视频文件提取音频，保存为相同文件名的音频文件。
    
    :param input_folder: 输入视频文件所在的文件夹路径。
    :param output_folder: 输出音频文件保存的文件夹路径。
    """
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 遍历输入文件夹中的所有文件
    for file_name in os.listdir(input_folder):
        input_file_path = os.path.join(input_folder, file_name)
        
        # 检查是否为视频文件（可根据需要扩展）
        if file_name.endswith(('.mp4', '.avi', '.mov', '.mkv')):
            # 输出文件路径
            output_file_name = os.path.splitext(file_name)[0] + ".wav"
            output_file_path = os.path.join(output_folder, output_file_name)
            
            # 使用 ffmpeg 提取音频
            try:
                print(f"正在处理: {file_name}")
                command = [
                    "ffmpeg", "-i", input_file_path,
                    "-c:a", "pcm_s16le",  # 强制输出标准PCM格式
                    "-map", "0:a:0",
                    output_file_path
                ]
                subprocess.run(command, check=True)
                print(f"提取成功: {output_file_path}")
            except subprocess.CalledProcessError as e:
                print(f"提取失败: {file_name}，错误信息: {e}")
    print("所有文件处理完成！")

# 示例用法
input_folder = os.path.join(file_path,"英语视频")
output_folder = os.path.join(file_path,"英语音频")
extract_audio_from_videos(input_folder, output_folder)
