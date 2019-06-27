# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy, pymysql
# class JobGaoxiaoPipeline(object):
#     def __init__(self, host, user, password, port, database, charset):
#         # 创建数据库链接
#         self.client = pymysql.Connect(
#             host=host, user=user,
#             password=password, database=database,
#             port=port, charset=charset
#         )
#         # 创建游标
#         self.mycursor = self.client.cursor()
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         host = crawler.settings['MYSQL_HOST']
#         user = crawler.settings['MYSQL_USER']
#         password = crawler.settings['MYSQL_PASSWORD']
#         port = crawler.settings['MYSQL_PORT']
#         database = crawler.settings['MYSQL_DATABASE']
#         charset = crawler.settings['MYSQL_CHARSET']
#         return cls(host, user, password, port, database, charset)
#
#     def process_item(self, item, spider):
#         """
#         :param item: 指的是spider爬虫文件中yield的item数据对象
#         :param spider:
#         :return:
#         """
#         item_dict = dict(item)
#         sql_insert, values = item.get_sql_str_values(item_dict)
#         try:
#             self.mycursor.execute(sql_insert, values)
#             print('===================================================================================================')
#             # self.client.commit()
#         except Exception as err:
#             print(err)
#             self.client.rollback()
#         return item
#
#     def close_spider(self, spider):
#         """可选方法,爬虫结束的时候会执行一次"""
#         self.client.close()
#         self.mycursor.close()
#         print('爬虫结束')










# twisted是一个异步的网络框架，这里可以帮助我们
# 实现异步将数据插入数据库
# adbapi里面的子线程会去执行数据库的阻塞操作，
# 当一个线程执行完毕之后，同时，原始线程能继续
# 进行正常的工作，服务其他请求。

from twisted.enterprise import adbapi
import pymysql

# mysql数据异步插入
class JobGaoxiaoPipeline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    # 使用这个函数来应用settings配置文件。
    @classmethod
    def from_crawler(cls, crawler):
        parmas = {
            'host': crawler.settings['MYSQL_HOST'],
            'user': crawler.settings['MYSQL_USER'],
            'passwd': crawler.settings['MYSQL_PASSWORD'],
            'db': crawler.settings['MYSQL_DATABASE'],
            'port': crawler.settings['MYSQL_PORT'],
            'charset': crawler.settings['MYSQL_CHARSET'],
        }
        # 初始化数据库连接池(线程池)
        # 参数一：mysql的驱动
        # 参数二：连接mysql的配置信息
        # **表示字典，*tuple元组,
        # 使用ConnectionPool，返回的是一个ThreadPool
        dbpool = adbapi.ConnectionPool(
            'pymysql',
            **parmas
        )
        return cls(dbpool)

    def process_item(self, item, spider):
        # 这里去调用任务分配的方法
        query = self.dbpool.runInteraction(
            self.insert_data_todb,
            item,
            spider
        )
        # 数据插入失败的回调
        query.addErrback(
            self.handle_error,
            item,
            spider
        )
        return item

    # 执行数据插入的函数
    def insert_data_todb(self, cursor, item,spider):
        data_dict = dict(item)
        insert_str, parmas = item.get_insert_sql(data_dict)
        print('=======================================================================')
        cursor.execute(insert_str, parmas)
        print('插入成功')
        return item

    # 如果异步任务执行失败的话，可以通过ErrBack()进行监听, 给get_insert_ql添加一个执行失败的回调事件
    def handle_error(self, failure, item,spider):
        print(failure)
        print('插入错误')
        # 在这里执行你想要的操作

