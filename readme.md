# Scrapy

## Part-2

### If virtual env isn't install in the machine then install it.

```
$ pip install virtualenv
```

### Make a virtual directory of the scrapy project

```
$ python -m venv venv
```

### Start the virtual environment

```
$ source venv/bin/activate
```

## Part-3

### Create a scrapy project

```
$ scrapy startproject ProjectName
```

Scrapy will make ProjectName/ProjectName/spider directory. Navigate into the child directory. In the spider directory ProjectNameSpider.py file is the main file.

## Part-4

A spider need to be made in this part. Navigate into the spider folder of the ProjectName.

### Make a spider for the project

```
$ scrapy genspider NameOfTheSpider simple-URL-without-the-http.com
```

A spider is now made. In the ProjectName/ProjectName/spider/NameOfTheSpider.py the base code is made along with the spider. This is the main file.

For the case of ipython in the shell, ipython needed to download.

```
$ pip install ipython
```

In the ProjectName/scrapy.cfg,

```
[settings]
default = bookscraper.settings
shell= ipython <-- this line is added
```

Now the scrapy project can use ipython in the shell.

To start the shell

```
$ scrapy shell
```

### Fetch the website in the shell

```
$ fetch ('url along with http://')
```

### 'response' is a object that contain the info from the website

```
$ response
```

### 'response' can target the css and its attribute

```
$ response.css(h1.title)
```

### Targeting the books.toscrape.com

```
$ response.css('article.product_pod')
```

Above code will return an array of all the matches.

### Getting a single book

```
$ response.css('article.product_pod').get()
```

### Storing the array in a variable and checking the length

```
$ books = response.css('article.product_pod')
$ len(books)
```

### Getting the name for first book

```
$ book1 = books[0]
$ book1.css('h3 a::text').get()
```

### Getting the next page button

```
$ next_page = response.css('li.next a ::attr(href)').get()
```

### Lets make a crawler now


### bookspider.py file
```python
import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            yield{
                'name': book.css('h3 a::text').get(),
                'price': book.css('.product_price .price_color::text').get(),
                'url': book.css('h3 a').attrib['href']
            }

            next_page = response.css('li.next a ::attr(href)').get()

            if next_page is not None:
                if 'catalogue/' in next_page:
                    next_page_url = 'http://books.toscrape.com/' + next_page
                else:
                    next_page_url = 'http://books.toscrape.com/catalogue/' + next_page
                yield response.follow(next_page_url,callback = self.parse)
```

### Let's execute the crawler to get the data in the terminal
```
$ scrapy crawl bookspider
```

### Save the data in json or csv
```
$ scrapy crawl bookspider -O BookData.json
```

## Part-5
Modify the spider file so that the output will give details of books from their individual details page.

### bookspider.py file
```python
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
```

Also apply bellow command to save the data
```
$ scrapy crawl bookspider -O BookData.json
```