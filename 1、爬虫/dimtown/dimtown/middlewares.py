# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse

from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

#####################
# driver下载地址：http://chromedriver.storage.googleapis.com/index.html
# selenium安装： pip install selenium
# seleniumwire安装: pip install selenium-wire
#####################
class DimtownDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        # 处理503的响应
        if response.status == 503:
            response = self.request_through_selenium(request, 'chromedriver_for_chrome114.exe')
        return response

    @staticmethod
    def request_through_selenium(request, driver_path):
        options = webdriver.ChromeOptions()
        # 处理证书错误
        options.add_argument('--ignore-certificate-errors')
        # 修改windows.navigator.webdriver，防机器人识别机制，selenium自动登陆判别机制
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument("--disable-blink-features=AutomationControlled")

        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(request.url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#index_ajax_list li .kzpost-data>a')))

        page_source = driver.page_source

        headers = {}
        for r in driver.requests:
            if 'https://dimtown.com/cosplay' == r.url:
                headers.update(r.headers)
        driver.quit()
        request.headers = headers
        response = HtmlResponse(url=request.url, body=page_source, encoding='utf8', request=request)
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
