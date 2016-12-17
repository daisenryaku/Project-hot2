# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
from news.dealstr import cleanStr,getStr
from news.dealurl import getUrl,filterUrl
import time

class SohunewsSpider(scrapy.Spider):
    name = "sohu"
    allowed_domains = ["sohu.com"]
    start_urls = (
        'http://www.sohu.com/',
    )
    filter = ['corp','tv','db.auto','caipiao','tousu','pic.cul','fund','2sc']

    def parse(self, response):
        #获得首页导航链接，继续爬
        match1 = '//*[@id="navList"]/div/ul/li/a/@href'
        urls = getUrl(response, match1, [], self.filter)
        for url in urls:
            yield scrapy.Request(url, callback=self.parse2)

    def parse2(self, response):
        #li
        data = [sel.xpath("text()""|@href").extract() for sel in response.xpath('//li/a')]
        data = [i for i in data if len(i) == 2 and len(i[1])>9 and 'shtml' in i[0].split('.')]
        #h2
        h2_data = [sel.xpath("text()""|@href").extract() for sel in response.xpath('//h2/a')]
        h2_data = [i for i in h2_data if len(i) == 2 and len(i[1])>9 and 'shtml' in i[0].split('.')]
        for i in h2_data:
            data.append(i)
        #h3
        h3_data = [sel.xpath("text()""|@href").extract() for sel in response.xpath('//h3/a')]
        h3_data = [i for i in h3_data if len(i) == 2 and len(i[1])>9 and 'shtml' in i[0].split('.')]
        for i in h3_data:
            data.append(i)
        #url
        urls = [i[0] for i in data]
        urls = filterUrl(urls,self.filter)
        for url in urls:
            yield scrapy.Request(url, callback=self.parse3)

    def parse3(self,response):
        item = NewsItem()
        #url
        item['news_url'] = response.url
        #title
        title = response.xpath('//title/text()').extract()
        if title != []:
            title = title[0].replace(',','').replace(' ','').replace('\n','')
            #标题过滤
            title = title.split('_')[0].split('-')[0].split('|')[0]
            item['news_title'] = title
        else:
            item['news_title'] = ''
        #abstract & body
        abstract = response.xpath('//p/text()').extract()
        if abstract != []:
            x = [cleanStr(i) for i in abstract if len(i.replace(' ','')) > 20]
            if x != []:
                text = getStr(x)
                if u'\u3011' in text:
                    item['news_abstract'] = text.split(u'\u3011')[1]
                else:
                    item['news_abstract'] = text
                #新闻正文
                s = ''
                for i in x:
                    s += i
                item['news_body'] = s.replace(' ','').replace('\n','').replace('\t','')
            else:
                item['news_abstract'] = title
                item['news_body'] = title
        else:
            item['news_abstract'] = title
            item['news_body'] = title
        #time
        item['news_time'] = time.time()
        yield item
