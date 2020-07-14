# -*- coding: utf-8 -*-
import scrapy
from ..items import LuanYushouItem
import re
import time
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(os.path.split(rootPath)[0])
from utils.common import get_md5


class LuanYushouSpiderSpider(scrapy.Spider):
    name = 'luan_yushou_spider'
    allowed_domains = ['fcj.luan.gov.cn']
    start_urls = ['http://fcj.luan.gov.cn/laweb/Web/PreSellInfo/ShowPreSellCertList.aspx']

    def parse(self, response):
        project_name_list = response.xpath('//*[@id="form1"]/table[2]/tr/td/table[1]/tr/td[1]/a/text()').extract()
        project_url_list = response.xpath('//*[@id="form1"]/table[2]/tr/td/table[1]/tr/td[1]/a/@href').extract()
        position_list = response.xpath('//*[@id="form1"]/table[2]/tr/td/table[1]/tr/td[2]/a/text()').extract()
        presale_list = response.xpath('//*[@id="form1"]/table[2]/tr/td/table[1]/tr/td[3]/a/text()').extract()
        presale_url_list = response.xpath('//*[@id="form1"]/table[2]/tr/td/table[1]/tr/td[3]/a/@href').extract()
        presale_area_list = response.xpath('//*[@id="form1"]/table[2]/tr/td/table[1]/tr/td[4]/text()').extract()
        presale_num_list = response.xpath('//*[@id="form1"]/table[2]/tr/td/table[1]/tr/td[5]/text()').extract()
        permit_date_list = response.xpath('//*[@id="form1"]/table[2]/tr/td/table[1]/tr/td[6]/text()').extract()
        for i in range(1, len(project_name_list)):
            item = LuanYushouItem()
            item['project_name'] = project_name_list[i].replace('\r', '').replace('\n', '').strip()
            item['position'] = position_list[i].replace('\r', '').replace('\n', '').strip()
            item['presale'] = presale_list[i].replace('\r', '').replace('\n', '').strip()
            item['presale_area'] = presale_area_list[i].replace('\r', '').replace('\n', '').strip()
            item['presale_num'] = presale_num_list[i].replace('\r', '').replace('\n', '').strip()
            item['permit_date'] = permit_date_list[i].replace('\r', '').replace('\n', '').strip()

            project_url = 'http://fcj.luan.gov.cn/laweb/Web' + project_url_list[i].replace('\r', '').replace('\n', '').strip()[2:]
            presale_url = 'http://fcj.luan.gov.cn/laweb/Web/PreSellInfo' + presale_url_list[i].replace('\r', '').replace('\n', '').strip()[2:]
            item['presale_url'] = presale_url
            item['presale_url_object_id'] = get_md5(presale_url)

            yield scrapy.Request(url=project_url, callback=self.parse_project, meta={'item': item})
            # yield scrapy.Request(url=presale_url, callback=self.parse_presale, meta={'item': item})

        total_page = response.xpath('//*[@id="AspNetPager1"]/table/tr/td[1]/b[2]/text()').extract_first().replace('/', '')
        __VIEWSTATE = response.xpath('//*[@id="__VIEWSTATE"]/@value').extract_first()
        __EVENTTARGET = 'AspNetPager1'
        current_page = response.xpath('//*[@id="AspNetPager1"]/table/tr/td[1]/b[2]/font/text()').extract_first()
        AspNetPager1_input = str(current_page)
        __EVENTARGUMENT = str(int(current_page) + 1)
        if int(current_page) <= int(total_page):
            url = 'http://fcj.luan.gov.cn/laweb/Web/PreSellInfo/ShowPreSellCertList.aspx'
            form_data = {
                '__VIEWSTATE': __VIEWSTATE,
                '__EVENTTARGET': __EVENTTARGET,
                '__EVENTARGUMENT': __EVENTARGUMENT,
                'AspNetPager1_input': AspNetPager1_input
            }
            yield scrapy.FormRequest(url=url, formdata=form_data, callback=self.parse)

    def parse_project(self, response):
        item = response.meta['item']
        item['constrution_designer'] = response.xpath('//*[@id="ProjectDesignCompany"]/text()').extract_first()
        item['green_designer'] = response.xpath('//*[@id="EnvironmentArtsDesignCompany"]/text()').extract_first()
        item['land_number'] = response.xpath('//*[@id="LandNo"]/text()').extract_first()
        item['invest_permit'] = response.xpath('//*[@id="AuthorizeNo"]/text()').extract_first()
        item['land_transfer_contract'] = response.xpath('//*[@id="LandUseCertNo"]/text()').extract_first()
        item['get_land_method'] = response.xpath('//*[@id="LandGetMode"]/text()').extract_first()
        item['land_area'] = response.xpath('//*[@id="LandArea"]/text()').extract_first()
        land_use_expiration =  response.xpath('//*[@id="LandUseLimit"]/text()').extract_first()
        if land_use_expiration:
            item['land_use_expiration'] = land_use_expiration.replace("年", "")
        else:
            item['land_use_expiration'] = ""
        item['land_usage'] = response.xpath('//*[@id="LandUse"]/text()').extract_first()
        item['land_startdate'] = response.xpath('//*[@id="LandUseBeginDate"]/text()').extract_first()
        item['land_finishdate'] = response.xpath('//*[@id="LandUseEndDate"]/text()').extract_first()
        item['tech_ecno_index'] = response.xpath('//*[@id="Memo"]/text()').extract_first()
        item['plot_ratio'] = response.xpath('//*[@id="CubageRate"]/text()').extract_first()
        item['green_ratio'] = response.xpath('//*[@id="GreenRate"]/text()').extract_first()
        item['parking_num'] = response.xpath('//*[@id="ParkingNum"]/text()').extract_first()
        item['delivery_require'] = response.xpath('//*[@id="DeliveStandard"]/text()').extract_first()
        item['position_enviroment'] = response.xpath('//*[@id="AroundEnvironment"]/text()').extract_first()
        item['corollary_facility'] = response.xpath('//*[@id="Establishment"]/text()').extract_first()
        item['crawl_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        yield item

