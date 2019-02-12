# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class AmazonProductItems(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    company = scrapy.Field()
    product_rating = scrapy.Field()
    num_reviews = scrapy.Field()
    prices = scrapy.Field()
    asin = scrapy.Field()
    product_url = scrapy.Field()
    all_reviews_url = scrapy.Field()

class AmazonReviewsItems(scrapy.Item):
    asin = scrapy.Field()
    reviewers_id = scrapy.Field()
    reviews_title = scrapy.Field()
    reviews_date = scrapy.Field()
    reviews_rating = scrapy.Field()
    reviews_text = scrapy.Field()
  
