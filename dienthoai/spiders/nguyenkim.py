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
        phones = response.css("a.nk-link-product::attr(href)").extract()
        for phone in phones:
            yield Request(phone,self.save_info)
            
    # def crawl(self,response):
    #     url = 'https://fptshop.com.vn'
    #     urls_phones = response.css("div.fs-lpil a.fs-lpil-img::attr(href)").getall()
    #     for url_phone in urls_phones:
    #         yield Request(url+url_phone,self.save_info)
            
    def save_info(self,response):
        prototypes = response.css('tbody.popup tr').getall()
        item = {}
        ten_dien_thoai = response.css("h1::text").get()
        gia_ban = response.css("span.nk-price-final::text").get()
        item.update({"ten_dien_thoai":ten_dien_thoai})
        item.update({"gia_ban":gia_ban})
        item.update({"link":response.url})

        for prototype in prototypes:
            prototype = scrapy.Selector(text=prototype)
            title = prototype.css("td.title::text").get()
            value = prototype.css("td.value::text").get()
            item.update({title:value})

        # he_dieu_hanh = scrapy.Selector(text=response.css("div.productInfo_description li").getall()[3]).css("li::text").get()
        # chipset = scrapy.Selector(text=response.css("div.productInfo_description li").getall()[4]).css("li::text").get()
        # gpu = scrapy.Selector(text=response.css("div.productInfo_description li").getall()[5]).css("li::text").get()
        
        yield item
 
