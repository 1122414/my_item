import pandas as pd
import os

# 设置你的文件夹路径
folder_path = r"C:\Users\Lenovo\Desktop\vscode_python\小项目\csv行列转换\data"  # 修改为你的文件夹路径
aim_path = r"C:\Users\Lenovo\Desktop\vscode_python\小项目\csv行列转换\output_data"

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):  # 只处理CSV文件
        file_path = os.path.join(folder_path, filename)  # 拼接文件路径
        
        # 读取CSV文件
        df = pd.read_csv(file_path, header=None)

        # 将每一行数据转置成列
        df_transposed = df.T

        # 构造输出文件的路径，原文件名 + '_transposed.csv'
        output_filename = filename.replace('.csv', '_transposed.csv')
        output_path = os.path.join(aim_path, output_filename)

        # 保存转置后的数据到新的CSV文件
        df_transposed.to_csv(output_path, index=False, header=False)

        print(f"已处理文件：{filename}，保存为：{output_filename}")
