import sys
import asyncio
import os

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from scrapy.cmdline import execute
execute(['scrapy', 'runspider', 'question4.py', '-o', 'liquorLegendsProducts.json', '-a', 'storeId=66'])
