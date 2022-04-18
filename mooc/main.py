from scrapy import cmdline

spiders = [
    'scrapy crawl mooc'
]

cmdline.execute(spiders.split())