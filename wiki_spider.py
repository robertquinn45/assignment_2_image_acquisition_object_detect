import scrapy


class QuotesSpider(scrapy.Spider):
    name = "wiki"
    start_urls = [
        'https://en.wikipedia.org/wiki/Paris',
        'https://en.wikipedia.org/wiki/Livestock',
        'https://en.wikipedia.org/wiki/Sport',
        'https://en.wikipedia.org/wiki/House',
        'https://en.wikipedia.org/wiki/Transport',
        'https://en.wikipedia.org/wiki/Zoo',
        'https://en.wikipedia.org/wiki/Cutlery',
        'https://en.wikipedia.org/wiki/Fruit',
        'https://en.wikipedia.org/wiki/Vegetable',
        'https://en.wikipedia.org/wiki/Furniture',
        'https://en.wikipedia.org/wiki/Food',
        'https://en.wikipedia.org/wiki/Car',
        'https://en.wikipedia.org/wiki/Train',
        'https://en.wikipedia.org/wiki/Boat',
        'https://en.wikipedia.org/wiki/Microwave_oven',
        'https://en.wikipedia.org/wiki/Telephone',
        'https://en.wikipedia.org/wiki/Bicycle',
        'https://en.wikipedia.org/wiki/Motorcycle',
        'https://en.wikipedia.org/wiki/Truck',
        'https://en.wikipedia.org/wiki/Laptop',
        'https://en.wikipedia.org/wiki/Computer',
        'https://en.wikipedia.org/wiki/Football',
        'https://en.wikipedia.org/wiki/Book',
        'https://en.wikipedia.org/wiki/Radio',
        'https://en.wikipedia.org/wiki/Desk',
        'https://en.wikipedia.org/wiki/Traffic_light',
        'https://en.wikipedia.org/wiki/Table_(furniture)',
        'https://en.wikipedia.org/wiki/Toothbrush',
        'https://en.wikipedia.org/wiki/Bottle',
        'https://en.wikipedia.org/wiki/Oven',
        'https://en.wikipedia.org/wiki/Refrigerator',
        'https://en.wikipedia.org/wiki/Suitcase',
        'https://en.wikipedia.org/wiki/Wine_glass',
        'https://en.wikipedia.org/wiki/Doughnut',
        'https://en.wikipedia.org/wiki/Bowl',
        'https://en.wikipedia.org/wiki/Bench_(furniture)',
        'https://en.wikipedia.org/wiki/Airplane'
    ]

    def parse(self, response):
        for img in response.css('.image img'): #('div.quote'):  # ::attr(src)
            yield {
                'src': img.css('img::attr(src)').get(),
                'title': img.css('img::attr(title)').get(),
                'alt': img.css('img::attr(alt)').get()
                #'src': quote.css('span.text::text').get(),
                #'author': quote.css('small.author::text').get(),
                #'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse) # scrapy.Request retruns absolute paths
            
            # response.css('.image img ::attr(src)').getall()
            
                # 'title': img.attrib.get('title', ''),
                # 'alt': img.attrib.get('alt', ''),
                # 'src': img.attrib.get('src', '')
                