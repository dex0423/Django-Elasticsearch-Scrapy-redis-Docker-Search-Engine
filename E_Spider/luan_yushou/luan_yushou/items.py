# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(os.path.split(rootPath)[0])
from models.es_type import ArticleType
import elasticsearch
import elasticsearch_dsl
from elasticsearch_dsl.connections import connections


"""
预售信息所有字段由 LuanYushouItem 传递；
存放于一张表中；
最小信息粒度为【房屋】；
"""

es = connections.create_connection(ArticleType)


def gen_suggests(index, info_tuple):
    """
    根据字符串生成搜索建议数组
    :param index:
    :param info_tuple:
    :return:
    """
    used_words = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            # 调用 es 的 analyzer 进口分析字符串
            from elasticsearch_dsl.connections import connections

            # 新建 ES 连接
            # 调用es的analyze接口分析字符串
            words = es.indices.analyze(index=index, body={"filter": ["lowercase"], "text":text})
            anylyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"]) > 1])
            new_words = anylyzed_words - used_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input": list(new_words), "weight": weight})

    return suggests


class LuanYushouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    # 项目名称
    project_name = scrapy.Field()
    # 项目坐落
    position = scrapy.Field()
    # 预售证号
    presale = scrapy.Field()
    # 预售面积
    presale_area = scrapy.Field()
    # 预售套数
    presale_num = scrapy.Field()
    # 批准时间
    permit_date = scrapy.Field()
    # 建筑设计单位
    constrution_designer = scrapy.Field()
    # 环艺设计单位
    green_designer = scrapy.Field()
    # 土地地块号
    land_number = scrapy.Field()
    # 投资立项批准号
    invest_permit = scrapy.Field()
    # 土地出让合同号
    land_transfer_contract = scrapy.Field()
    # 土地取得方式
    get_land_method = scrapy.Field()
    # 土地面积
    land_area = scrapy.Field()
    # 土地使用年限
    land_use_expiration = scrapy.Field()
    # 土地规划用途
    land_usage = scrapy.Field()
    # 土地作用起始日期
    land_startdate = scrapy.Field()
    # 土地作用结束日期
    land_finishdate = scrapy.Field()
    # 技术经济指标
    tech_ecno_index = scrapy.Field()
    # 容积率
    plot_ratio = scrapy.Field()
    # 绿化率
    green_ratio = scrapy.Field()
    # 车位数
    parking_num = scrapy.Field()
    # 交付标准
    delivery_require = scrapy.Field()
    # 周边环境
    position_enviroment = scrapy.Field()
    # 配套设施
    corollary_facility = scrapy.Field()

    # 预售页面的 url
    presale_url = scrapy.Field()
    presale_url_object_id = scrapy.Field()

    crawl_time = scrapy.Field()

    def save_to_es(self):
        # 将 item 数据转换成 es 数据
        arcticle = ArticleType()
        arcticle.project_name = self["project_name"]
        arcticle.position = self["position"]
        arcticle.presale = self["presale"]
        arcticle.presale_area = self["presale_area"]
        arcticle.presale_num = self["presale_num"]
        arcticle.permit_date = self["permit_date"]
        arcticle.constrution_designer = self["constrution_designer"]
        arcticle.green_designer = self["green_designer"]
        arcticle.land_number = self["land_number"]
        arcticle.invest_permit = self["invest_permit"]
        arcticle.land_transfer_contract = self["land_transfer_contract"]
        arcticle.get_land_method = self["get_land_method"]
        arcticle.land_area = self["land_area"]
        arcticle.land_use_expiration = self["land_use_expiration"]
        arcticle.land_usage = self["land_usage"]
        arcticle.land_startdate = self["land_startdate"]
        arcticle.land_finishdate = self["land_finishdate"]
        arcticle.tech_ecno_index = self["tech_ecno_index"]
        arcticle.plot_ratio = self["plot_ratio"]
        arcticle.green_ratio = self["green_ratio"]
        arcticle.delivery_require = self["delivery_require"]
        arcticle.position_enviroment = self["position_enviroment"]
        arcticle.corollary_facility = self["corollary_facility"]
        arcticle.presale_url = self["presale_url"]
        arcticle.presale_url_object_id = self["presale_url_object_id"]
        arcticle.crawl_time = self["crawl_time"]

        arcticle.suggest = gen_suggests(ArticleType.Index.name,
                                            (
                                                (arcticle.project_name, 10),
                                                (arcticle.position, 9),
                                                (arcticle.constrution_designer, 8),
                                                (arcticle.green_designer, 7),
                                                (arcticle.position_enviroment, 6),
                                                (arcticle.corollary_facility, 6)
                                            )
                                        )
            # [{"input":[], "weight":2}]

        arcticle.save()

        return


