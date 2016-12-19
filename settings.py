#encoding=utf-8

#Mongodb相关配置
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_DATABASE = "NEWS"
MONGODB_PASSWORD = ""
MONGODB_USERNAME = ""

#Project所在路径
PROJECT_PATH="C:\Users\Administrator\Desktop\project_hot2\\"

#生成json所存储的路径
JSON_STORE_PATH="C:\Users\Administrator\Desktop\project_hot2\PrepareJson\\"

#定义新闻相似的Jaccard系数区间
SCOPE_SIMILAR_NEWS=(0.15,0.4)

#生成news.json时每个新闻所关联的相似新闻数
NUM_SIMILAR_NEWS2NEWS=3

#生成words.json时每个词语所关联的相似新闻数
NUM_SIMILAR_WORDS2NEWS=3

#生成topic.json时每个topic相关的新闻数
NUM_TOPICS2NEWS=10

