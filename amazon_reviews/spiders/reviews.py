import scrapy


class ReviewsSpider(scrapy.Spider):
    name = "reviews"
    allowed_domains = ["www.amazon.in"]
    start_urls = ["https://www.amazon.in/Bose-Quietcomfort-Bluetooth-Headphones-Cancelling/product-reviews/B098FKXT8L/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"]

    def parse(self, response):
        pass
