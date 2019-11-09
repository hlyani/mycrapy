# -*- coding: utf-8 -*-
import scrapy
from myscrap.items import MyscrapItem
import re


class HotelSpider(scrapy.Spider):
    name = 'hotel'
    allowed_domains = ['hotels.ctrip.com']
    base_url = 'https://hotels.ctrip.com/hotel/'
    start_urls = ['https://hotels.ctrip.com/hotel/changsha206/p100']

    def parse(self, response):
        print('----------------------------------------------------------')

        # 选取所有标签tr，且class属性等于even或odd的元素
        node_list = response.xpath('//ul[@class="hotel_item"]')

        # 选取所有标签a且id=downHerf,href属性值
        next_page = response.xpath(
            '//a[@id="downHerf"]/@href').get()
        print("next page = " + next_page)
        print('----------------------------------------------------------')

        # search = response.xpath(
        #     '//div[@class="search_part"]/input[1]/@value').get()

        search = "changsha206"

        current_url = self.base_url + search + '/p' + response.xpath(
            '//a[@class="current"]/text()').get()

        for node in node_list:
            item = MyscrapItem()

            item['name'] = node.xpath(
                './li[@class="hotel_item_name"]/h2/a/text()').get()
            item['diamond'] = node.xpath(
                './li[@class="hotel_item_name"]/span/span[3]/@title').get()
            item['last_order'] = node.xpath(
                './li[@class="hotel_item_name"]/p[@class="hotel_item_last_book"]/text()').get()
            item['address'] = node.xpath(
                './li[@class="hotel_item_name"]/p[@class="hotel_item_htladdress"]/text()').getall()[-1]
            item['score'] = node.xpath(
                './li[4]/div/a/span[@class="hotel_value"]/text()').get()
            item['level'] = node.xpath(
                './li[contains(@class,"hotel_item_judge")]/div/a/span[@class="hotel_level"]/text()').get()
            item['recommend'] = node.xpath(
                './li[4]/div/a/span[@class="total_judgement_score"]/span/text()').get()
            item['commend_people'] = node.xpath(
                './li[4]/div/a/span[@class="hotel_judgement"]/span/text()').get()
            item['commend'] = node.xpath(
                './li[4]/div/a/span[@class="recommend"]/text()').get()

            # 请求给调度器，入队，循环结束完成后，交给下载器去异步执行，返回response
            # yield scrapy.Request(url=self.base_url + item['position_link'] ,callback=self.detail)  # 请求详细页
            # yield scrapy.Request(url=self.base_url + search, callback=self.detail, meta={'item': item})

            # dont_filter=True
            # 原因：爬取的url重复了，所以RedisSpider模块默认会记录爬过的url，会把后面出现以前爬过的url去掉，导致重新开启程序爬取之前爬过的url，都被去除掉后就爬不到东西。
            yield scrapy.Request(url=current_url, dont_filter=True, callback=self.detail, meta={'item': item})

        # 请求下一页
        yield scrapy.Request(url=next_page, callback=self.parse)

    def detail(self, response):
        print('----------------------------------------------------------')
        print("detail")
        print('----------------------------------------------------------')
        # 得到parse中的yield item
        item = response.meta['item']

        item["name"] = item["name"].strip()

        item["address"] = item["address"].strip().replace(
            "】", "") if item["address"] else ""

        item["commend"] = re.search(
            r'([\u4e00-\u9fa5]+)', item["commend"]).group(1) if item["commend"] else ""

        item["commend_people"] = item["commend_people"] if item["commend_people"] else ""

        item["diamond"] = item["diamond"] if item["diamond"] else ""

        item["last_order"] = re.search(
            r'最新预订：(\w+)', item["last_order"]).group(1) if item["last_order"] else ""

        item["level"] = item["level"] if item["level"] else ""

        item["score"] = item["score"] if item["score"] else ""

        item["recommend"] = item["recommend"] if item["recommend"] else ""

        print('----------------------------------------------------------')

        yield item
