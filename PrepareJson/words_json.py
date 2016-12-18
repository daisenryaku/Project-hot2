#encoding=utf-8
import json
import pymongo
import time
import sys
from basic import Basic

sys.path.append('../') # 在路径中添加上级目录，方便导入父级目录的settings

from settings import *

class genWords(Basic):

    def __init__(self,is_last=1,timestamp=None,timetuple=None,collection='news'):
        '''
        默认collection为news
        若is_last=1，则自动选择最新一次爬取的数据
        若is_last！=1，则接受timestamp或timetuple将在该时间内的数据作为来源
        timetuple精确到小时即可
        timtestamp将向后搜索1800s
        '''
        super(genWords,self).__init__(is_last=1,timestamp=timestamp,\
                                      timetuple=timetuple,collection=collection)

    def prepare_words(self):
        self.words=[]
        start_time,last_time=self.process_time(column_sort='words_time',collection='words')

        word_dict=self.db['words'].find_one({"$and":[{"words_time":{"$gte":start_time}},{"words_time":{"$lte":last_time}}]})

        words=sorted(word_dict.iteritems(),key=lambda x: x[1],reverse=True)[2:102]#入选前100个词语 第一个为Object_id,第二个为words_time 故跳过
        words=[[x[0],x[1],[x[1]]] for x in words] #[内容,当前热度,[历史热度趋势（按时间正序排列]]
        print len(words)
        for each in words:
            s_time,l_time=start_time,last_time
            for i in range(14*6):#取前14天的信息，每天的热度取8次，然后以该平均值作为本天热度
                s_time-=10800#秒 4*3600
                l_time-=10800
                word_dict=self.db['words'].find_one({"$and": [{"words_time": {"$gte": start_time}}, {"words_time": {"$lte": last_time}}]})
                if word_dict==None:
                    each[2].append(0)
                else:
                    each[2].append(word_dict.get(each[0],0))

    def prepare_news(self):

        start_time, last_time = self.process_time(column_sort='news_time', collection='news')
        for each_news in self.db['news'].find({"$and": [{"news_time": {"$gte": start_time}}, {"news": {"$lte": last_time}}]}).sort('hot',pymongo.DESCENDING).limit(100):
            


if __name__=='__main__':
    f=genWords()
    f.prepare_news()

