from scrapy import cmdline

if __name__ == '__main__':
    # cmdline.execute('scrapy crawl cosplay'.split())
    cmdline.execute('scrapy crawl cosplay -s JOBDIR=crawls/cosplay'.split())
