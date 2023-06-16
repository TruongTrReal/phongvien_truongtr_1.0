import scrapy
from demo.items import VietstockItem

class VietstockSpider(scrapy.Spider):
    name = 'vietstock'
    allowed_domains = ['vietstock.vn']
    start_urls = ['https://vietstock.vn/']
    #scrapy shell https://vietstock.vn/

    def parse(self, response):
        news = response.css('div.single_post_text')
        for new in news:
            relative_url = new.css('h4 a').attrib['href']
            url = 'https://vietstock.vn' + relative_url
            yield scrapy.Request(url, callback=self.parse_new_page)

        # Find all the link in the navbar and follow them
        nav_links = response.css('li.has-sub')
        for nav_link in nav_links:
            relative_url = nav_link.css('a').attrib['href']
            next_url = 'https://vietstock.vn' + relative_url
            yield response.follow(next_url, callback=self.parse)


    #Go to each New and get full New article, time and image
    def parse_new_page(self, response):
        new = response.css("div.article-content")[0]
        imgages = new.css("img").getall()
        vietstock_item = VietstockItem()

        vietstock_item['url'] = response.url,
        vietstock_item['title'] = new.css("h1.article-title ::text").get(),

        brief = new.css("p.pHead ::text").get(),
        content_array = new.css("p.pBody ::text").getall(),
        vietstock_item['content'] = brief[0] + ' '.join(content_array[0])

        vietstock_item['imgage_link'] = [imgage.split('src="')[1].split('"')[0] for imgage in imgages[:3]],
        vietstock_item['summarized'] = False
        yield vietstock_item
        

# run spider and save to json file: scrapy crawl vietstock -o vietstock.json
# start virtual environment: .\venv\Scripts\activate
