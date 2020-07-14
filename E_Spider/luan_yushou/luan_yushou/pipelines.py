# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from .items import LuanYushouItem, LuanXianshouProjItem, LuanXianshouPresaleItem

import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(os.path.split(rootPath)[0])
from models.es_type import ArticleType
from twisted.enterprise import adbapi
import pymysql

class DefaultValuesPipeline(object):
    def process_item(self, item, spider):
        '''
        设置需要抓取的字符串的默认字符为 NULL 空值
        :param item:
        :param spider:
        :return:
        '''
        for field in item.fields:
            item.setdefault(field, 'null')
        return item


class LuanYushouPipeline(object):
    def process_item(self, item, spider):
        if item.__class__ == LuanYushouItem:
            if len(item) == 40:
                write_into_csv('yushou_project_info', item)
        elif item.__class__ == LuanXianshouProjItem:
            if len(item) == 39:
                write_into_csv('xianshou_project_info', item)
        elif item.__class__ == LuanXianshouPresaleItem:
            if len(item) == 19:
                write_into_csv('xianshou_presale_info', item)

        return item


import csv

def write_into_csv(file_name, item):
    '''
    :params file_name: csv 文件路径名
    :params item: 要写入的数据，注意是 dict 字典格式
    '''
    with open('{}.csv'.format(file_name), 'a', newline='', encoding='utf-8-sig') as csv_file_writer:
        writer = csv.writer(csv_file_writer)
        with open('{}.csv'.format(file_name), 'r', encoding='utf-8-sig') as csv_file_reader:
            reader = csv.reader(csv_file_reader)
            rows = [row for row in reader]
            # 如果第一行为空则写入第一行标题
            if not rows:
                writer.writerow(item.keys())
            # 如果数据已经存在表格中则不写入数据
            if list(item.values()) in rows:
                 print('item already exist in csv : {}'.format(item))
            else:
                print('item save csv : {}'.format(item))
                writer.writerow(item.values())


class ElasticsearchPipeline(object):
    def process_item(self, item, spider):
        item.save_to_es()
        return item


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            port=settings["MYSQL_PORT"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            db=settings["MYSQL_DBNAME"],
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
            cp_reconnect=True,
        )
        # 注意调用的是adb.ConnectionPool()、而不是adb.Connection()
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步插入
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 处理异常
        query.addErrback(self.handle_error, item, spider)

        return item

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        #  执行具体的插入
        #  根据不同的item 构建不同的sql语句并插入到mysql中
        # 方法一
        # if item.__class__.__name__ == "JobBoleArticleItem"
        # 方法二
        # 利用Django中的model模式、写一个专门实现get_insert_sql()的函数

        # insert_sql, params = item.get_insert_sql()
        # cursor.execute(insert_sql, params)

        insert_sql = """
            insert into article(title, url, create_date, fav_nums)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_sql, (item["title"], item["url"], item["create_date"], item["fav_nums"]))

        # 已自动提交，不需要再提交了