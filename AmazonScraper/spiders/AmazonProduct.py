import scrapy
from scrapy import Spider
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from AmazonScraper.items import AmazonProductItems
import re

class AmazonProduct(Spider):
    name = 'AmazonProduct'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics/ref=zg_bs_nav_0'
        ]
    
    
    def parse(self, response):
        # Extracting all product urls, calling request, then parsing product info from the product pages returned
        product_url= response.xpath('//span[@class="aok-inline-block zg-item"]/a[@class="a-link-normal"]/@href').extract()
        product_urls = [] 
        for url in product_url:
            absolute_url = response.urljoin(url)
            product_urls.append(absolute_url)
            yield Request(absolute_url, callback = self.parse_product_info, meta= {'product_url' : product_urls})

        # Extracting 'See all reviews' URL calling request then extractin reviews info with parse_reviews function
        #all_reviews_url = response.xpath('//a[@class="a-size-small a-link-normal"]/@href').extract()  
        #for url in all_reviews_url:
         #   absolute_url = response.urljoin(url)
          #  yield Request(absolute_url, callback = self.parse_reviews)


    def parse_product_info(self, response):
        Item = AmazonProductItems()
        product_url = response.meta['product_url']
        Item['product_url'] = product_url
        # Extracting product information from product page
        title = response.xpath('//span[@id="productTitle"]/text()').extract()
        title = title[0].replace('\n','') 
        Item['title'] = title.strip()

        # Name of the fulfilling company
        Item['company'] = response.xpath('//a[@id="bylineInfo"]/text()').extract()

        # Overall product rating 
        product_rating= response.xpath('//div[@id="averageCustomerReviews_feature_div"]//span[@class="a-icon-alt"]/text()').extract()

        # Handling exceptions ('Out of range index') due to absence of value returning 'null' instead
        try:
            product_rating = product_rating[0]
        except IndexError:
            product_rating = 'null'
        Item['product_rating'] = product_rating.replace('out of 5 stars','')

        num_reviews = response.xpath('//div[@id="averageCustomerReviews_feature_div"]//span[@id="acrCustomerReviewText"]/text()').extract()          
        Item['num_reviews'] = num_reviews[0].replace('customer reviews','') 

        # Extracting price and handling out of range index errors
        price = response.xpath('//span[@id="priceblock_ourprice"]/text()').extract()
        try:
            prices = price[0]
        except IndexError:
            prices = 'null'
       
        Item['prices'] = prices.replace('$','')

        # Extracting ASIN and stripping leading and ending spaces
        #asin = response.xpath('//th[contains(text(),"ASIN")]/following-sibling::td/txt()').extract()
        

        # Extracting all reviews URLs to parse reviews all product reviews next
        all_reviews_url = response.xpath('//a[@class="a-link-emphasis a-text-bold"]/@href').extract()
        Item['all_reviews_url'] =  all_reviews_url
        asin = re.findall('B0.{8}', all_reviews_url[0])
        asin = asin[0].replace('\n','')
        Item['asin'] = asin.strip()

        yield Item
        



