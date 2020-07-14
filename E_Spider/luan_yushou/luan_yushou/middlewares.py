# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from .useragent import USER_AGENT_LIST
import random
from .settings import *
from scrapy.exceptions import NotConfigured
import requests


class LuanYushouSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class LuanYushouDownloaderMiddleware(object):
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


class UserAgentDownloadMiddleware(object):
    def process_request(self, request, spider):
        user_agent = random.choice(USER_AGENT_LIST)
        request.headers['User-Agent'] = user_agent
        spider.logger.debug(user_agent)


class RandomProxyMiddleware(object):
    def __init__(self, settings):
        self.proxies = settings.get("IP_PROXY_LIST")

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('HTTPPROXY_ENABLED'):
            raise NotConfigured

        return cls(crawler.settings)

    def process_request(self, request, spider):
        while 1:
            proxy = 'http://' + random.choice(IP_PROXY_LIST)
            test_result = self.test_url(proxy, spider)
            if not test_result:
                continue
            break
        request.meta["proxy"] = proxy
        spider.logger.debug("-"*120)
        spider.logger.debug(proxy)
        spider.logger.debug("-"*120)

    def process_response(settings, request, response, spider):
        pass

    def process_exception(self, request, exception, spider):
        pass

    def test_url(self, proxy, spider):
        spider.logger.info("TEST PROXY {}".format(proxy))
        test_url = 'http://www.qq.com/'
        try:
            response = requests.get(test_url, proxies={"http":proxy}, timeout=10, verify=False)
            if response.status_code == 200:
                spider.logger.info("PROXY {} AVAILABLE".format(proxy))
                return True
            else:
                return False
        except Exception as e:
            spider.logger.info("PROXY {} NOT AVAILABLE".format(proxy))
            return False
