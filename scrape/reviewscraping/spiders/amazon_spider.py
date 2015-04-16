import scrapy

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from reviewscraping.items import ReviewItem

class AmazonSpider(CrawlSpider):
    name = "amazon"
    allowed_domains = ["amazon.com"]
    start_urls = [
        "http://www.amazon.com"
    ]

    crawled_product_ids = set()

    # rules = (
    #     #Rule(LinkExtractor(allow='.*/product/.*', deny=['.*/product/images/.*', '.*/e/.*'])),
    #     Rule(LinkExtractor(allow='.*/dp/B0.*')),
    #     Rule(LinkExtractor('.*/product-reviews/.*'), callback='parse_item'),
    # )

    def parse(self, response):
        # Follow links to get to product reviews

        for link in response.xpath('//span[@class=\'crAvgStars\']/a'):
            rel_path = link.xpath('@href').extract()[0]
            full_path = "http://www.amazon.com" + rel_path
            yield scrapy.Request(rel_path, callback=self.parse)

        # Follow links to more product reviews
        for link in response.xpath('//a[contains(text(), \'Next\') and contains(@href, \'/product-reviews/\')]'):
            rel_path = link.xpath('@href').extract()[0]
            full_path = "http://www.amazon.com" + rel_path
            yield scrapy.Request(full_path, callback=self.parse)

        # Follow links to products
        for link in response.xpath('//a[contains(@href, \'/product/\')]'):
            rel_path = link.xpath('@href').extract()[0]
            full_path = "http://www.amazon.com" + rel_path
            #print full_path
            product_id = full_path.split('/')[5]
            print product_id
            if not product_id in self.crawled_product_ids:
                self.crawled_product_ids.add(product_id)
                yield scrapy.Request(full_path, callback=self.parse)

        # Parse reviews found on page into items
        for sel in response.xpath('//div[contains(concat(\' \', @class, \' \'), \' review \')]'):
            item = ReviewItem()

            item['site_id']       = sel.xpath('@id').extract()
            item['site']          = 'amazon'
            item['stars']         = sel.xpath('.//i[contains(concat(\' \', @class, \' \'), \'review-rating\')]/span/text()').extract()
            item['title']         = sel.xpath('.//a[contains(concat(\' \', @class, \' \'), \'review-title\')]/text()').extract()
            item['text']          = sel.xpath('.//span[contains(concat(\' \', @class, \' \'), \'review-text\')]/text()').extract()
            item['link']          = sel.xpath('.//a[contains(concat(\' \', @class, \' \'), \'review-title\')]/@href').extract()
            item['knowledgeable'] = len(sel.xpath('./span[text()=\'Verified Purchase\']')) == 1

            yield item

    def parse_item(self, response):
        items = []
        reviews = response.xpath('//div[contains(concat(\' \', @class, \' \'), \' review \')]')

        for sel in reviews:
            item = ReviewItem()

            item['site_id'] = sel.xpath('@id').extract()
            item['site']    = 'amazon'
            item['stars']   = sel.xpath('.//i[contains(concat(\' \', @class, \' \'), \'review-rating\')]/span/text()').extract()
            item['title']   = sel.xpath('.//a[contains(concat(\' \', @class, \' \'), \'review-title\')]/text()').extract()
            item['text']    = sel.xpath('.//span[contains(concat(\' \', @class, \' \'), \'review-text\')]/text()').extract()
            item['link']    = sel.xpath('.//a[contains(concat(\' \', @class, \' \'), \'review-title\')]/@href').extract()

            items.append(item)

        return items
