import requests
import re
from lxml import etree
from renting import tools

# image_pattern = re.compile(r'//(.*?).png')
# price_pattern = re.compile(r':-(.*?)px')

with open("city.txt", "r", encoding="utf-8") as fp:
    url_list = fp.read().strip().split("\n")

for url in url_list:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
    }
    print(url)
    response = requests.get(url, headers=headers)
    content = response.text
    # with open("ziroom.html", "w", encoding="utf-8") as fp:
    #     fp.write(content)
    tree = etree.HTML(content)
    href_list = tree.xpath('//ul[@class="f-box"]/li[1]/div[@class="opt"]/div[1]/div[@class="child-opt"]/div/a')
    print(href_list)
    for href in href_list:
        area_url = href.xpath('./@href')[0]
        with open("area.txt", "a", encoding="utf-8") as fp:
            fp.write("http:"+area_url+"\n")

# title = tree.xpath('//aside[@class="Z_info_aside"]/h1/text()')[0]
# area = tree.xpath('//div[@class="Z_home_info"]/div/dl[1]/dd/text()')[0]
# toward = tree.xpath('//div[@class="Z_home_info"]/div/dl[2]/dd/text()')[0]
# room_type = tree.xpath('//div[@class="Z_home_info"]/div/dl[3]/dd/text()')[0]
# position = tree.xpath('//ul[@class="Z_home_o"]/li[1]/span[@class="va"]/span/text()')[0]
# image_list = tree.xpath('//div[@class="Z_price"]/i')
# image_url = str(image_list[0].xpath('./@style')[0])
# image_url = "http:" + re.search(image_pattern, image_url).group()
# tools.get_image(image_url)
# num_string = tools.img_discern("price.png")
# price = ""
# floor = tree.xpath('//ul[@class="Z_home_o"]/li[2]/span[@class="va"]/text()')[0]
# elevator = tree.xpath('//ul[@class="Z_home_o"]/li[3]/span[@class="va"]/text()')[0]
# build_time = tree.xpath('//ul[@class="Z_home_o"]/li[4]/span[@class="va"]/text()')[0]
# heating = tree.xpath('//ul[@class="Z_home_o"]/li[5]/span[@class="va"]/text()')[0]
# afforest = tree.xpath('//ul[@class="Z_home_o"]/li[6]/span[@class="va"]/text()')[0]
# simple_info = tree.xpath('//div[@class="Z_rent_desc"]/text()')[0].strip()
# for i in image_list:
#     image_url = str(i.xpath('./@style')[0])
#     price += num_string[int(float(re.search(price_pattern, image_url).group(1))/31.24)]
#
# print(title, area, toward, room_type, position, price, floor, elevator, build_time, heating, afforest, simple_info)
