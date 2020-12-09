import pandas as pd
from matplotlib import pyplot as plt
import pickle
import jieba
from wordcloud import WordCloud
from cnsenti import Emotion
from cnsenti import Sentiment
# data= data[0:5]
senti = Sentiment()
emotion = Emotion()
#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
#设置value的显示长度为100，默认为50
pd.set_option('max_colwidth',100)
# stopword_list_cn = [k.strip() for k in open('../../data/cn_stopwords.txt', encoding='utf8').readlines() if k.strip() != '']
# stopword_list_hit = [k.strip() for k in open('../..//data/hit_stopwords.txt', encoding='utf8').readlines() if k.strip() != '']
# stopword_list_scu = [k.strip() for k in open('../../data/scu_stopwords.txt', encoding='utf8').readlines() if k.strip() != '']
# stopword_list = stopword_list_cn+stopword_list_scu+stopword_list_hit



def emotion_sentiment_convert(x):
    result = emotion.emotion_count(x)
    result_senti = senti.sentiment_count(x)

    return result['好'],result['乐'],result['哀'],result['怒'],result['惧'],result['恶'],result['惊'],result_senti['pos'], result_senti['neg']
def emotion_sentiment_convert_all(x):
    result = emotion.emotion_count(x)
    result_senti = senti.sentiment_count(x)
    result_senti_score = senti.sentiment_calculate(x)
    return result['好'],result['乐'],result['哀'],result['怒'],result['惧'],result['恶'],result['惊'],result_senti['pos'], result_senti['neg'],result_senti_score['pos'],result_senti_score['neg']