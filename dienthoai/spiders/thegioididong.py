import scrapy
from scrapy import Request
import re


class QuotesSpider(scrapy.Spider):
    name = "thegioididong"

    def start_requests(self):
        url = 'https://www.thegioididong.com/dtdd-apple-iphone'
        yield Request(url, self.parse)

    def parse(self, response):
        url = 'https://www.thegioididong.com'
        for producer in response.css('div.manunew a::attr(href)').getall():
            if(producer!="/dtdd-apple-iphone"):
                url_producer = url+producer
                yield Request(url_producer, self.scrawl)
            else:
                for href_phone_item in response.css('ul.homeproduct li a::attr(href)').getall():
                    url_phone_item = url+href_phone_item
                    yield Request(url_phone_item, self.save_info)

    def scrawl(self,response):
        url = 'https://www.thegioididong.com'
        for href_phone_item in response.css('ul.homeproduct li a::attr(href)').getall():
            url_phone_item = url+href_phone_item
            yield Request(url_phone_item, self.save_info)

        #     yield Request(
        #         url=url_phone_item,
        #         callback=self.save_info,
        #         meta={
        #             "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
        #     },
        # )
    # script = """
    #         function main(splash)
    #             local url = splash.args.url
    #             assert(splash:go(url))
    #             assert(splash:wait(0.5))
    #             assert(splash:runjs("$('.viewparameterfull').click();"))
    #             return {
    #                 html = splash:html(),
    #                 url = splash:url(),
    #             }
    #         end
    #         """
    def save_info(self,response):
        status = response.css('span.labelstatus::text').get()
        name = response.css('div.rowtop h1::text').get()
        url_image = response.css('div.rowdetail aside.picture img::attr(src)').get()
        price_sale = response.css("div.rowdetail aside.price_sale div.area_price strong::text").get()
        price_origin = response.css("div.rowdetail aside.price_sale div.area_price span::text").get()
        display_1 = response.css("div.box_content ul.parameter li.g6459_79_77 a::text").getall()
        display_2 = response.css("div.box_content ul.parameter li.g6459_79_77 div::text").getall()
        display = "".join(display_1+display_2)
        os = response.css("div.box_content ul.parameter li.g72 div a::text").get()
        camera = response.css("div.box_content ul.parameter li.g27 div::text").get()
        camera_selfie = response.css("div.box_content ul.parameter li.g29 div::text").get()
        cpu = response.css("div.box_content ul.parameter li.g6059 a::text").get()
        ram = response.css("div.box_content ul.parameter li.g50 div::text").get()
        ram = "".join(re.findall("[0-9]", ram))

        rom = response.css("div.box_content ul.parameter li.g49 div::text").get()
        rom = "".join(re.findall("[0-9]", rom))

        sim = ", ".join(response.css("div.box_content ul.parameter li.g6339_6463 div.isim a::text").getall())
        pin_1 = response.css("div.box_content ul.parameter li.g84_10882 div::text").getall()
        pin_2 = response.css("div.box_content ul.parameter li.g84_10882 a::text").getall()
        pin = "".join(pin_1+pin_2)
        link = response.request.url
        if(price_sale):
             yield {
                "link":link,
                "name": name,
                "url_image":url_image,
                "price_sale":price_sale,
                "price_origin":price_origin,
                "display":display,
                "os":os,
                "camera":camera,
                "camsera_selfie":camera_selfie,
                "cpu":cpu,
                "ram":ram,
                "rom":rom,
                "sim":sim,
                "pin":pin
            }
        else:
            array_price = []
            memories = response.css("div.rowdetail aside.price_sale div.memory a span::text").getall()
            prices = response.css("div.rowdetail aside.price_sale div.memory a strong::text").getall()
            for index in range(len(memories)):
                array_price.append({"memory":memories[index],"price":prices[index]})
            yield {
                "link":link,
                "name": name,
                "url_image":url_image,
                "price":array_price,
                "display":display,
                "os":os,
                "camera":camera,
                "camera_selfie":camera_selfie,
                "cpu":cpu,
                "ram":ram,
                "rom":rom,
                "sim":sim,
                "pin":pin
            }
        