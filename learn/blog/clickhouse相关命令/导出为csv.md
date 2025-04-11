在 ClickHouse 中导出数据到 CSV 文件可以通过以下步骤完成：

### 方法一：使用`clickhouse-client`命令行工具

~~~bash
# 94中，注意替换
sudo docker exec -it clickhouse clickhouse-client --database=ty --query="SELECT * FROM ods_telegram_message FORMAT CSV" > tg_msg.csv
sudo docker exec -it clickhouse clickhouse-client --database=ty --query="SELECT * FROM ods_telegram_message FORMAT CSVWithNames" > tg_msg.csv
~~~



1. **基本导出命令**：

   ```bash
   clickhouse-client \
     --user=<用户名> \
     --password=<密码> \
     --database=<数据库名> \
     --query="SELECT * FROM <表名> FORMAT CSV" \
     > <输出文件路径>.csv
   ```

   - **示例**：
     
     ```bash
     clickhouse-client --query="SELECT * FROM my_table FORMAT CSV" > data.csv
     ```

2. **包含列标题**：
   使用`CSVWithNames`格式以包含列名：

   ```bash
   clickhouse-client --query="SELECT * FROM my_table FORMAT CSVWithNames" > data_with_header.csv
   ```

3. **指定主机和端口**（若远程连接）：

   ```bash
   clickhouse-client --host=远程主机IP --port=9000 --query="..." > data.csv
   ```

### 方法二：通过 HTTP 接口

使用`curl`调用 ClickHouse 的 HTTP 接口：

```bash
curl "http://用户名:密码@服务器地址:8123/?query=SELECT+*+FROM+数据库.表+FORMAT+CSV" > data.csv
```

- **示例**：
  ```bash
  curl "http://default:123456@localhost:8123/?query=SELECT%20*%20FROM%20mydb.mytable%20FORMAT%20CSVWithNames" > data.csv
  ```

### 方法三：使用`INTO OUTFILE`（仅限本地）

在 ClickHouse 22.6 及以上版本中，支持直接导出到服务器本地文件：

```sql
SELECT * FROM my_table INTO OUTFILE '/path/to/output.csv' FORMAT CSVWithNames;
```

**注意**：需确保 ClickHouse 服务有权限写入目标路径。

### 参数说明

- **--user**：ClickHouse 用户名（默认`default`）。
- **--password**：对应用户的密码。
- **--database**：指定数据库（可选）。
- **--query**：要执行的 SQL 查询，需包含`FORMAT`子句。
- **FORMAT CSV**：指定输出格式为 CSV。
- **FORMAT CSVWithNames**：包含列名的 CSV。

### 验证导出结果

- 检查文件头部：`head -n 5 data.csv`
- 统计行数：`wc -l data.csv`（应与表数据量一致）

### 处理大数据量

- 分页导出：结合`LIMIT`和`OFFSET`分批查询。
- 并行导出：按时间或 ID 范围拆分查询，并行执行。

### 注意事项

- **权限**：确保用户有执行查询和访问表的权限。
- **编码**：默认 UTF-8，避免乱码。
- **特殊字符**：CSV 自动处理逗号和换行符，字段会用双引号包裹。

按照上述方法，即可轻松将 ClickHouse 数据导出为 CSV 文件。
