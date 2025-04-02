import os
import subprocess

def extract_audio_from_videos(input_path, output_folder, file_name):
    """
    从指定文件夹中的视频文件提取音频，保存为相同文件名的音频文件。
    
    :param input_folder: 输入视频文件所在的文件夹路径。
    :param output_folder: 输出音频文件保存的文件夹路径。
    """
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 检查是否为视频文件（可根据需要扩展）
    if input_path.endswith(('.mp4', '.avi', '.mov', '.mkv')):
        # 输出文件路径
        output_file_name = os.path.splitext(file_name)[0] + ".wav"
        output_file_path = os.path.join(output_folder, output_file_name)
        
        # 使用 ffmpeg 提取音频
        try:
            print(f"正在处理: {file_name}")
            # 在 extract_audio_from_videos 函数中优化ffmpeg命令
            command = [
                "ffmpeg",
                "-i", input_path,
                "-ar", "16000",        # 采样率统一为16kHz
                "-ac", "1",            # 单声道
                "-af", "highpass=f=300,lowpass=f=3000",  # 过滤高低频噪声
                output_file_path
            ]
            subprocess.run(command, check=True)
            print(f"提取成功: {output_file_path}")
            return output_file_path
        except subprocess.CalledProcessError as e:
            print(f"提取失败: {file_name}，错误信息: {e}")
    print("所有文件处理完成！")

if __name__ == '__main__':
    input_path = r"E:\GitHub\Repositories\my_item\learn\小项目\爬取youtube视频\videos\困在汪苏泷这段rap里了 单依纯38个转音也太强了#单依纯 #汪苏泷 #如果爱忘了 #声生不息.mp4"
    output_folder = r'E:\GitHub\Repositories\my_item\learn\小项目\爬取youtube视频\audio'
    file_name = "汪苏泷这段rap"
    
    extract_audio_from_videos(input_path, output_folder, file_name)
