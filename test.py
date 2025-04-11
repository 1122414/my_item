import os
import subprocess


def extract_audio_from_videos(input_path):
    """
    从指定文件夹中的视频文件提取音频，保存为相同文件名的音频文件。

    :param input_folder: 输入视频文件所在的文件夹路径。
    :param output_folder: 输出音频文件保存的文件夹路径。
    """

    output_folder=r'/Users/yuanshanshan/Downloads/pycharm/12.3/yss/爬虫/audios'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_file_path=os.path.join(output_folder,'研讨厅音频.wav')

    # 检查是否为视频文件（可根据需要扩展）
    if input_path.endswith(('.mp4', '.avi', '.mov', '.mkv')):
        # 使用 ffmpeg 提取音频
        try:
            # print(f"正在处理: {file_name}")
            # 在 extract_audio_from_videos 函数中优化ffmpeg命令
            command = [
                "ffmpeg",
                "-i", input_path,
                "-ar", "16000",  # 采样率统一为16kHz
                "-ac", "1",  # 单声道
                "-af", "highpass=f=300,lowpass=f=3000",  # 过滤高低频噪声
                output_file_path
            ]
            subprocess.run(command, check=True)

            print(f"提取成功: {output_file_path}")
            return output_file_path
        except subprocess.CalledProcessError as e:
            pass
            #print(f"提取失败: {file_name}，错误信息: {e}")
    print("所有文件处理完成！")


if __name__ == '__main__':
    #视频的路径
    input_path = r"/Users/yuanshanshan/Downloads/pycharm/12.3/yss/爬虫/USENIX Security '23 - Know Your Cybercriminal： Evaluating Attacker Preferences by Measuring....mp4"
    
    extract_audio_from_videos(input_path)