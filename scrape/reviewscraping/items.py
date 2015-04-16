import scrapy

class ReviewItem(scrapy.Item):
    title = scrapy.Field()
    site = scrapy.Field()
    site_id = scrapy.Field()
    link = scrapy.Field()
    text = scrapy.Field()
    stars = scrapy.Field()
    knowledgeable = scrapy.Field()