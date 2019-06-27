# -*- coding: utf-8 -*-
import scrapy
from job_gaoxiao.items import JobGaoxiaoItem, JobGxiaoxiangqingItem,JobGgaoxiaohotItem,JobGgaoxiaousertem
from scrapy_redis.spiders import RedisSpider


# class QsbkSpider(scrapy.Spider):

class QsbkSpider(RedisSpider):
    name = 'qsbk'
    allowed_domains = ['qiushibaike.com']
    # start_urls = ['https://www.qiushibaike.com/']
    redis_key = 'qsbk:start_url'

    def parse(self, response):
        li_list = response.xpath('//div[@class="recommend-article"]/ul/li')
        for li in li_list:
            hot_itme = JobGaoxiaoItem()
            """
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
            #作者头像
            article_author_profile = scrapy.Field()
            """
            hot_itme['article_title'] = li.xpath('./div[@class="recmd-right"]/a[@class="recmd-content"]/text()').extract_first('')
            hot_itme['article_video'] = li.xpath('./a/img/@src').extract_first('')
            hot_itme['article_tag'] = li.xpath('./a/div/text()').extract_first('')
            hot_itme['article_funny'] = li.xpath('.//div[@class="recmd-num"]/span[1]/text()').extract_first('')
            hot_itme['article_comment'] = li.xpath('.//div[@class="recmd-num"]/span[4]/text()').extract_first('')
            hot_itme['article_author'] = li.xpath('.//span[@class="recmd-name"]/text()').extract_first('')
            hot_itme['article_author_profile'] = li.xpath('.//a[@class="recmd-user"]/img/@src').extract_first('')
            yield hot_itme
            new_url = 'https://www.qiushibaike.com' + (li.xpath('.//a[@class="recmd-content"]/@href').extract_first(''))
            yield scrapy.Request(
                url=new_url,
                callback=self.parse_data_particulars
            )
            if '下一页' in response.text:
                last_page = int(
                    response.xpath('//ul[@class="pagination"]/li[last()-1]/a/span/text()').extract_first(''))
                for page in range(2, last_page + 1):
                    next_page_url = 'https://www.qiushibaike.com/8hr/page/%s/' % str(page)
                    yield scrapy.Request(
                        url=next_page_url,
                        callback=self.parse
                    )
            hot_url = 'https://www.qiushibaike.com/' + response.xpath('//div[@id="index_header"]/ul/li[3]/a/@href').extract_first('')
            yield scrapy.Request(
                url=hot_url,
                callback=self.parse_hot_data
            )
    #详情页数据解析
    def parse_data_particulars(self, response):
        if response.text:
            xiangqing_item = JobGxiaoxiangqingItem()
            """
            # 获取详情标题
            details_title = scrapy.Field()
            # 发表时间
            details_date = scrapy.Field()
            # 好笑度
            details_funny = scrapy.Field()
            # 内容
            details_content = scrapy.Field()
            # 发表地址
            details_Published_address = scrapy.Field()
            #评论详情
            details_comment = scrapy.Field()
            """
            xiangqing_item['details_title'] = response.xpath('.//h1[@class="article-title"]/text()').extract_first('').replace('\n', '')
            xiangqing_item['details_date'] = response.xpath('.//span[@class="stats-time"]/text()').extract_first('').replace('\n', '')
            xiangqing_item['details_funny'] = response.xpath('.//i[@class="number"]/text()').extract_first('').replace('\n', '')
            xiangqing_item['details_Published_address'] = response.xpath('.//a[@class="source-column"]/text()').extract_first('').replace('\n', '')
            s = response.xpath('.//div[@class="thumb"]//img/@src').extract()
            d = ",".join(s)
            xiangqing_item['details_content'] = d + ',' + response.xpath('.//video[@id="article-video"]/source/@src').extract_first('') + ',' + response.xpath('//div[@class="content"]//text()').extract_first('').replace('\u200b', '')
            if '糗友神评'in response.text:
                pinglun = response.xpath('.//div[@class="comments-list clearfix"]/div/div[@class="replay"]')
                s = []
                for pl_xq in pinglun:
                    a =pl_xq.xpath('.//a/text()').extract_first('')+pl_xq.xpath('.//span/text()').extract_first('')
                    s.append(a)
                xiangqing_item['details_comment']=','.join(s)
            else:
                xiangqing_item['details_comment']= ''
            #获取作者url
            author_url ='https://www.qiushibaike.com'+ response.xpath('//div[@id="articleSideLeft"]/a/@href').extract_first('')+'articles/'
            # print(author_url)
            yield xiangqing_item
            yield scrapy.Request(
                url=author_url,
                #回调到作者页
                callback=self.parse_author_data
            )


        else:
            print('该网页没有数据')
    #24小时数据解析
    def parse_hot_data(self,response):
        """
        #发表用户
        user_name = scrapy.Field()
        #用户头像
        user_pic = scrapy.Field()
        #文本
        content = scrapy.Field()
        #好笑度
        funny = scrapy.Field()
        #评论数
        comment_count = scrapy.Field()
        #评论用户
        comment_user = scrapy.Field()
        #评论内容
        comment_text = scrapy.Field()
        #评论点赞
        comment_dianzhan = scrapy.Field()
        :param response:
        :return:
        """
        hot_itme = JobGgaoxiaohotItem()
        if response.text:
            data_content= response.xpath('//div[@class="content-block clearfix"]/div[@id="content-left"]/div')

            for data_one in data_content:
                # print(data_one)
                hot_itme['user_pic'] = data_one.xpath('.//div[@class="author clearfix"]/a[1]/img/@src').extract_first('')+data_one.xpath('.//div[@class="author clearfix"]/span[1]/img/@src').extract_first('')
                hot_itme['user_name'] = data_one.xpath('.//div[@class="author clearfix"]/a[2]/h2/text()').extract_first('').replace('\n', '')+data_one.xpath('.//div[@class="author clearfix"]/span[2]/h2/text()').extract_first('').replace('\n', '')
                hot_itme['content'] = (',').join(data_one.xpath('.//a[@class="contentHerf"]/div[@class="content"]/span//text()').extract()).replace('\n','').replace('\u3000','').replace(' ','')+data_one.xpath('.//div[@class="thumb"]/a/img/@src').extract_first('')
                hot_itme['funny']= data_one.xpath('.//span[@class="stats-vote"]/i/text()').extract_first('')
                hot_itme['comment_count'] = data_one.xpath('.//span[@class="stats-comments"]/a/i/text()').extract_first('')
                hot_itme['comment_user'] = data_one.xpath('.//span[@class="cmt-name"]/text()').extract_first('')
                hot_itme['comment_text'] = (',').join(data_one.xpath('.//div[@class="main-text"]/text()').extract()).replace('\n','')
                hot_itme['comment_dianzhan'] = ('').join(data_one.xpath('.//div[@class="likenum"]/text()').extract()).replace('\n','')
                print(hot_itme)
                new_URL = 'https://www.qiushibaike.com'+data_one.xpath('.//a[@class="contentHerf"]/@href').extract_first('')
                yield hot_itme
                yield scrapy.Request(
                    url=new_URL,
                    callback=self.parse_data_particulars
                )

                if '下一页' in response.text:
                    last_page = int(
                             response.xpath('//ul[@class="pagination"]/li[last()-1]/a/span/text()').extract_first(''))
                    for page in range(2, last_page + 1):
                        next_page_url = 'https://www.qiushibaike.com/hot/page/%s/' % str(page)
                        yield scrapy.Request(
                            url=next_page_url,
                            callback=self.parse_hot_data
                        )
        else:
            print('该网页没有数据')
    #解析个人动态
    def parse_author_data(self,response):
        if response.text:
            if '当前用户已关闭糗百个人动态' not in response.text:
                data_xq=response.xpath('//div[@class="user-col-right"]/div')
                for data in data_xq:
                    user_itme=JobGgaoxiaousertem()
                    """
                    #用户名
                    user_name = scrapy.Field()
                    #用户头像
                    user_pic = scrapy.Field()
                    #推荐
                    recommendations = scrapy.Field()
                    #内容
                    content = scrapy.Field()
                    #热度
                    liveness = scrapy.Field()
                    #发表时间
                    date_publish = scrapy.Field()
                    #点赞人
                    likesm= scrapy.Field()
                    """
                    user_itme['user_name']= data.xpath('.//li[@class="user-article-avatar"]/a[2]/text()').extract_first('').replace('\n','')+data.xpath('.//li[@class="user-article-avatar"]/img/@alt').extract_first('').replace('\n','')
                    user_itme['user_pic'] = data.xpath('.//li[@class="user-article-avatar"]/a[1]/img/@src').extract_first('').replace('\n','')+data.xpath('.//li[@class="user-article-avatar"]/img/@src').extract_first('').replace('\n','')
                    user_itme['recommendations'] =','.join(data.xpath('.//li[@class="user-comment-info"]//text()').extract()).replace('\n','')
                    user_itme['content'] =','.join(data.xpath('.//li[@class="user-article-text"]//a//text()').extract()).replace('\n','')+' '+data.xpath('.//li[@class="user-article-pic"]/a/img/@src').extract_first('').replace('\n','')
                    user_itme['liveness'] = data.xpath('.//li[@class="user-article-stat"]/text()').extract_first('').replace('发表于','').replace('\n','')
                    user_itme['date_publish']=data.xpath('.//li[@class="user-article-stat"]/a/text()').extract_first('').replace('\n','')
                    user_itme['likesm'] = ''.join(data.xpath('.//li[@class="user-article-vote"]//text()').extract()).replace('\n', '')
                    yield user_itme
                    next_page = int(response.xpath('//ul[@class="user-navcnt"]/li[last()-1]/a/text()').extract_first(''))
                    #用户详情下一页
                    for page_data in range(2,next_page+1):
                        yield scrapy.Request(
                            url=response.url+'page/%s/'%str(page_data),
                            callback=self.parse_author_data
                        )
            else:
                print('当前用户已关闭糗百个人动态')
        else:
            print('该网页没有数据')






