# -*- coding: utf-8 -*-
import scrapy
from ..items import LuanXianshouProjItem, LuanXianshouPresaleItem
import re


class LuanYushouSpiderSpider(scrapy.Spider):
    name = 'luan_yushou_spider'
    allowed_domains = ['fcj.luan.gov.cn']
    start_urls = ['http://fcj.luan.gov.cn/laweb/ShowBuild.aspx']

    def parse(self, response):
        project_url_list = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_tbShowList"]/tr/td[2]/table/tr/td/a/@href').extract()
        for project_url in project_url_list:
            project_url = 'http://fcj.luan.gov.cn/laweb/' + project_url
            yield scrapy.Request(url=project_url, callback=self.parse_project)

    def parse_project(self, response):
        xianshou_proj_item = LuanXianshouProjItem()
        project_name = response.xpath('//*[@id="ProjectName"]/text()').extract_first()
        xianshou_proj_item['project_name'] = project_name
        xianshou_proj_item['position'] = response.xpath('//*[@id="ProjectAddress"]/text()').extract_first()
        xianshou_proj_item['constrution_designer'] = response.xpath('//*[@id="ProjectDesignCompany"]/text()').extract_first()
        xianshou_proj_item['property_manager'] = response.xpath('//*[@id="EstateManageCompany"]/text()').extract_first()
        xianshou_proj_item['green_designer'] = response.xpath('//*[@id="EnvironmentArtsDesignCompany"]/text()').extract_first()
        xianshou_proj_item['land_number'] = response.xpath('//*[@id="LandNo"]/text()').extract_first()
        xianshou_proj_item['invest_permit'] = response.xpath('//*[@id="AuthorizeNo"]/text()').extract_first()
        xianshou_proj_item['land_transfer_contract'] = response.xpath('//*[@id="LandUseCertNo"]/text()').extract_first()
        xianshou_proj_item['get_land_method'] = response.xpath('//*[@id="LandGetMode"]/text()').extract_first()
        xianshou_proj_item['land_area'] = response.xpath('//*[@id="LandArea"]/text()').extract_first()
        xianshou_proj_item['land_use_expiration'] = response.xpath('//*[@id="LandUseLimit"]/text()').extract_first()
        xianshou_proj_item['land_usage'] = response.xpath('//*[@id="LandUse"]/text()').extract_first()
        xianshou_proj_item['land_startdate'] = response.xpath('//*[@id="LandUseBeginDate"]/text()').extract_first()
        xianshou_proj_item['land_finishdate'] = response.xpath('//*[@id="LandUseEndDate"]/text()').extract_first()
        xianshou_proj_item['tech_ecno_index'] = response.xpath('//*[@id="Memo"]/text()').extract_first()
        xianshou_proj_item['plot_ratio'] = response.xpath('//*[@id="CubageRate"]/text()').extract_first()
        xianshou_proj_item['green_ratio'] = response.xpath('//*[@id="GreenRate"]/text()').extract_first()
        xianshou_proj_item['parking_num'] = response.xpath('//*[@id="ParkingNum"]/text()').extract_first()
        xianshou_proj_item['delivery_require'] = response.xpath('//*[@id="DeliveStandard"]/text()').extract_first()
        xianshou_proj_item['position_enviroment'] = response.xpath('//*[@id="AroundEnvironment"]/text()').extract_first()
        xianshou_proj_item['corollary_facility'] = response.xpath('//*[@id="Establishment"]/text()').extract_first()

        static_url = 'http://fcj.luan.gov.cn/laweb/' + response.xpath('//*[@id="ctl00_ContentPlaceHolder1_tdProjectSum"]/a/@href').extract_first()
        yield scrapy.Request(url=static_url, callback=self.parse_static, meta={'item': xianshou_proj_item})

        presale_urls = response.xpath('//*[@id="aspnetForm"]/center/div/table[2]/tbody/tr/td[1]/table/tbody/tr[5]/td/table/tbody/tr/td[2]/a/@href').extract()
        for presale_url in presale_urls:
            xianshou_presale_item = LuanXianshouPresaleItem()
            xianshou_presale_item['project_name'] = project_name
            presale_url = 'http://fcj.luan.gov.cn/' + presale_url
            yield scrapy.Request(url=presale_url, callback=self.parse_presale, meta={'meta': xianshou_presale_item})

    def parse_static(self, response):
        xianshou_proj_item = response.meta['item']
        buildings = response.xpath('//*[@id="form1"]/div[2]/table/tr[3]/td/table/tr/td[1]/text()').extract()
        total_room_nums = response.xpath('//*[@id="form1"]/div[2]/table/tr[3]/td/table/tr/td[2]/text()').extract()
        total_room_areas = response.xpath('//*[@id="form1"]/div[2]/table/tr[3]/td/table/tr/td[3]/text()').extract()
        available_room_nums = response.xpath('//*[@id="form1"]/div[2]/table/tr[3]/td/table/tr/td[4]/text()').extract()
        available_room_areas = response.xpath('//*[@id="form1"]/div[2]/table/tr[3]/td/table/tr/td[5]/text()').extract()
        seized_room_nums = response.xpath('//*[@id="form1"]/div[2]/table/tr[3]/td/table/tr/td[6]/text()').extract()
        seized_room_areas = response.xpath('//*[@id="form1"]/div[2]/table/tr[3]/td/table/tr/td[7]/text()').extract()
        mortgage_room_nums = response.xpath('//*[@id="form1"]/div[2]/table/tr[3]/td/table/tr/td[8]/text()').extract()
        mortgage_room_areas = response.xpath('//*[@id="form1"]/div[2]/table/tr[3]/td/table/tr/td[9]/text()').extract()
        limited_room_nums = response.xpath('//*[@id="form1"]/div[2]/table/tr[3]/td/table/tr/td[10]/text()').extract()
        limited_room_areas = response.xpath('//*[@id="form1"]/div[2]/table/tr[3]/td/table/tr/td[11]/text()').extract()
        record_room_nums = response.xpath('//*[@id="form1"]/div[2]/table/tr[3]/td/table/tr/td[12]/text()').extract()
        record_room_areas = response.xpath('//*[@id="form1"]/div[2]/table/tr[3]/td/table/tr/td[13]/text()').extract()
        signed_room_nums = response.xpath('//*[@id="form1"]/div[2]/table/tr[3]/td/table/tr/td[14]/text()').extract()
        signed_room_areas = response.xpath('//*[@id="form1"]/div[2]/table/tr[3]/td/table/tr/td[15]/text()').extract()
        moveback_room_nums = response.xpath('//*[@id="form1"]/div[2]/table/tr[3]/td/table/tr/td[16]/text()').extract()
        moveback_room_areas = response.xpath('//*[@id="form1"]/div[2]/table/tr[3]/td/table/tr/td[17]/text()').extract()
        retention_room_nums = response.xpath('//*[@id="form1"]/div[2]/table/tr[3]/td/table/tr/td[18]/text()').extract()
        retention_room_areas = response.xpath('//*[@id="form1"]/div[2]/table/tr[3]/td/table/tr/td[19]/text()').extract()

        for i in range(len(buildings)):
            xianshou_proj_item['building'] = buildings[i]
            xianshou_proj_item['total_room_num'] = total_room_nums[i]
            xianshou_proj_item['total_room_area'] = total_room_areas[i]
            xianshou_proj_item['available_room_num'] = available_room_nums[i]
            xianshou_proj_item['available_room_area'] = available_room_areas[i]
            xianshou_proj_item['seized_room_num'] = seized_room_nums[i]
            xianshou_proj_item['seized_room_area'] = seized_room_areas[i]
            xianshou_proj_item['mortgage_room_num'] = mortgage_room_nums[i]
            xianshou_proj_item['mortgage_room_area'] = mortgage_room_areas[i]
            xianshou_proj_item['limited_room_num'] = limited_room_nums[i]
            xianshou_proj_item['limited_room_area'] = limited_room_areas[i]
            xianshou_proj_item['record_room_num'] = record_room_nums[i]
            xianshou_proj_item['record_room_area'] = record_room_areas[i]
            xianshou_proj_item['signed_room_num'] = signed_room_nums[i]
            xianshou_proj_item['signed_room_area'] = signed_room_areas[i]
            xianshou_proj_item['moveback_room_num'] = moveback_room_nums[i]
            xianshou_proj_item['moveback_room_area'] = moveback_room_areas[i]
            xianshou_proj_item['retention_room_num'] = retention_room_nums[i]
            xianshou_proj_item['retention_room_area'] = retention_room_areas[i]

            yield xianshou_proj_item

    def parse_presale(self, response):
        xianshou_presale_item = response.meta['item']
        xianshou_presale_item['presale'] = response.xpath('//*[@id="证书编号"]/text()').extract_first()
        xianshou_presale_item['position'] = response.xpath('//*[@id="房地坐落"]/text()').extract_first()
        xianshou_presale_item['sale_company'] = response.xpath('//*[@id="预售单位"]/text()').extract_first()
        xianshou_presale_item['usage_type'] = response.xpath('//*[@id="性质"]/text()').extract_first()
        xianshou_presale_item['presale_target'] = response.xpath('//*[@id="预售对象"]/text()').extract_first()
        xianshou_presale_item['open_date'] = response.xpath('//*[@id="开盘日期"]/text()').extract_first()
        xianshou_presale_item['presale_total_area'] = response.xpath('//*[@id="预售总建筑面积"]/text()').extract_first()
        xianshou_presale_item['presale_num'] = response.xpath('//*[@id="预售套数"]/text()').extract_first()
        xianshou_presale_item['permit_authority'] = response.xpath('//*[@id="发证机关"]/text()').extract_first()
        xianshou_presale_item['presale_permit_date'] = response.xpath('//*[@id="发证日期"]/text()').extract_first()
        xianshou_presale_item['presale_building'] = response.xpath('//*[@id="txtDong"]/a/text()').extract_first()

        presale_building_url = 'http://fcj.luan.gov.cn/laweb/Web' + response.xpath('//*[@id="txtDong"]/a/@href').extract_first()[2:]

        yield scrapy.Request(url=presale_building_url, callback=self.parse_room, meta={'item': item})
        # pass

    def parse_room(self, response):
        item = response.meta['item']
        rooms = response.xpath('//*[@id="Room1__room_map_"]/tr/td/@title').extract()
        rooms_status = response.xpath('//*[@id="Room1__room_map_"]/tr/td/@style').extract()
        for i in len(rooms):
            room = rooms[i]
            room_status_color = re.search(r'background-color:.*?;', rooms_status[i]).group().replace('background-color:', '').replace(';', '')
            if '室号' in room:
                item['room_number'] = re.search(r'室号：.*?户型', room).group().replace('室号：', '').replace('户型', '')
                item['room_type'] = re.search(r'户型：.*?室内面积', room).group().replace('户型：', '').replace('室内面积', '')
                item['room_private_area'] = re.search(r'套内面积：.*?建筑面积', room).group().replace('套内面积：', '').replace('建筑面积', '')
                item['room_construction_area'] = re.search(r'建筑面积：.*?设计用途', room).group().replace('建筑面积：', '').replace('设计用途', '')
                item['room_design_usage'] = re.search(r'设计用途.*?层高', room).group().replace('设计用途：', '').replace('层高', '')
                item['room_floor'] = re.search(r'层高.*?', room).group().replace('层高', '').strip()
                if room_status_color == '#F0FFB6':
                    item['room_status'] = '可售'
                elif room_status_color == '#FFFF66':
                    item['room_status'] = '预定'
                elif room_status_color == '#82B4FF':
                    item['room_status'] = '签约'
                elif room_status_color == '#96E686':
                    item['room_status'] = '备案'
                elif room_status_color == '#E5E5E5':
                    item['room_status'] = '自留'
                elif room_status_color == '#FFCCFF':
                    item['room_status'] = '回迁'
                elif room_status_color == '#CC3399':
                    item['room_status'] = '抵押'
                elif room_status_color == '#Salmon':
                    item['room_status'] = '政府回购'
                elif room_status_color == '#FF0000':
                    item['room_status'] = '查封'
                elif room_status_color == '#6666CC':
                    item['room_status'] = '限制'
                elif room_status_color == '#7030A0':
                    item['room_status'] = '处理'
                elif room_status_color == '#FF8D00':
                    item['room_status'] = '不可售'
                elif room_status_color == '#00822D':
                    item['room_status'] = '已执行'
                elif room_status_color == '#CFE1E9':
                    item['room_status'] = '历史遗留'
                elif room_status_color == '#646464':
                    item['room_status'] = '其他'
                else:
                    item['room_status'] = ''

                yield item