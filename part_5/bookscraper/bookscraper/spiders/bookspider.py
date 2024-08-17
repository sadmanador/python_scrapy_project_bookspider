import scrapy

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    def parse(self, response):
        books = response.css('article.product_pod')
        
        for book in books:
            relative_url = book.css('h3 a::attr(href)').get()
            
            if 'catalogue/' in relative_url:
                book_url = 'http://books.toscrape.com/' + relative_url
            else:
                book_url = 'http://books.toscrape.com/catalogue/' + relative_url
            yield response.follow(book_url, callback=self.parse_book_page)
           
        next_page = response.css('li.next a::attr(href)').get() 
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'http://books.toscrape.com/' + next_page
            else:
                next_page_url = 'http://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url, callback=self.parse)
            
    def parse_book_page(self, response):
        table_row = response.css('table tr')
        
        yield {
            "title": response.css('div.product_main h1::text').get(),
            "imgUrl": response.css('.thumbnail img::attr(src)').get(),
            "url": response.url,
            'product_type': table_row[1].css('td::text').get(),
            'price': response.css('p.price_color::text').get(),
            'price_excl_tax': table_row[2].css('td::text').get(),
            'price_incl_tax': table_row[3].css('td::text').get(),
            'tax': table_row[4].css('td::text').get(),
            'availability': table_row[5].css('td::text').get(),
            'num_views': table_row[6].css('td::text').get(),
            'star': response.css('p.star-rating').attrib['class'],
            'category': response.xpath("//ul[@class='breadcrumb']/li[3]/a/text()").get(),
            'description': response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
        }
