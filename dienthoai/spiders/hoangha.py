import scrapy
from scrapy import Request


class QuotesSpider(scrapy.Spider):
    name = "hoangha"

    def start_requests(self):
        url = "https://hoanghamobile.com/dien-thoai-di-dong-c14.html?sort=0&p="
        page = ["1","2","3","4","5","6","7","8","9","10"]
        for x in page:
            yield Request(url+x, self.parse)

    def parse(self, response):
        url = "https://hoanghamobile.com"
        url_phones = response.css('a.mosaic-overlay::attr(href)').getall()
        for url_phone in url_phones:
            yield Request(url+url_phone,self.save_info)

    def save_info(self,response):

        link = response.request.url
        start = 0
        # prototypes = response.css('tbody.popup tr').getall()
        item = {}
        name = response.css('section.product-details h1 strong::text').get()
        url_image = response.css('section.product-details div.head-content img::attr(src)').get()
        price_sale = response.css('section.product-details div.head-content div.product-price span::text').get() 
        leght_array = len(response.css('section.product-details div.simple-prop a::text').getall())
        if leght_array==8:
            start = 0
        else:
            start = 1
        display_1 = response.css('section.product-details div.simple-prop a::text').getall()[start]
        display_2 = response.css('section.product-details div.simple-prop a::text').getall()[start+1]
        display = display_1+ ", " + display_2
        os = response.css('section.product-details div.simple-prop a::text').getall()[start+2]
        cpu = response.css('section.product-details div.simple-prop a::text').getall()[start+3]
        ram = response.css('section.product-details div.simple-prop a::text').getall()[start+4]
        camera = response.css('section.product-details div.simple-prop a::text').getall()[start+5]
        rom = response.css('section.product-details div.simple-prop a::text').getall()[start+6]
        pin = response.css('section.product-details div.simple-prop a::text').getall()[start+7]
        # gia_ban = response.css("span.nk-price-final::text").get()
        # item.update({"ten_dien_thoai":ten_dien_thoai})
        item.update({
            "link":link,
            "name":name,
            "url_image":url_image,
            "price_sale":price_sale,
            "display":display,
            "os":os,
            "cpu":cpu,
            "ram":ram,
            "camera":camera,
            "rom":rom,
            "pin":pin

        })
        # item.update({"link":response.url})

        # for prototype in prototypes:
        #     prototype = scrapy.Selector(text=prototype)
        #     title = prototype.css("td.title::text").get()
        #     value = prototype.css("td.value::text").get()
        #     item.update({title:value})

        # he_dieu_hanh = scrapy.Selector(text=response.css("div.productInfo_description li").getall()[3]).css("li::text").get()
        # chipset = scrapy.Selector(text=response.css("div.productInfo_description li").getall()[4]).css("li::text").get()
        # gpu = scrapy.Selector(text=response.css("div.productInfo_description li").getall()[5]).css("li::text").get()
        
        yield item
 
