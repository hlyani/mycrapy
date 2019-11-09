# -*- coding: utf-8 -*-
import json
import pymysql

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class MyscrapPipeline(object):
    def open_spider(self, spider):
        self.file = open('out.json', 'w', encoding='utf-8')
        json_header = '{"hotel":['
        self.count = 0
        # 保存到文件
        self.file.write(json_header)

    def close_spider(self, spider):
        json_tail = ']}'
        # 定位到最后一个逗号
        self.file.seek(self.file.tell() - 1)
        # 截断后面的字符
        self.file.truncate()
        # 添加终止符保存到文件
        self.file.write(json_tail)
        self.file.close()

    def process_item(self, item, spider):
        # 字典转换json字符串
        content = json.dumps(dict(item), ensure_ascii=False,
                             indent=2, separators=(',', ': ')) + ","
        self.count += 1
        print('content', self.count)
        # 保存到文件
        self.file.write(content)
        return item


class MysqlPipeline(object):
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    def open_spider(self, spider):
        self.db = pymysql.connect(
            self.host, self.user, self.password, self.database, charset="utf8", port=int(self.port))
        self.cursor = self.db.cursor()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get("MYSQL_HOST"),
            database=crawler.settings.get("MYSQL_DATABASE"),
            user=crawler.settings.get("MYSQL_USER"),
            password=crawler.settings.get("MYSQL_PASSWORD"),
            port=crawler.settings.get("MYSQL_PORT")
        )

    def process_item(self, item, spider):
        print('+++++++++++++++++++++++++++++++++++++++')
        print(item)
        data = dict(item)
        keys = ','.join(data.keys())
        values = ', '.join(['%s'] * len(data))

        print(values)

        print('=========================================')
        print(data)
        print('=========================================')

        sql = 'insert into %s (%s) values (%s)' % ('hotel', keys, values)

        print(sql)
        print("0000000000000000000000000000000000")

        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()

    def close_spider(self, spider):
        self.db.close()


# CREATE TABLE IF NOT EXISTS `hotel`(
#    `id` INT UNSIGNED AUTO_INCREMENT,
#    `name` VARCHAR(255) NOT NULL,
#    `diamond` VARCHAR(255) NOT NULL,
#    `last_order` VARCHAR(255) NOT NULL,
#    `address` VARCHAR(255) NOT NULL,
#    `score` VARCHAR(255) NOT NULL,
#    `level` VARCHAR(255) NOT NULL,
#    `recommend` VARCHAR(255) NOT NULL,
#    `commend_people` VARCHAR(255) NOT NULL,
#    `commend` VARCHAR(255) NOT NULL,
#    PRIMARY KEY ( `id` )
# )ENGINE=InnoDB DEFAULT CHARSET=utf8;
