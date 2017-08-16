# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# title: the job from 51job
# id is the unique id for jd given by 51job, we can find the jd page with http://search.51job.com/job/ + id + ,c.html
class LiepinItem(scrapy.Item):
    # define the fields for your item here like:
	title = scrapy.Field()
	id = scrapy.Field()
	pass


class JobItem(scrapy.Item):
    # define the fields for your item here like:
	title = scrapy.Field()
	salary = scrapy.Field()
	city = scrapy.Field()
	xueliyaoqiu = scrapy.Field()
	gongzuonianxian = scrapy.Field()
	bumen = scrapy.Field()
	ganweizhize = scrapy.Field()
	renzhiyaoqiu = scrapy.Field()
	xingbieyaoqiu = scrapy.Field()
	nianlinyaoqiu = scrapy.Field()
	pass