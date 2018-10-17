# -*- coding: utf-8 -*-
import scrapy

from ..items import DoubanItem
class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'
    # 允许的域名
    allowed_domains = ['movie.douban.com']
    # 入口URL
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
        #循环电影的条目
        for i_item in movie_list:
            #导入item，进行数据解析
            douban_item = DoubanItem()
            douban_item['serial_number'] = i_item.xpath(".//div[@class='item']//em/text()").extract_first()
            douban_item['movie_name'] =  i_item.xpath(".//div[@class='info']//div[@class='hd']/a/span[1]/text()").extract_first()
            #如果文件有多行进行解析
            content = i_item.xpath(".//div[@class='info']//div[@class='bd']/p[1]/text()").extract()
            for i_content in content:
                content_s ="".join( i_content.split())
                douban_item['introduce'] = content_s
            douban_item['star'] = i_item.xpath(".//span[@class='rating_num']/text()").extract_first()
            douban_item['evaluate'] = i_item.xpath(".//div[@class='star']//span[4]/text()").extract_first()
            douban_item['describe'] = i_item.xpath(".//p[@class='quote']/span/text()").extract_first()
            print(douban_item)
            yield  douban_item
        #解析下一页，取后一页的XPATH
        next_link = response.xpath("//span[@class='next']/link/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield  scrapy.Request("https://movie.douban.com/top250"+next_link,callback=self.parse)
