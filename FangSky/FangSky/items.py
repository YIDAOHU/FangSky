# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewHouseItem(scrapy.Item):
    # 省份
    province = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 所在小区
    village_name = scrapy.Field()
    # 房价
    price = scrapy.Field()
    # 户型
    rooms = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 行政区
    district = scrapy.Field()
    # 是否在售
    sale = scrapy.Field()
    # 详情链接
    origin_url = scrapy.Field()

    def get_insert_sql(self):
        """
        存储到MySQL
        """
        insert_sql = """insert into new_house(province, city, village_name, price, rooms, 
                        area,address, district, sale, origin_url)
                        values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        params = (self["province"], self["city"], self["village_name"], self["price"], self["rooms"],
                  self["area"], self["address"], self["district"], self['sale'], self['origin_url'])

        return insert_sql, params


class EsfItem(scrapy.Item):
    # 省份
    province = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 所在小区
    village_name = scrapy.Field()
    # 房价
    price = scrapy.Field()
    # 户型
    rooms = scrapy.Field()
    # 层
    floor = scrapy.Field()
    # 朝向
    toward = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 详情链接
    origin_url = scrapy.Field()
    # 年代
    build_year = scrapy.Field()

    def get_insert_sql(self):
        """
        存储到MySQL
        """
        insert_sql = """insert into second_hand_house(province, city, village_name, price, rooms, floor, toward,
                        area,address, origin_url, build_year)
                        values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        params = (self["province"], self["city"], self["village_name"], self["price"], self["rooms"], self["floor"],
                  self["toward"], self["area"], self["address"],  self['origin_url'], self['build_year'])

        return insert_sql, params
