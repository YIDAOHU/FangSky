# -*- coding: utf-8 -*-

import scrapy
import re
from FangSky.items import NewHouseItem, EsfItem


class FangSpider(scrapy.Spider):
    name = 'fang'
    allowed_domains = ['fang.com']
    start_urls = ['http://www.fang.com/SoufunFamily.htm']

    def parse(self, response):
        trs = response.xpath('//div[@class="outCont"]//tr')
        province = None
        for tr in trs:
            tds = tr.xpath('.//td[not(@class)]')
            province_td = tds[0]
            province_text = province_td.xpath('.//text()').get()
            province_text = re.sub(r"\s", "", province_text)
            if province_text:
                province = province_text
            if province == '其它':
                continue
            city_td = tds[1]
            city_links = city_td.xpath('.//a')
            for city_link in city_links:
                city = city_link.xpath('.//text()').get()
                city_url = city_link.xpath('.//@href').get()
                url_module = city_url.split("//")
                scheme = url_module[0]
                domain = url_module[1]
                if 'bj' in domain:
                    newhouse_url = "http://newhouse.fang.com/house/s/"
                    esf_url = "http://esf.fang.com/"
                else:
                    newhouse_url = scheme + "//" + "newhouse." + domain + "house/s/"
                    esf_url = scheme + "//" + "esf." + domain

                yield scrapy.Request(url=newhouse_url, meta={"info": (province, city)}, callback=self.parse_newhouse)
                yield scrapy.Request(url=esf_url, meta={"info": (province, city)}, callback=self.parse_esf)

    def parse_newhouse(self, response):
        province, city = response.meta.get("info")
        lis = response.xpath('//div[contains(@class,"nl_con")]/ul/li[not(@id)]')
        for li in lis:
            village_name = li.xpath('.//div[@class="nlcd_name"]/a/text()').get()
            village_name = village_name.strip()
            house_type_list = li.xpath('.//div[contains(@class,"house_type")]/a/text()').getall()
            house_type_list = map(lambda x: re.sub("\s", "", x), house_type_list)
            rooms = filter(lambda x: x.endswith(u'居'), house_type_list)
            area = "".join(li.xpath('.//div[contains(@class,"house_type")]/text()').getall())
            area = re.sub(r"\s|－|/", "", area)
            address = li.xpath('.//div[@class="address"]/a/@title').get()
            district_text = "".join(li.xpath('.//div[@class="address"]/a//text()').getall())
            district = re.search(r".*\[(.+)\].*", district_text).group(1)
            sale = li.xpath('.//div[contains(@class,"fangyuan")]/span/text()').get()
            price_text = "".join(li.xpath('.//div[contains(@class,"nhouse_price")]//text()').getall())
            price = re.sub(r"\s|u'广告'", "", price_text)
            origin_url = li.xpath('.//div[@class="nlcd_name"]/a/@href').get()

            item = NewHouseItem(province=province, city=city, village_name=village_name, rooms=rooms, area=area, address=address,
                                district=district, sale=sale, price=price, origin_url=origin_url)

            yield item

        next_url = response.xpath('//div[@class="page"]//a[@class="next"]/@href').get()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url),  meta={"info": (province, city)},
                                 callback=self.parse_newhouse)

    def parse_esf(self, response):
        province, city = response.meta.get("info")
        dls = response.xpath('//div[@class="houseList"]/dl[contains(@id,"list")]')
        for dl in dls:
            item = EsfItem(province=province, city=city)
            item['village_name'] = dl.xpath('.//p[@class="mt10"]/a//text()').get()
            infos = dl.xpath('.//p[@class="mt12"]/text()').getall()
            infos = map(lambda x: re.sub(r"\s", "", x), infos)
            for info in infos:
                if u'厅' in info:
                    item['rooms'] = info
                elif u'层' in info:
                    item['floor'] = info
                elif u'向' in info:
                    item['toward'] = info
                else:
                    item['build_year'] = info.replace(u'建筑年代', "")
            item['address'] = dl.xpath('.//p[@class="mt10"]/span/@title').get()
            item['area'] = dl.xpath('.//div[contains(@class, "area")]/p/text()').get()
            item['price'] = "".join(dl.xpath('.//div[@class="moreInfo"]/p[1]//text()').getall())
            detail_url = dl.xpath('.//p[@class="title"]/a/@href').get()
            item['origin_url'] = response.urljoin(detail_url)

            yield item
        next_url = response.xpath('//a[@id="PageControl1_hlk_next"]/@href').get()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url), meta={"info": (province, city)}, callback=self.parse_esf)






