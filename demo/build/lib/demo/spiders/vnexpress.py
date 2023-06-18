import scrapy
from demo.items import VietstockItem

class VnexpressSpider(scrapy.Spider):
    name = "vnexpress"
    allowed_domains = ["vnexpress.net"]
    start_urls = ["https://vnexpress.net/kinh-doanh/"]

    def parse(self, response):
        news = response.css('h2.title-news')
        for new in news:
            relative_url = new.css('a').attrib['href']
            url = relative_url
            yield scrapy.Request(url, callback=self.parse_new_page)

        # Find all the link in the navbar and follow them
        nav_links = [
            'kinh-doanh/quoc-te',
            'kinh-doanh/doanh-nghiep',
            'kinh-doanh/chung-khoan',
            'kinh-doanh/vi-mo',
            'kinh-doanh/hang-hoa',
            'bat-dong-san/chinh-sach',
            'bat-dong-san/thi-truong',
            'bat-dong-san/du-an',
            'phap-luat',
        ]
        for nav_link in nav_links:
            relative_url = nav_link
            next_url = 'https://vnexpress.net/' + relative_url
            yield response.follow(next_url, callback=self.parse)


    #Go to each New and get full New article, time and image
    def parse_new_page(self, response):
        new = response.css("div.sidebar-1")[0]
        imgages = new.css("img").getall()
        vietstock_item = VietstockItem()

        vietstock_item['url'] = response.url,
        vietstock_item['title'] = str(new.css("h1.title-detail ::text").get()),

        brief = new.css("p.description ::text").get(),
        content_array = new.css("p.Normal ::text").getall(),
        vietstock_item['content'] = brief[0] + ' '.join(content_array[0])

        vietstock_item['imgage_link'] = None,
        vietstock_item['summarized'] = False
        yield vietstock_item
        
#  scrapy crawl vnexpress -o vnexpress.json
# end environment: deactivate