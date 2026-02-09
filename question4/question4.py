import sys
import asyncio

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import string
from urllib.parse import urljoin

import scrapy


class LiquorLegendsProductsSpider(scrapy.Spider):
    name = "liquorLegendsProducts"
    allowed_domains = ["rewardsapi.liquorlegends.com.au", "liquorlegends.com.au"]

    def __init__(self, storeId: str = "66", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storeId = str(storeId)
        self.seenSlugs = set()
        self.searchTerms = list(string.ascii_lowercase) + [str(n) for n in range(10)]

    def start_requests(self):
        base = "https://rewardsapi.liquorlegends.com.au/api/v1/product-search/{store}?currentUser=0&search={term}"
        for term in self.searchTerms:
            url = base.format(store=self.storeId, term=term)
            yield scrapy.Request(url, callback=self.parseSearch, cb_kwargs={"term": term}, dont_filter=True)

    def parseSearch(self, response, term: str):
        products = response.json() if response.headers.get("Content-Type", b"").startswith(b"application/json") else []
        for product in products or []:
            slug = product.get("slug")
            productId = product.get("plu")
            if not slug or slug in self.seenSlugs:
                continue
            self.seenSlugs.add(slug)

            productUrl = f"https://liquorlegends.com.au/product/{slug}?outlet={self.storeId}"
            yield response.follow(
                productUrl,
                callback=self.parseProduct,
                cb_kwargs={"productId": productId, "slug": slug}
            )

    def parseProduct(self, response, productId: str, slug: str):
        price = response.xpath("//span[@itemprop='price']/@content | //meta[@itemprop='price']/@content").get()
        if not price:
            price = response.xpath("normalize-space(//span[@itemprop='price'])").get()

        imageUrl = response.xpath(
            "//meta[@itemprop='image']/@content | //div[contains(@class,'product__image')]//img/@src | //img[@itemprop='image']/@src"
        ).get()
        skuName = response.xpath("//meta[@itemprop='name']/@content | //h1/text()").get()

        yield {
            "productId": productId,
            "skuName": skuName.strip() if skuName else None,
            "imageUrl": urljoin(response.url, imageUrl) if imageUrl else None,
            "priceNow": price.strip() if price else None,
            "productUrl": response.url,
            "storeId": self.storeId
        }
