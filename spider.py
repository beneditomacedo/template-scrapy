import time
import scrapy
from scrapy.crawler import CrawlerProcess


class DC_Description_Spider(scrapy.Spider):
    name = "dc_chapter_spider"

    def start_requests(self):
        urls = ["https://assets.datacamp.com/production/repositories/2560/datasets/19a0a26daa8d9db1d920b5d5607c19d6d8094b3b/all_short"]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_front)

    def parse_front(self, response):
        course_blocks = response.css('div.course-block')
        course_links = course_blocks.xpath('./a/@href')
        links_to_follow = course_links.extract()

        for url in links_to_follow:
            yield response.follow(url=url, callback=self.parse_pages)

    def parse_pages(self, response):
        # Create a SelectorList of the course titles text
        crs_title = response.xpath('//h1[contains(@class,"title")]/text()')
        # Extract the text and strip it clean
        crs_title_ext = crs_title.extract_first().strip()
        # Create a SelectorList of course descriptions text
        crs_descr = response.css('p.course__description::text')
        # Extract the text and strip it clean
        crs_descr_ext = crs_descr.extract_first().strip()
        # Fill in the dictionary
        dc_dict[crs_title_ext] = crs_descr_ext


# Initialize the dictionary **outside** of the Spider class
dc_dict: dict[str, str] = {}

# Run the Spider
process = CrawlerProcess({'LOG_LEVEL': 'CRITICAL'})
process.crawl(DC_Description_Spider)
process.start()

time.sleep(5)

for key, value in dc_dict.items():
    print(key)
    print(value)
    print("===============================")
