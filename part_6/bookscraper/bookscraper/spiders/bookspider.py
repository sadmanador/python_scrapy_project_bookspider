import scrapy
from bookscraper.items import BookItem

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
        
        
        book_items = BookItem()
        book_items['upc']= table_row[0].css('td::text').get()
        book_items['title']=response.css('div.product_main h1::text').get()
        book_items['url']= response.url
        book_items['img_url'] = response.css('.thumbnail img::attr(src)').get()
        book_items['price']= response.css('p.price_color::text').get()
        book_items['product_type']= table_row[1].css('td::text').get()
        book_items['price_excl_tax'] =  table_row[2].css('td::text').get()
        book_items['price_incl_tax']= table_row[3].css('td::text').get()
        book_items['tax']= table_row[4].css('td::text').get()
        book_items['availability']= table_row[5].css('td::text').get()
        book_items['num_reviews']= table_row[6].css('td::text').get()
        book_items['stars']= response.css('p.star-rating').attrib['class']
        book_items['category']= response.xpath("//ul[@class='breadcrumb']/li[3]/a/text()").get()
        book_items['description']= response.xpath("//div[@id='product_description']/following-sibling::p/text()").get()
        
        yield book_items
        