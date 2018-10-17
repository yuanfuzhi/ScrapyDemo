# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy import log
from twisted.enterprise import adbapi
from .settings import MYSQL_HOST,MYSQL_DBNAME,MYSQL_USER,MYSQL_PASSWD,MYSQL_PORT


class DoubanPipeline(object):
     def __init__(self):
         dbhost=MYSQL_HOST
         dbname=MYSQL_DBNAME
         dbuser=MYSQL_USER
         dbpass=MYSQL_PASSWD
         port=MYSQL_PORT
         self.conn = pymysql.connect(user=dbuser, passwd=dbpass, db=dbname, host=dbhost, charset="utf8", use_unicode=True)
         self.cursor = self.conn.cursor()
        #清空表：
         self.cursor.execute("truncate table doubantop;")
         self.conn.commit()

     def process_item(self, item, spider):
         try:
             # 查重处理
            self.cursor.execute(
                """select * from doubantop where serial_number = %s""",
                item['serial_number'])
            # 是否有重复数据
            repetition = self.cursor.fetchone()

            # 重复
            if repetition:
                pass

            else:
                self.cursor.execute("""INSERT INTO doubantop (serial_number, movie_name, introduce, star, evaluate, describes)
                                VALUES (%s, %s, %s, %s, %s, %s)""",
                                (
                                    item['serial_number'],
                                    item['movie_name'],
                                    item['introduce'],
                                    item['star'],
                                    item['evaluate'],
                                    item['describe']
                                )
                                     )
                self.conn.commit()

         except pymysql.Error as e:
             print ("Error %d: %s" % (e.args[0],e.args[1]))
         return item

