import os
import whisper

now_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(now_path)

def transcribe_audio_files(input_folder, output_folder, model_size="base"):
    """
    使用 Whisper 模型识别文件夹中的音频文件，并输出字幕文件到指定文件夹。

    :param input_folder: 输入音频文件所在的文件夹路径。
    :param output_folder: 输出字幕文件保存的文件夹路径。
    :param model_size: Whisper 模型大小 (如 "tiny", "base", "small", "medium", "large")。
    """
    # 检查并创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 加载 Whisper 模型
    print(f"加载 Whisper 模型: {model_size}...")
    model = whisper.load_model(model_size)

    # 遍历输入文件夹中的所有音频文件
    for file_name in os.listdir(input_folder):
        input_file_path = os.path.join(input_folder, file_name)

        # 检查是否为音频文件
        if file_name.endswith(('.wav', '.mp3', '.m4a', '.flac')):
            print(f"正在处理: {file_name}")
            try:
                # 识别音频内容
                result = model.transcribe(input_file_path)

                # 输出字幕文件路径
                output_file_name = os.path.splitext(file_name)[0] + ".txt"
                output_file_path = os.path.join(output_folder, output_file_name)

                # 保存字幕到文本文件
                with open(output_file_path, "w", encoding="utf-8") as f:
                    f.write(result["text"])
                print(f"字幕保存成功: {output_file_path}")

            except Exception as e:
                print(f"处理失败: {file_name}，错误信息: {e}")

    print("所有文件处理完成！")


# 示例用法
input_folder = os.path.join(file_path,"英语音频")
output_folder = os.path.join(file_path,"英语字幕")
transcribe_audio_files(input_folder, output_folder, model_size="base")
