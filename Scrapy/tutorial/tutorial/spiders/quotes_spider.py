import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    # this is the short way to generate a scrapyRequest object
    # the default implementation of start_requests() is used this way
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        # 'http://quotes.toscrape.com/page/2/'
    ]
    # below is the "long way" for generating scrapy.Request objects
    # def start_requests(self):
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/'
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        # response.follow uses href attributes automatically, so you can simply pass the <a> element
        for a in response.css('li.next a'):
            yield response.follow(a, callback=self.parse)
        
        # below are slower ways of doing the same thing as above    
        # next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)
            # this is a slower way of doing the above. using response.follow lets you use relative urls
            # next_page = response.urljoin(next_page)
            # yield scrapy.Request(next_page, callback=self.parse)
        
        # this is allows you to pass a selector directly to response.follow instead of a string
        # for href in response.css('li.next a::attr(href)'):
        #     yield response.follow(href, callback=self.parse)

        

    # def parse(self, response):
    #     page = response.url.split('/')[-2]
    #     filename = 'quotes-%s.html' % page
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #     self.log('Saved file %s' % filename)