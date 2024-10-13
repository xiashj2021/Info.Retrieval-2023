import scrapy
import re


class HelloSpider(scrapy.Spider):
    name = "hello"

    def start_requests(self):
        urls = [
            # 'http://quotes.toscrape.com/page/1/',
            # 'http://quotes.toscrape.com/page/2/',
            'http://xxxy.lzu.edu.cn'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # page = response.url.split("/")[-2]
        # filename = f'hello-{page}.html'
        filename = f'hello.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

class QuotesSpider(scrapy.Spider):
    name = "quotes-data"
    start_urls = [
        'https://quotes.toscrape.com/page/1/',
        'https://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

class QuotesAllSpider(scrapy.Spider):
    name = "quotes-whole-site"
    start_urls = [
        'https://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

class AuthorSpider(scrapy.Spider):
    name = 'author-all'

    start_urls = ['https://quotes.toscrape.com/']

    def parse(self, response):
        author_page_links = response.css('.author + a')
        yield from response.follow_all(author_page_links, self.parse_author)

        pagination_links = response.css('li.next a')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }

# -*- coding: utf-8 -*-
import scrapy
from IR2023.items import Ir2023Item
 
 
class MovieSpider(scrapy.Spider):
    # 爬虫名
    name = 'movie'
    # 爬取网站的域名
    allowed_domains = ['movie.douban.com']
    # 入口url
    start_urls = ['https://movie.douban.com/top250']
 
    def parse(self, response):
        # 首先抓取电影列表
        movie_list = response.xpath("//ol[@class='grid_view']/li")
        for selector in movie_list:
            # 遍历每个电影列表，从其中精准抓取所需要的信息并保存为item对象
            item = Ir2023Item()
            item['ranking'] = selector.xpath(".//div[@class='pic']/em/text()").extract_first()
            item['name'] = selector.xpath(".//span[@class='title']/text()").extract_first()
            text = selector.xpath(".//div[@class='bd']/p[1]/text()").extract()
            intro = ""
            for s in text:  # 将简介放到一个字符串
                intro += "".join(s.split())  # 去掉空格
            item['introduce'] = intro
            item['star'] = selector.css('.rating_num::text').extract_first()
            item['comments'] = selector.xpath(".//div[@class='star']/span[4]/text()").extract_first()
            item['describe'] = selector.xpath(".//span[@class='inq']/text()").extract_first()
            # print(item)
            yield item  # 将结果item对象返回给Item管道
        # 爬取网页中的下一个页面url信息
        next_link = response.xpath("//span[@class='next']/a[1]/@href").extract_first()
        if next_link:
            next_link = "https://movie.douban.com/top250" + next_link
            print(next_link)
            # 将Request请求提交给调度器
            yield scrapy.Request(next_link, callback=self.parse)