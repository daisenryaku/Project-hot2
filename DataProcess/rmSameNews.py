#encoding=utf-8
import pymongo
import jieba
import time
import sys
from basic import Basic
import  cleanstr

sys.path.append('../') # 在路径中添加上级目录，方便导入父级目录的settings

from settings import *

with open('stopwords.dat','r') as f:
    g=f.readlines()

stopwords=set([x.rstrip('\n').decode('utf8') for x in g])

def repeatability(str_1, str_2,threshold):  # 判断语句是否重复，是则返回1
    list_1 = set(str_1)
    list_2 = set(str_2)

    a = set(list_1).difference(stopwords)
    b = set(list_2).difference(stopwords)

    intersection = len(a & b)
    union = len(a | b)

    if float(intersection) / union > threshold:
        # print str_1,'----',str_2
        return 1
    else:
        return 0

class Deduplication(Basic):
    def __init__(self, is_last=1, timestamp=None, timetuple=None, collection='news'):
        '''
        默认collection为news
        若is_last=1，则自动选择最新一次爬取的数据
        若is_last！=1，则接受timestamp或timetuple将在该时间内的数据作为来源
        timetuple精确到小时即可
        timtestamp将向后搜索1800s
        '''
        super(Deduplication, self).__init__(is_last=1, timestamp=timestamp, \
                                       timetuple=timetuple, collection=collection)

    def get_data(self,start_time,last_time):
        self.data=[]
        for news in self.coll.find({"$and": [{"news_time": {"$gte": start_time}}, {"news_time": {"$lte": last_time}}]}).sort('hot',pymongo.DESCENDING):
            text=news['news_title']+news['news_abstract']+news['news_body']
            self.data.append([news['_id'],cleanstr.cleanStr(news['news_title']),text,1]) #最后一位为标志位，若为0则表明其等待被删除

    def run(self,search_range=1000,threshold=0.44):
        start_time,last_time=self.process_time()
        print self.process_time()
        self.get_data(start_time,last_time)
        total=len(self.data)
        for i in range(total-1):
            for j in range(1,min(search_range,total-i-1)):
                if repeatability(self.data[i][1],self.data[i+j][1],threshold) and self.data[i][3]!=0 and self.data[i+j][3]!=0:
                    #选择一个长度较短的删除,并将将被删除的新闻的权重转移给另一个新闻
                    if len(self.data[i][2])>len(self.data[i+j][2]):
                        self.data[i][3]+=self.data[i + j][3]
                        self.data[i + j][3]=0
                    else:
                        self.data[i+j][3]+=self.data[i][3]
                        self.data[i][3]=0
        for each in self.data:
            self.coll.update_one({"_id": each[0]}, {'$set': {'count': each[3]}})


if __name__=='__main__':
    f=Deduplication()
    f.run()

