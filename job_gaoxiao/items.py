# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobGaoxiaoItem(scrapy.Item):
    # 文章标题
    article_title = scrapy.Field()
    # 文章图片，视频
    article_video = scrapy.Field()
    # 文章图片视频 上的标签
    article_tag = scrapy.Field()
    # 好笑度
    article_funny = scrapy.Field()
    # 评论量
    article_comment = scrapy.Field()
    # 作者
    article_author = scrapy.Field()
    # 作者头像
    article_author_profile = scrapy.Field()

    # def get_sql_str_values(self, data):
    #     sql_insert = """
    #             INSERT INTO %s (%s)
    #             VALUES (%s)
    #             """ % (
    #         'qsbk_1',
    #         ','.join(data.keys()),
    #         ','.join(['%s'] * len(data))
    #     )
    #     values = list(data.values())
    #     return sql_insert, values
    #
    # def get_collection_name(self):
    #     return 'qsbk_1'
    def get_insert_sql(self,item):
        insert_sql = """
            insert into qsbk_1(article_title,article_video,article_tag,article_funny,article_comment,article_author,article_author_profile)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """
        params = (
            item['article_title'], item['article_video'], item['article_tag'], item['article_funny'],
            item['article_comment'],
            item['article_author'], item['article_author_profile']
        )
        return insert_sql, params


class JobGxiaoxiangqingItem(scrapy.Item):
    # 获取详情标题
    details_title = scrapy.Field()
    # 发表时间
    details_date = scrapy.Field()
    # 好笑度
    details_funny = scrapy.Field()
    # 内容
    details_content = scrapy.Field()
    # 发此地址
    details_Published_address = scrapy.Field()
    # 评论详情
    details_comment = scrapy.Field()
    # def get_sql_str_values(self, data):
    #     sql_insert = """
    #             INSERT INTO %s (%s)
    #             VALUES (%s)
    #             """ % (
    #         'qbsk_2',
    #         ','.join(data.keys()),
    #         ','.join(['%s'] * len(data))
    #     )
    #     values = list(data.values())
    #     return sql_insert, values
    #
    # def get_collection_name(self):
    #     return 'qbsk_2'
    def get_insert_sql(self,item):
        insert_sql = """
            insert into qbsk_2(details_title,details_date,details_funny,details_content,details_Published_address,details_comment)
            VALUES (%s,%s,%s,%s,%s,%s)
            """
        params = (
            item['details_title'], item['details_date'], item['details_funny'], item['details_content'],item['details_Published_address'], item['details_comment']

        )
        return insert_sql, params


class JobGgaoxiaohotItem(scrapy.Item):
    # 发表用户
    user_name = scrapy.Field()
    # 用户头像
    user_pic = scrapy.Field()
    # 文本
    content = scrapy.Field()
    # 好笑度
    funny = scrapy.Field()
    # 评论数
    comment_count = scrapy.Field()
    # 评论用户
    comment_user = scrapy.Field()
    # 评论内容
    comment_text = scrapy.Field()
    # 评论点赞
    comment_dianzhan = scrapy.Field()

    # def get_sql_str_values(self, data):
    #     sql_insert = """
    #             INSERT INTO %s (%s)
    #             VALUES (%s)
    #             """ % (
    #         'qbsk_3',
    #         ','.join(data.keys()),
    #         ','.join(['%s'] * len(data))
    #     )
    #     values = list(data.values())
    #     return sql_insert, values
    #
    # def get_collection_name(self):
    #     return 'qbsk_3'
    def get_insert_sql(self,item):
        insert_sql = """
            insert into qbsk_3(user_name,user_pic,content,funny,comment_count,comment_user,comment_dianzhan)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """
        params = (
            item['user_name'], item['user_pic'], item['content'], item['funny'], item['comment_count'],item['comment_user'], item['comment_dianzhan']
        )
        return insert_sql, params


class JobGgaoxiaousertem(scrapy.Item):
    # 用户名
    user_name = scrapy.Field()
    # 用户头像
    user_pic = scrapy.Field()
    # 推荐
    recommendations = scrapy.Field()
    # 内容
    content = scrapy.Field()
    # 热度
    liveness = scrapy.Field()
    # 发表时间
    date_publish = scrapy.Field()
    # 点赞人
    likesm = scrapy.Field()

    # def get_sql_str_values(self, data):
    #     sql_insert = """
    #             INSERT INTO %s (%s)
    #             VALUES (%s)
    #             """ % (
    #         'qbsk_4',
    #         ','.join(data.keys()),
    #         ','.join(['%s'] * len(data))
    #     )
    #     values = list(data.values())
    #     return sql_insert, values

    # def get_collection_name(self,item):
    #     return 'qbsk_4'
    def get_insert_sql(self, item):
        insert_sql = """
            insert into qbsk_4(user_name,user_pic,recommendations,content,liveness,date_publish,likesm)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """
        params = (
            item['user_name'], item['user_pic'], item['recommendations'], item['content'], item['liveness'],item['date_publish'], item['likesm']

        )
        return insert_sql, params