# -*- coding: utf-8 -*-
import scrapy
import re
from renting.items import RentingItem
from renting import tools
from scrapy_redis.spiders import RedisSpider

image_pattern = re.compile(r'//(.*?).png')
price_pattern = re.compile(r':-(.*?)px')


class ZiroomspiderSpider(RedisSpider):
    name = 'ziroomspider'
    redis_key = "renting:start_url"

    # 获取每个城市不同价位租房链接
    def parse(self, response):
        item = RentingItem()
        # 按照所属地区爬取链接
        span_url = response.xpath(
            '//ul[@class="f-box"]/li[1]/div[@class="opt"]/div[@class="opt-type active"]/div[@class="grand-child-opt"]/span[@class="item"]'
        )
        item["city"] = response.xpath('//dt[@class="Z_city_name"]/text()').extract()[0]
        item["area"] = response.xpath('//div[@class="f-res"]/div[@class="ct"]/a[1]/text()').extract()[0]
        for span in span_url:
            area_url = span.xpath('.//span[@class="checkbox-group"]/a')
            for url in area_url:
                street_url = "http:" + url.xpath('./@href').extract()[0]
                item["street"] = url.xpath('./text()').extract()[0]
                yield scrapy.Request(street_url, callback=self.get_page, meta={'item': item})

    # 获取不同地区租房每一页的链接
    def get_page(self, response):
        item = response.request.meta['item']
        url = response.url
        has_page = response.xpath('//div[@class="Z_pages"]')
        if len(has_page.xpath('.//a')):
            page_num = int(has_page.xpath('.//a[last()-1]/text()').extract()[0])
            for i in range(1, page_num + 1):
                page_url = url[:-1] + "-p{}/".format(i)
                yield scrapy.Request(page_url, callback=self.get_link, meta={'item': item})
        else:
            yield scrapy.Request(url, callback=self.get_link, meta={'item': item})

    # 爬取每一页每个租房信息的链接
    def get_link(self, response):
        item = response.request.meta['item']
        room_list = response.xpath('//div[@class="Z_list-box"]/div')
        for room in room_list:
            url = room.xpath('.//div[@class="pic-box"]/a/@href')
            if len(url):
                room_url = "http:" + url.extract()[0]
                yield scrapy.Request(room_url, callback=self.get_datas, meta={'item': item})
                # yield scrapy.Request(room_url, callback=self.get_datas)
            else:
                continue

    # 获取数据
    def get_datas(self, response):
        item = response.request.meta['item']
        # item = RentingItem()
        # 获取租房标题
        item["title"] = response.xpath('//aside[@class="Z_info_aside"]/h1/text()').extract()[0]
        # 获取租房面积
        item["acreage"] = response.xpath('//div[@class="Z_home_info"]/div/dl[1]/dd/text()').extract()[0]
        # 获取租房朝向
        item["toward"] = response.xpath('//div[@class="Z_home_info"]/div/dl[2]/dd/text()').extract()[0]
        # 获取租房户型
        item["room_type"] = response.xpath('//div[@class="Z_home_info"]/div/dl[3]/dd/text()').extract()[0]
        # 获取租房所在位置
        item["position"] = response.xpath('//ul[@class="Z_home_o"]/li[1]/span[@class="va"]/span/text()').extract()[0]
        # 获取租房价格
        image_list = response.xpath('//div[@class="Z_price"]/i')
        image_url = str(image_list[0].xpath('./@style').extract()[0])
        image_url = "http:" + re.search(image_pattern, image_url).group()
        tools.get_image(image_url)
        num_string = tools.img_discern("price.png")
        price = ""
        for i in image_list:
            image_url = str(i.xpath('./@style')[0])
            price += num_string[int(float(re.search(price_pattern, image_url).group(1)) / 31.24)]
        item["price"] = price
        # 楼层高度
        item["storey"] = response.xpath('//ul[@class="Z_home_o"]/li[2]/span[@class="va"]/text()').extract()[0]
        # 是否有电梯
        item["elevator"] = response.xpath('//ul[@class="Z_home_o"]/li[3]/span[@class="va"]/text()').extract()[0]
        # 房屋建筑时间
        item["build_time"] = response.xpath('//ul[@class="Z_home_o"]/li[4]/span[@class="va"]/text()').extract()[0]
        # 暖气/门锁
        item["heating"] = response.xpath('//ul[@class="Z_home_o"]/li[5]/span[@class="va"]/text()').extract()[0]
        # 绿化程度
        item["afforest"] = response.xpath('//ul[@class="Z_home_o"]/li[6]/span[@class="va"]/text()').extract()[0]
        # 房屋简介
        item["simple_info"] = response.xpath('//div[@class="Z_rent_desc"]/text()').extract()[0].strip()
        print(item["city"], item["area"], item["street"])
        print(item["title"], item["acreage"], item["toward"], item["room_type"], item["position"], item["price"])
        print(item["storey"], item["elevator"], item["build_time"], item["heating"], item["afforest"])
        print(item["simple_info"])
        yield item
