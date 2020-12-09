import pandas as pd
from matplotlib import pyplot as plt
import pickle
import jieba
from wordcloud import WordCloud
stopword_list_cn = [k.strip() for k in open('../../stopwords/cn_stopwords.txt', encoding='utf8').readlines() if k.strip() != '']
stopword_list_hit = [k.strip() for k in open('../../stopwords/hit_stopwords.txt', encoding='utf8').readlines() if k.strip() != '']
stopword_list_scu = [k.strip() for k in open('../../stopwords/scu_stopwords.txt', encoding='utf8').readlines() if k.strip() != '']
stopword_list = stopword_list_cn+stopword_list_scu+stopword_list_hit
print(len(stopword_list))
plt.rcParams["font.sans-serif"]=["SimHei"]
plt.rcParams['axes.unicode_minus'] = False
# with open("./data.pkl", "rb") as dataFile:
#     data = pickle.load(dataFile)
with open('../../data/yangshi_data.txt', 'r', encoding='utf-8') as file:
    data = pd.DataFrame()
    data['text']=file.readlines()[0:2500]
data["target"]='fake'
fake_data = data[data["target"] == "fake"]
train = []
for line in [' '.join([text for text in jieba.lcut(text) if text not in stopword_list] )for text in fake_data.text]:
    words = line.split(' ')
    train.append(words)
print(train)
import jieba,os,re
from gensim import corpora, models, similarities
dictionary = corpora.Dictionary(train)
# corpus[0]: [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1),...]
# corpus是把每条新闻ID化后的结果，每个元素是新闻中的每个词语，在字典中的ID和频率
corpus = [dictionary.doc2bow(text) for text in train]
lda = models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=20)

topic_list = lda.print_topics(20)
print("10个主题的单词分布为：\n")
for topic in topic_list:
    print(topic)
print(dictionary.doc2bow(['疫情','新增','防控','病例']))
print("**",lda.get_document_topics(dictionary.doc2bow(['疫情','新增','防控','病例'])))