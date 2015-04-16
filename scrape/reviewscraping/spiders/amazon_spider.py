import scrapy

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from reviewscraping.items import ReviewItem

class AmazonSpider(CrawlSpider):
    name = "amazon"
    allowed_domains = ["amazon.com"]
    start_urls = [
        "http://www.amazon.com",
        "http://www.amazon.com/books-used-books-textbooks/b/ref=sd_allcat_bo?ie=UTF8&node=283155",
        "http://www.amazon.com/Beauty-Makeup-Skin-Hair-Products/b/ref=sd_allcat_bty?ie=UTF8&node=3760911",
        "http://www.amazon.com/home-garden-kitchen-furniture-bedding/b/ref=sd_allcat_home_storefront?ie=UTF8&node=1055398",
        "http://www.amazon.com/movies-tv-dvd-bluray/b/ref=sd_allcat_mov?ie=UTF8&node=2625373011",
        "http://www.amazon.com/MP3-Music-Download/b/ref=sd_allcat_dmusic?ie=UTF8&node=163856011",
        "http://www.amazon.com/toys/b/ref=sd_allcat_tg?ie=UTF8&node=165793011",
        "http://www.amazon.com/b/ref=sd_allcat_localsvs_home?ie=UTF8&node=10192825011"
    ]

    crawled_product_ids = set()

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
            product_id = full_path.split('/')[5]
            if not product_id in self.crawled_product_ids:
                self.crawled_product_ids.add(product_id)
                yield scrapy.Request(full_path, callback=self.parse)

        # Parse reviews found on page into items
        for sel in response.xpath('//div[contains(concat(\' \', @class, \' \'), \' review \')]'):
            item = ReviewItem()

            item['site_id']       = sel.xpath('@id').extract()[0]
            item['site']          = 'amazon'
            item['stars']         = sel.xpath('.//i[contains(concat(\' \', @class, \' \'), \'review-rating\')]/span/text()').extract()[0]
            item['title']         = sel.xpath('.//a[contains(concat(\' \', @class, \' \'), \'review-title\')]/text()').extract()[0]
            item['text']          = sel.xpath('.//span[contains(concat(\' \', @class, \' \'), \'review-text\')]/text()').extract()[0]
            item['link']          = sel.xpath('.//a[contains(concat(\' \', @class, \' \'), \'review-title\')]/@href').extract()[0]
            item['knowledgeable'] = len(sel.xpath('./span[text()=\'Verified Purchase\']')) == 1

            yield item