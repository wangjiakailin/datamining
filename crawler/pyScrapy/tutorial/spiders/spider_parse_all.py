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
import redis
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

stockListFile 		= "stockList.txt"
urlListInputFile 	= "urlList/url_previous.txt"
urlListoutputFile 	= "urlList/url_crawler.txt"
outputUrlListFile 	= "urlList/url_latest.txt"
loggingFile 		= "logs/config_all.log"

logging.basicConfig(filename=loggingFile,filemode="w",format="%(asctime)s-%(name)s-%(levelname)s-%(message)s",level=logging.INFO);
logger = logging.getLogger("log_demo");

def loadFile(inputFile):
    file_object = open(inputFile.encode('gbk'))
    try:
         all_the_text = file_object.read()
    finally:
         file_object.close( )
    #print(str(all_the_text))
    return all_the_text

def csv_output(path, file_name, in_text):       
    #data.append(in_text.strip(' ').replace(',',''))
    #print data
    isExists=os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        print path+' 创建成功'
        # 创建目录操作函数
        os.makedirs(path)
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print path+' 目录已存在'  
    
    csvfile = open(path+'/'+file_name, 'a+')
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

client =  redis.StrictRedis(host='localhost', port=6379)
bRedis =  client.ping()
#bRedis = False;
if(not bRedis):
    print "\n#########\nredis not started\n#########\n"
    exit();

stockList = open(stockListFile)

urlList   = loadFile("urlList/url_previous.txt").split("\n")
for filename in urlList:
    client.set(filename, True)

class jobSpider(scrapy.Spider):
    name = "em_parse"
    allowed_domains = ["eastmoney.com"]
    start_urls = [
    'http://guba.eastmoney.com/list,002165,1,f_1.html'
    ]

    #1. process by stockId
    def parse(self, response):
        #print response.url
        for stockId in stockList:
	    stockId = "".join(stockId.split())
            url = 'http://guba.eastmoney.com/list,'+str(stockId.strip('\n'))+',1,f_1.html'
            logger.info("stockId=============="+stockId+"==============");  
            yield Request(url, callback = self.parse1, meta={'stockId': "".join(stockId.split())})

    #2. process by pageId 
    def parse1(self, response):
        sel = scrapy.Selector(response)
        print "url ================ "+response.url
        stockId = response.meta['stockId']
        #print "stockId ================ "+stockId
        
        #1. get the pageCount        
        pageStr = sel.xpath('//div[@class="pager"]/text()').extract()[0]
        pageCount = getPageCount(pageStr)
        
        for pageId in range(0, pageCount+1):
            url = 'http://guba.eastmoney.com/list,'+str(stockId)+',1,f_'+str(pageId)+'.html'
            #print "########url: "+str(url)
            yield Request(url, self.parse2, meta={'stockId': stockId.strip('\n')})

    #3. process by title list;
    def parse2(self, response):
        sel = scrapy.Selector(response)
        stockId = response.meta['stockId']
        titles = sel.xpath('//div[@class="articleh"]/span[@class="l3"]/a/@href')
        print "########len: "+str(len(titles))
        logger.info("titleCount=============="+str(len(titles))+"==============");
        logger.info("urlCount=============="+response.url+"==============");
        len1 = len(titles)  
        for i in range(0,len1):
        #for i in range(1,2):
            #print "########index: "+str(titles[i].extract())
            url = 'http://guba.eastmoney.com' + titles[i].extract()
            #csv_output(url)
            #print "########url_l1: "+str(url)
            #yield Request(url, callback = self.parse3, meta={'stockId': stockId.strip("\n")})
            path = "./"
            csv_output(path, outputUrlListFile, url)
	    res = client.get(url)
	    if(res is None):
	        csv_output(path, urlListoutputFile, url)
