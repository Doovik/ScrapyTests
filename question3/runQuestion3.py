import sys
import asyncio

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from scrapy.cmdline import execute
execute(['scrapy', 'runspider', 'question3.py', '-o', 'liquorLegendsStores.json'])
