import scrapy


class AaIndustrialCategorySpider(scrapy.Spider):
    name = "aaindustrial"
    allowed_domains = ["aaindustrial.com.au"]
    start_urls = ["https://www.aaindustrial.com.au/"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seenCategoryLinks = set()

    def parse(self, response):
        topLevelLinks = response.xpath("//*[@id='nav-left']/ul/li/a[@href and not(contains(@href,'#'))]/@href").getall()
        subCategoryLinks = response.xpath("//*[@id='ui-accordion-1-panel-0']/li/a[@href and not(contains(@href,'#'))]/@href").getall()
        subSubCategoryLinks = response.xpath("//*[@id='ui-accordion-ui-accordion-1-panel-0-panel-1']/li/a[@href and not(contains(@href,'#'))]/@href").getall()

        for href in topLevelLinks + subCategoryLinks + subSubCategoryLinks:
            fullHref = response.urljoin(href)
            if fullHref in self.seenCategoryLinks:
                continue
            self.seenCategoryLinks.add(fullHref)
            yield response.follow(fullHref, callback=self.parseCategory, dont_filter=True)

    def parseCategory(self, response):
        topLevelLinks = response.xpath("//*[@id='nav-left']/ul/li/a[@href and not(contains(@href,'#'))]/@href").getall()
        subCategoryLinks = response.xpath("//*[@id='ui-accordion-1-panel-0']/li/a[@href and not(contains(@href,'#'))]/@href").getall()
        subSubCategoryLinks = response.xpath("//*[@id='ui-accordion-ui-accordion-1-panel-0-panel-1']/li/a[@href and not(contains(@href,'#'))]/@href").getall()
        categoryLinks = response.xpath("//a[contains(@href,'/category/') and not(contains(@href,'#'))]/@href").getall()
        for href in topLevelLinks + subCategoryLinks + subSubCategoryLinks + categoryLinks:
            fullHref = response.urljoin(href)
            if fullHref not in self.seenCategoryLinks:
                self.seenCategoryLinks.add(fullHref)
                yield response.follow(fullHref, callback=self.parseCategory, dont_filter=True)

        products = response.xpath(
            "//li[contains(@class,'product') or contains(@class,'item')][.//a[contains(@href,'/product/')]]"
            " | //div[contains(@class,'product-grid') or contains(@class,'products')]//div[contains(@class,'product')][.//a[contains(@href,'/product/')]]"
        )

        for product in products:
            link = product.xpath(".//a[contains(@href,'/product/')][1]/@href").get()
            name = product.xpath(
                "normalize-space((.//a[contains(@href,'/product/')][1]/@title"
                " | .//a[contains(@href,'/product/')][1]/@aria-label"
                " | .//a[contains(@href,'/product/')][1]/@data-name"
                " | .//a[contains(@href,'/product/')][1]//text()"
                " | .//*[contains(@class,'name')][1]//text()"
                " | .//h2[1]//text() | .//h3[1]//text())[1])"
            ).get()
            price = product.xpath(
                "normalize-space(.//*[contains(@class,'price') or contains(@class,'Price') or contains(text(),'$')][1])"
            ).get()
            image = product.xpath(
                "(.//img/@data-src | .//img/@src)[1]"
            ).get()

            productId = None
            if link:
                slug = link.rstrip("/").split("/")[-1]
                productId = slug.split("-")[0]

            item = {
                "productId": productId,
                "skuName": name if name else None,
                "imageUrl": response.urljoin(image) if image else None,
                "priceNow": price if price else None,
                "productUrl": response.urljoin(link) if link else response.url,
            }

            if not item["skuName"] and link:
                yield response.follow(
                    link,
                    callback=self.parseProduct,
                    cb_kwargs={"item": item},
                    dont_filter=True,
                )
            else:
                yield item

        nextPage = response.xpath(
            "//a[contains(@rel,'next') or contains(@class,'next') or contains(translate(normalize-space(text()),'NEXT','next'),'next')]/@href"
        ).get()
        if nextPage:
            yield response.follow(nextPage, callback=self.parseCategory, dont_filter=True)

    def parseProduct(self, response, item):
        name = response.xpath(
            "normalize-space((//*[@id='single-product-details']//h1[1]//text()"
            " | //*[@id='single-product-details']//h2[1]//text()"
            " | //*[@id='single-product-details']//*[@class[contains(.,'name')] or contains(@class,'product-name')][1]//text()"
            " | //meta[@property='og:title']/@content"
            " | //title/text()"
            ")[1])"
        ).get()

        if (not name or name == '') and item.get("productUrl"):
            slug = item["productUrl"].rstrip("/").split("/")[-1]
            name = slug.replace("-", " ")

        if name:
            item["skuName"] = name

        if not item.get("priceNow"):
            detailPrice = response.xpath(
                "normalize-space((//*[@id='single-product-details']//*[contains(@class,'price') or contains(text(),'$')])[1])"
            ).get()
            if detailPrice:
                item["priceNow"] = detailPrice

        if not item.get("imageUrl"):
            detailImage = response.xpath("(//*[@id='single-product-details']//img/@src | //*[@id='single-product-details']//img/@data-src)[1]").get()
            if detailImage:
                item["imageUrl"] = response.urljoin(detailImage)

        yield item
