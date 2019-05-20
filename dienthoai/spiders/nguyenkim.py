import scrapy
from scrapy import Request


class QuotesSpider(scrapy.Spider):
    name = "nguyenkim"

    def start_requests(self):
        urls = [
            'https://www.nguyenkim.com/dien-thoai-di-dong/page-1/',
            'https://www.nguyenkim.com/dien-thoai-di-dong/page-2/',
            'https://www.nguyenkim.com/dien-thoai-di-dong/page-3/',
            'https://www.nguyenkim.com/dien-thoai-di-dong/page-4/'
        ]
        for url in urls:
            yield Request(url, self.parse)

    def parse(self, response):
        yield {"url":response.request.url}

    # def crawl(self,response):
    #     url = 'https://fptshop.com.vn'
    #     urls_phones = response.css("div.fs-lpil a.fs-lpil-img::attr(href)").getall()
    #     for url_phone in urls_phones:
    #         yield Request(url+url_phone,self.save_info)
            
   
 
