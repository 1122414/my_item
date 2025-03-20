import pandas as pd
import chardet
from fuzzywuzzy import fuzz
file_path1 = r'C:\Users\Lenovo\Desktop\vscode_python\小项目\similar_goods\吉慕超市商品对比同行明细_去除.xlsx'
file_path2 = r'C:\Users\Lenovo\Desktop\vscode_python\小项目\similar_goods\共橙.xlsx'
with open (file_path1, 'rb') as f:
    raw_data = f.read(1024)

detected_encoding = chardet.detect(raw_data)['encoding']

# 读取表 1 和表 2 的数据
table1 = pd.read_excel(file_path1)
table2 = pd.read_excel(file_path2)

# 定义一个函数来计算字符串相似度并返回最相似的商品字段值
def find_most_similar_product(product_name):
    max_score = 0
    most_similar_product = None
    for index, row in table2.iterrows():
        score = fuzz.ratio(product_name, row['商品标题'])
        if score > max_score:
            max_score = score
            most_similar_product = row['商品标题'] 
            most_similar_product_price = row['价格（元）'] 
    return most_similar_product,most_similar_product_price

# 对表 1 中的每个商品名字应用函数找到最相似的商品字段值并添加到新列
table1['相似商品'], table1['相似商品价格'] = zip(*table1['商品标题'].apply(find_most_similar_product))

# 保存结果到新的 CSV 文件
table1.to_excel('matched_table.xlsx', index=False)