##############################################################################################

"""
预售信息所有字符由 LuanXianshouProjItem 和 LuanXianshouPresaleItem 传递；
分别存放于两张表中；
LuanXianshouProjItem 字段包括【项目信息】和【统计信息】两大类，信息最小粒度为项目的【栋号】
LuanXianshouPresaleItem 字段包括【项目名称】、【预售信息】、【房屋信息】，信息最小粒度为【房屋】
"""


class LuanXianshouProjItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    # 项目名称
    project_name = scrapy.Field()
    # 项目坐落
    position = scrapy.Field()
    # 建筑设计单位
    constrution_designer = scrapy.Field()
    # 环艺设计单位
    green_designer = scrapy.Field()
    # 土地地块号
    land_number = scrapy.Field()
    # 投资立项批准号
    invest_permit = scrapy.Field()
    # 土地出让合同号
    land_transfer_contract = scrapy.Field()
    # 土地取得方式
    get_land_method = scrapy.Field()
    # 土地面积
    land_area = scrapy.Field()
    # 土地使用年限
    land_use_expiration = scrapy.Field()
    # 土地规划用途
    land_usage = scrapy.Field()
    # 土地作用起始日期
    land_startdate = scrapy.Field()
    # 土地作用结束日期
    land_finishdate = scrapy.Field()
    # 技术经济指标
    tech_ecno_index = scrapy.Field()
    # 容积率
    plot_ratio = scrapy.Field()
    # 绿化率
    green_ratio = scrapy.Field()
    # 车位数
    parking_num = scrapy.Field()
    # 交付标准
    delivery_require = scrapy.Field()
    # 周边环境
    position_enviroment = scrapy.Field()
    # 配套设施
    corollary_facility = scrapy.Field()
    # 栋号
    building = scrapy.Field()
    # 全部套数
    total_room_num = scrapy.Field()
    # 全部面积
    total_room_area = scrapy.Field()
    # 可售套数
    available_room_num = scrapy.Field()
    # 可售面积
    available_room_area = scrapy.Field()
    # 查封套数
    seized_room_num = scrapy.Field()
    # 查封面积
    seized_room_area = scrapy.Field()
    # 抵押套数
    mortgage_room_num = scrapy.Field()
    # 抵押面积
    mortgage_room_area = scrapy.Field()
    # 限制套数
    limited_room_num = scrapy.Field()
    # 限制面积
    limited_room_area = scrapy.Field()
    # 备案套数
    record_room_num = scrapy.Field()
    # 备案面积
    record_room_area = scrapy.Field()
    # 签约套数
    signed_room_num = scrapy.Field()
    # 签约面积
    signed_room_area = scrapy.Field()
    # 回迁套数
    moveback_room_num = scrapy.Field()
    # 回迁面积
    moveback_room_area = scrapy.Field()
    # 自留套数
    retention_room_num = scrapy.Field()
    # 自留面积
    retention_room_area = scrapy.Field()

class LuanXianshouPresaleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    # 项目名称
    project_name = scrapy.Field()
    # 预售证号
    presale = scrapy.Field()
    # 项目坐落
    position = scrapy.Field()
    # 售房单位
    sale_company = scrapy.Field()
    # 房屋用途性质
    usage_type = scrapy.Field()
    # 预售对象
    presale_target = scrapy.Field()
    # 开盘日期
    open_date = scrapy.Field()
    # 预售总建筑面积
    presale_total_area = scrapy.Field()
    # 预售套数
    presale_num = scrapy.Field()
    # 发证机关
    permit_authority = scrapy.Field()
    # 发证日期
    presale_permit_date = scrapy.Field()
    # 预售栋
    presale_building = scrapy.Field()
    # 室号
    room_number = scrapy.Field()
    # 户型
    room_type = scrapy.Field()
    # 套内面积
    room_private_area = scrapy.Field()
    # 建筑面积
    room_construction_area = scrapy.Field()
    # 设计用途
    room_design_usage = scrapy.Field()
    # 层高
    room_floor = scrapy.Field()
    # 状态
    room_status = scrapy.Field()

