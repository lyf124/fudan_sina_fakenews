import pandas as pd
from matplotlib import pyplot as plt
import pickle
import jieba
from wordcloud import WordCloud
stopword_list = [k.strip() for k in open('../../stopwords/cn_stopwords.txt', encoding='utf8').readlines() if k.strip() != '']
print(stopword_list)
plt.rcParams["font.sans-serif"]=["SimHei"]
plt.rcParams['axes.unicode_minus'] = False
# with open("./data.pkl", "rb") as dataFile:
#     data = pickle.load(dataFile)
with open('../../data/fake_data.txt', 'r', encoding='utf-8') as file:
    data = pd.DataFrame()
    data['text']=file.readlines()
data["target"]='fake'
from cnsenti import Emotion
from cnsenti import Sentiment
# data= data[0:5]
senti = Sentiment()
emotion = Emotion()


def function_sentiment(x):
    result = senti.sentiment_count(x)
    return result['pos'],result['neg']


data['pos'],data['neg']= zip(*data['text'].apply(lambda x:function_sentiment(x)))
with open("data_fake_senti.pkl", "wb") as dataFile:
    pickle.dump(data,dataFile)

