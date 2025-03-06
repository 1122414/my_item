# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class QiubaiproPipeline:

    # 专门用来处理item的pipeline
    # 该方法可以接受爬虫文件提交过来的item对象
    # 该方法每接收到一个item就会被调用一次
    fp = None
    # 重写父类方法，在爬虫启动时调用
    def open_spider(self, spider):
        print('爬虫开始了')
        self.fp = open('qiubai.txt', 'w', encoding='utf-8')


    # 必须携带 只能处理item对象
    def process_item(self, item, spider):
        name = item['name']
        total_price = item['total_price']

        self.fp.write(name + '|' + total_price + '\n')
        # 此处return item是为了将item对象传给其他管道处理
        return item
    
    # 重写父类方法，在爬虫结束时调用
    def close_spider(self, spider):
        self.fp.close()
        print('爬虫结束了')

# 管道文件中一个管道类对应将一组数据存储到一个平台或载体中
class mysqlPileLine(object):
    conn = None
    cursor = None
    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='3306',
            database='qiubai',
            charset='utf8'
        )
        
    def process_item(self, item, spider):
        self.cursor = self.conn.cursor()

        try:
            self.cursor.execute("insert into qiubai(name,total_price) values(%s,%s)",(item['name'],item['total_price']))
            self.conn.commit()
        except Exception as e:
            print(e)
        return item
    
    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()