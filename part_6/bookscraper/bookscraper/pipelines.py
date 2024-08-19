from itemadapter import ItemAdapter

class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Strip all the white spaces from strings (excluding 'description')
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                if isinstance(value, str):  # Ensure value is a string
                    adapter[field_name] = value.strip()
        
        # Convert 'category' and 'product_type' to lowercase
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            if isinstance(value, str):  # Ensure value is a string
                adapter[lowercase_key] = value.lower()
            
        # Convert price fields to float
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            if isinstance(value, str):  # Ensure value is a string
                value = value.replace('£', '').strip()
                try:
                    adapter[price_key] = float(value)
                except ValueError:
                    adapter[price_key] = 0.0  # Default to 0.0 if conversion fails
            
        # Convert 'availability' to the number of books
        availability_strings = adapter.get('availability')
        if isinstance(availability_strings, str):
            split_string_array = availability_strings.split('(')
            if len(split_string_array) < 2:
                adapter['availability'] = 0
            else:
                availability_array = split_string_array[1].split(' ')
                try:
                    adapter['availability'] = int(availability_array[0])
                except ValueError:
                    adapter['availability'] = 0  # Default to 0 if conversion fails
            
        # Convert 'num_reviews' to integer
        num_reviews_string = adapter.get('num_reviews')
        if isinstance(num_reviews_string, str):
            try:
                adapter['num_reviews'] = int(num_reviews_string)
            except ValueError:
                adapter['num_reviews'] = 0  # Default to 0 if conversion fails
        
        # Convert 'stars' to a number
        stars_string = adapter.get('stars')
        if isinstance(stars_string, str):
            split_stars_array = stars_string.split(' ')
            if len(split_stars_array) > 1:
                stars_text_value = split_stars_array[1].lower()
                stars_mapping = {
                    "zero": 0,
                    "one": 1,
                    "two": 2,
                    "three": 3,
                    "four": 4,
                    "five": 5
                }
                adapter['stars'] = stars_mapping.get(stars_text_value, 0)
        
        
        # Update 'img_url' field to include the base URL
        base_url = 'http://books.toscrape.com/'
        img_url = adapter.get('img_url', '')
        if img_url:
            adapter['img_url'] = base_url + img_url.lstrip('.')
        
        return item
