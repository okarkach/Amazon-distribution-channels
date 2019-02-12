import re
import scrapy
from scrapy import Spider
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from AmazonScraper.items import AmazonReviewsItems
from AmazonScraper.items import AmazonProductItems
import pandas as pd

class AmazonReviews(Spider):
    name = 'AmazonReviews'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/']
        
    
     #Calling requests on previously scraped urls and parsing reviews content 
    def parse(self, response):
        Reviews = AmazonReviews()
        Items = AmazonProductItems()
        # Extracting all product urls, calling request, then parsing product info from the product pages returned
        product_info = pd.read_csv('/Users/samk/Box/scrapers/amazon.com/AmazonScraper/ProductInfo_electronics.csv')
        product_reviews_url= product_info['all_reviews_url']
        for url in product_reviews_url:
            absolute_url = response.urljoin(url)
            yield Request(absolute_url, callback = self.parse_reviews)
            next_page_url = response.xpath('//li[@class="a-last"]//a/@href').extract_first()
            if next_page_url:
                yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)

    #Function parsing all reviews in Url request
    def parse_reviews(self, response):
        Reviews = AmazonReviewsItems()
        #reviews_dict = {}
        asin_link = response.xpath('//li[@class="a-last"]//a/@href').extract_first()
        asin = re.findall("B0.{8}", asin_link)
        Reviews['asin'] = asin
        reviewers_id = []
        reviews_rating = []
        reviews_date = []
        reviews_title = []
        reviews_text = []
        # Looping through review blocks, exctrating the content, and appending it to lists
        for i in range(9):
            reviewer_id = response.xpath('//span[@class="a-profile-name"]/text()').extract()[2+i] #skipping the first 2 reviews as they present in body
            
            review_rating = response.xpath('//div[@id="cm_cr-review_list"]/div[@class="a-section review"]/div[@class="a-row a-spacing-none"]/div[@class="a-section celwidget"]/div[@class="a-row"]/a[@class="a-link-normal"]/i[@data-hook="review-star-rating"]/span[@class="a-icon-alt"]/text()').extract()[i]
            #review_rating = [rating.replace('out of 5 stars','') for rating in review_rating]
            review_rating = review_rating.replace('out of 5 stars','')
            review_title = response.xpath('//a[@class="a-size-base a-link-normal review-title a-color-base a-text-bold"]/text()').extract()[i]  
            review_date =  response.xpath('//span[@class="a-size-base a-color-secondary review-date"]/text()').extract()[2+i]
        
        # Extracting review text and handling <br> to include all text then move to the next review
            reviews = response.xpath('(//span)[@class="a-size-base review-text"]') 
            review_text = [reviews.xpath('string(.)').extract() for review in reviews] 
            review_text = review_text[i]
           
            reviewers_id.append(reviewer_id)
            reviews_rating.append(review_rating)
            reviews_date.append(review_date)
            reviews_title.append(review_title)
            reviews_text.append(review_text)

            Reviews['reviewers_id'] = reviewers_id
            Reviews['reviews_rating'] = reviews_rating
            Reviews['reviews_title'] = reviews_title
            Reviews['reviews_date'] = reviews_date
            Reviews['reviews_text'] = reviews_text 
           #reviewers_id.append(reviewer_id)
            #reviews_rating.append(review_rating)
           # reviews_date.append(review_date)
            #reviews_title.append(review_title)
           # reviews_text.append(review_text)

        next_page_url = response.xpath('//li[@class="a-last"]//a/@href').extract_first()
        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse_reviews)
    
        yield   Reviews
        


        

