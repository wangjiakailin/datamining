#coding:utf-8
import re
import json
import scrapy
import os
import sys
import re
import xlwt
import csv
import md5
import hashlib
import time
import logging
from scrapy.http.request import Request
reload(sys)
sys.setdefaultencoding('utf-8')

from scrapy.selector import Selector  
try:  
    from scrapy.spider import Spider  
except:  
    from scrapy.spider import BaseSpider as Spider  
from scrapy.utils.response import get_base_url  
from scrapy.utils.url import urljoin_rfc  
from scrapy.contrib.spiders import CrawlSpider, Rule  
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle
#from fang_Scrapy.tutorial.tutorial.items import LiepinItem
#from fang_Scrapy.tutorial.tutorial.items import JobItem

urlListFile 	 = "urlList/url_crawler.txt"
pathName 	 = "stockInfo_v2_yanbao"
loggingFile	 = "logs/config_all.log"
outputStatusFile = "logs/stockStatus.txt"

logging.basicConfig(filename=loggingFile, filemode="w",format="%(asctime)s-%(name)s-%(levelname)s-%(message)s",level=logging.INFO);  
logger = logging.getLogger("log_demo");  

def csv_output(path, file_name, in_text):       
    #data.append(in_text.strip(' ').replace(',',''))
    #print data
    isExists=os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        #print path+' 创建成功'
        # 创建目录操作函数
        os.makedirs(path)
    else:
        # 如果目录存在则不创建，并提示目录已存在?
        #print path+' 目录已存在?
	ii = 3
    
    csvfile = open(path+'/'+file_name, 'w+')
    in_text = in_text.replace("\r\n", " ").replace("\s*",",");
    csvfile.write(in_text+'\n')
    csvfile.close()

def csv_output_status(path, file_name, in_text):
    #data.append(in_text.strip(' ').replace(',',''))
    #print data
    isExists=os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        #print path+' 创建成功'
        # 创建目录操作函数
        os.makedirs(path)
    else:
        ii = 3
        # 如果目录存在则不创建，并提示目录已存在?
        #print path+' 目录已存在?

    csvfile = open(path+'/'+file_name, 'a+')
    print "path: ----: "+path+'/'+file_name
    in_text = in_text.replace("\r\n", " ").replace("\s*",",");
    csvfile.write(in_text+'\n')
    csvfile.close()

def getPageCount(pageStr):
    pageCount = int(re.findall(r'(\w*[0-9]+)\w*',pageStr)[0])
    if(pageCount%80 == 0):
        pageCount = pageCount/80
    else:
        pageCount = pageCount/80+1
    return pageCount

def getCurrentDatetime():
    return time.strftime('%Y-%m-%d',time.localtime(time.time()))

def getMd5(inStr):
    m2 = hashlib.md5()   
    m2.update(inStr)   
    return str(m2.hexdigest())

def getPath(stockId, currentDatetime):
    return stockId+'/'+currentDatetime

def getFileName(currentDatetime, url):
    return currentDatetime+"_"+getMd5(url)+".txt";

lineList = open(urlListFile)

class jobSpider(scrapy.Spider):
    name = "em_crawler"
    allowed_domains = ["eastmoney.com"]
    start_urls = [
    'http://guba.eastmoney.com/list,002165,2,f_1.html'
    ]

    #1. process by stockId
    def parse(self, response):
        #print response.url
        for line in lineList:
	    stockId = "".join(line.split(",")[1])
	    url = "".join(line.split(" ")[0]).strip('\n') 
            logger.info("stockId=============="+stockId+"==============");  
            logger.info("url=============="+url+"==============");  
            yield Request(url, callback = self.parse3, meta={'stockId': stockId})

    #4. process by text
    def parse3(self, response):
        sel = scrapy.Selector(response)
        stockId = response.meta['stockId']
        logger.info("stockId==============enter parse3=============="); 
        url = response.url
        strHeader = ""
        strFooter = ""
        if(sel.re('id="zw_header"')):
            strHeader = sel.xpath('//div[@id="zw_header"]').xpath('string(.)').extract()[0]
            #print strHeader
        if(sel.re('id="zw_footer"')):
            strFooter = sel.xpath('//div[@id="zw_footer"]').xpath('string(.)').extract()[0]

	urls_l1 = sel.xpath('//div[@id="zwconttbt"]')
	titleContent = urls_l1.xpath('string(.)').extract()[0]
	print "titleContent==="+str(urls_l1)+"===="+str(titleContent)

        urls_l2 = sel.xpath('//div[@class="stockcodec"]')
        info = titleContent+"\n"+urls_l2.xpath('string(.)').extract()[0].replace(strHeader,"").replace(strFooter,"").replace(r"点击查看原文","")
                
        curDatetime_l2 = sel.xpath('//div[@class="zwfbtime"]').xpath('string(.)').extract()[0]
        curDatetime = "".join(curDatetime_l2.split(" ")[1]) 
        
        time.sleep(0.25)
        currentDatetime = getCurrentDatetime()
        path            = getPath(pathName+"/"+stockId, currentDatetime)
        file_name       = getFileName(curDatetime, url);
	csv_output_status('./', outputStatusFile, stockId+","+url+',pass')
        csv_output(path, file_name, info)
