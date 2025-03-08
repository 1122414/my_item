### python中json文件操作

~~~python
import json
 
# 读取JSON文件
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data
 
# 写入JSON文件
def write_json_file(file_path, data):
    with open(file_path, 'w') as file:
        # 使用indent=4进行格式化输出
        # ensure_ascii=False是在使用json.dump或json.dumps方法时的一个参数选项,它告诉 JSON 序列化器保留非 ASCII 字符而不进行转义。
        json.dump(data, file, indent=4, ensure_ascii=False)  
        

# 示例使用
json_file_path = 'example.json'
 
# 写入示例数据
data_to_write = {
    "name": "John",
    "age": 30,
    "city": "New York"
}
write_json_file(json_file_path, data_to_write)
 
# 读取数据
read_data = read_json_file(json_file_path)
print(read_data)
~~~

### json格式问题

json文件中，键值对必须用""包裹，''会报错