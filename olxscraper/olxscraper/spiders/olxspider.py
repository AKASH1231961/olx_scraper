import scrapy
from urllib.parse import urlparse


class OLXSpider(scrapy.Spider):
    name = "olx"
    allowed_domains = ["olx.in"]
    start_urls = [
        "https://www.olx.in/kozhikode_g4058877/for-rent-houses-apartments_c1723"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    # "playwright_include_page": True,
                    "playwright_page_methods": [
                        {
                            "method": "wait_for_selector",
                            "args": ['li[data-aut-id="itemBox"]'],
                        }
                    ],
                },
                callback=self.parse,
            )

    def parse(self, response):
        for product in response.xpath('//li[starts-with(@data-aut-id, "itemBox")]'):
            link = response.urljoin(product.xpath(".//a[@href]/@href").get())

            # passing listing info to details page
            yield scrapy.Request(
                url=link,
                callback=self.parse_details,
                meta={
                    "playwright": True,
                },
            )
        # #Handling pagination (next page )
        next_page = response.xpath('//a[@data-aut-id="arrowRight"]/@href').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            parsed = urlparse(next_page_url)
            if "olx.in" in parsed.netloc and "page=" in next_page_url:
                yield scrapy.Request(
                    url=next_page_url,
                    callback=self.parse,
                    meta={
                        "playwright": True,
                        # "playwright_include_page":True,
                        "playwright_abort_request": ["bam.nr-data.net", "v.clarity.ms"],
                        "playwright_page_methods": [
                            {
                                "method": "wait_for_selector",
                                "args": ['li[data-aut-id="itemBox"]'],
                            }
                        ],
                    },
                )

    def parse_details(self, response):
        ad_id = response.xpath(
            './/div[@class="_1-oS0"]/strong[contains(., "AD ID")]/text()[3]'
        ).get()
        bathrooms = response.xpath(
            '//span[@data-aut-id="value_bathrooms"]/text()'
        ).get()
        try:
            bathrooms = int(bathrooms) if bathrooms else None
        except ValueError:
            bathrooms = None
        bedrooms = response.xpath('//span[@data-aut-id="value_rooms"]/text()').get()
        try:
            bedrooms = int(bedrooms) if bedrooms else None
        except ValueError:
            bedrooms = None
        item = {
            "property_name": response.xpath(
                './/h1[@data-aut-id="itemTitle"]/text()'
            ).get(),
            "property_id": ad_id,
            "breadcrumbs": response.xpath(
                '//ol[@class="rui-2Pidb"]/li/a/text()'
            ).getall(),
            "price": response.xpath('.//span[@data-aut-id="itemPrice"]/text()').get(),
            "image_url": response.xpath('.//div[@class="_23Jeb"]//img/@src').get(),
            "description": response.xpath(
                './/div[@data-aut-id="itemDescriptionContent"]/p/text()'
            ).get(),
            "seller_name": response.xpath(
                '//div[@data-aut-id="userTitle"]/span[last()]/text()'
            ).get(),
            "location": response.xpath('//span[@class="_1RkZP"]/text()').get(),
            "property_type": response.xpath(
                '//span[@data-aut-id="value_type"]/text()'
            ).get(),
            "bathrooms": bathrooms,
            "bedrooms": bedrooms,
        }
        yield item
