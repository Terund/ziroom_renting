# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RentingItem(scrapy.Item):
    # define the fields for your item here like:
    city = scrapy.Field()  # 房源城市
    area = scrapy.Field()  # 房源地区
    street = scrapy.Field()  # 房源街道
    title = scrapy.Field()  # 房源标题
    acreage = scrapy.Field()  # 房间大小
    toward = scrapy.Field()  # 房间朝向
    room_type = scrapy.Field()  # 房间户型
    position = scrapy.Field()  # 房间所在位置
    price = scrapy.Field()  # 租房的价格
    storey = scrapy.Field()  # 租房的楼层高度
    elevator = scrapy.Field()  # 租房是否有电梯
    build_time = scrapy.Field()  # 租房的建筑时间
    heating = scrapy.Field()  # 租房的暖气/门锁设施
    afforest = scrapy.Field()  # 租房附近小区的绿化程度
    simple_info = scrapy.Field()  # 租房的简介
