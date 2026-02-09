import sys
import asyncio

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Now import and run scrapy
from scrapy.cmdline import execute
execute(["scrapy", "runspider", "question2.py", "-o", "aaIndustrialProducts.json"])
