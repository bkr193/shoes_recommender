import scrapy

class ShoesSpider(scrapy.Spider):
    name = "shoes"
    start_urls = [
        #type your URL here which you want to parse
    ]

    def parse(self, response):
        for shoe in response.css('div.product-score')[::2]: #getting every second element of the list
            name = shoe.css('a').get()
            rate = shoe.css('div::text').get()
            text_rate = shoe.css('a span.score-text').get()
            reviews_count = shoe.css('a span.reviews-count').get()
            if name is not None:
                if 'NEW' not in rate: #if shoe is rated as 'NEW' it doesn't have also text_rate and reviews so it's unnecessary
                    yield {
                        'name': name.split("/")[1].split('"')[0],
                        'rate': rate.split('\n')[1].lstrip(),
                        'text rate': text_rate.split('>')[1].split('<')[0],
                        'reviews count': reviews_count.split('>')[1].split('<')[0].split(' ')[0] 
                        }
        next_page = response.css('link[rel=next]::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)