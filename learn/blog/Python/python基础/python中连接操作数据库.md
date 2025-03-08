~~~python
# 建立连接
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='3306',
    database='python_spider',
    charset='utf8'
    # 自动执行变更 无需conn.commit()
    autocommit=True
)

# 获得游标
cur = conn.cursor()

# 执行sql语句
cur.execute('insert into Mallox_integraservices(publish_time,publish_person,publish_content,view_url) values(%s,%s,%s,%s)', (publish_time_list[i],publish_person_list[i].strip(),publish_content_list_xpath[i].xpath('string(.)').strip(),view_url))

# 执行变更
conn.commit()

~~~

