import scrapy
from scrapy import Request
import re


class QuotesSpider(scrapy.Spider):
    name = "fpt"

    def start_requests(self):
        url = 'https://fptshop.com.vn/'
        yield Request(url, self.parse)

    def parse(self, response):
        url = 'https://fptshop.com.vn'
        # cates = response.css("header.fs-header div.fs-mntd1 ul").extract_first()
        cates = scrapy.Selector(text=response.css("header.fs-header div.fs-mntd1 ul").extract_first())
        for cate in cates.css("li").getall():
            url_cate = url+scrapy.Selector(text=cate).css("a::attr(href)").get()
            yield Request(url_cate,self.crawl)
            # yield {
            #     "url_phone":url_cate
            # }

    def crawl(self,response):
        url = 'https://fptshop.com.vn'
        urls_phones = response.css("div.fs-lpil a.fs-lpil-img::attr(href)").getall()
        for url_phone in urls_phones:
            yield Request(url+url_phone,self.save_info)
            
    def save_info(self,response):
        link = response.request.url
        name = response.css("h1::text").get()
        price_sale = response.css("p.fs-dtprice ::text").get()
        price_origin = response.css("p.fs-dtprice del::text").get()
        url_image = response.css("div.fs-dtslb img::attr(src)").get()
        display = scrapy.Selector(text=response.css("div.fs-tsright li").getall()[0]).css("span::text").get()
        camera_selfie = scrapy.Selector(text=response.css("div.fs-tsright li").getall()[1]).css("span::text").get()
        camera = scrapy.Selector(text=response.css("div.fs-tsright li").getall()[2]).css("span::text").get()+' '
        ram = scrapy.Selector(text=response.css("div.fs-tsright li").getall()[3]).css("span::text").get()
        ram = "".join(re.findall("[0-9]", ram))

        rom = scrapy.Selector(text=response.css("div.fs-tsright li").getall()[4]).css("span::text").get()
        rom = "".join(re.findall("[0-9]", rom))

        cpu = scrapy.Selector(text=response.css("div.fs-tsright li").getall()[5]).css("span::text").get()
        gpu = scrapy.Selector(text=response.css("div.fs-tsright li").getall()[6]).css("span::text").get()
        pin = scrapy.Selector(text=response.css("div.fs-tsright li").getall()[7]).css("span::text").get()
        os = scrapy.Selector(text=response.css("div.fs-tsright li").getall()[8]).css("span::text").get()
        sim = scrapy.Selector(text=response.css("div.fs-tsright li").getall()[9]).css("span::text").get()
        yield {
            "url_image":url_image,
            "price_origin":price_origin,
            "link":link,
            "name":name,
            "price_sale":price_sale,
            "display":display,
            "camera":camera+" "+camera_selfie,
            # "camera_selfie":camera_selfie,
            "ram":ram,
            "rom":rom,
            "cpu":cpu,
            "gpu":gpu,
            "pin":pin,
            "os":os,
            "sim":sim
        }
 
