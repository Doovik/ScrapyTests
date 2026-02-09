import sys
import asyncio
import json
import scrapy

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())




class LiquorLegendsStoresSpider(scrapy.Spider):
    name = "liquorLegendsStores"
    allowed_domains = ["rewardsapi.liquorlegends.com.au"]
    start_urls = ["https://rewardsapi.liquorlegends.com.au/api/v1/venue/geo-json"]

    def parse(self, response):
        payload = response.json()
        features = payload.get("features", []) if isinstance(payload, dict) else []

        for feature in features:
            props = feature.get("properties", {}) or {}
            locationDataStr = props.get("location_data", "{}")
            
            try:
                locationData = json.loads(locationDataStr) if isinstance(locationDataStr, str) else locationDataStr
            except:
                locationData = {}
            
            store = locationData.get("store_details", {}) or {}

            yield {
                "storeId": store.get("htmassist_id") or store.get("outlet_id"),
                "storeName": store.get("store_name") or store.get("hotel_name"),
                "storeAddress": props.get("address"),
                "storeSuburb": props.get("suburb"),
                "storePostcode": props.get("postcode"),
                "storeState": props.get("state")
            }
