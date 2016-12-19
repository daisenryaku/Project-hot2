#encoding=utf-8
from  DataProcess import clac_word_freq,clac_news_hot,classify_news,rm_samenews,hot_muti_count

a = clac_word_freq.CalcFreq()
a.run()

b=clac_news_hot.CalcNewsHot()
b.run()

c=classify_news.newsClassier()
c.run()

d.

