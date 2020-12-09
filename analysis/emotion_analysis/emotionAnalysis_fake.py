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


def function_emotion(x):
    result = emotion.emotion_count(x)
    return result['好'],result['乐'],result['哀'],result['怒'],result['惧'],result['恶'],result['惊']


data['hao'],data['le'],data['ai'],data['nu'],data['ju'],data['e'],data['jing']= zip(*data['text'].apply(lambda x:function_emotion(x)))
with open("data_fake_emo.pkl", "wb") as dataFile:
    pickle.dump(data,dataFile)

