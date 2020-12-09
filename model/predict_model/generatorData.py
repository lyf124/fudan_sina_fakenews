import pandas as pd
from matplotlib import pyplot as plt
import pickle
import jieba
from wordcloud import WordCloud
#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
#设置value的显示长度为100，默认为50
pd.set_option('max_colwidth',100)
stopword_list_cn = [k.strip() for k in open('../../stopwords/cn_stopwords.txt', encoding='utf8').readlines() if k.strip() != '']
stopword_list_hit = [k.strip() for k in open('../../stopwords/hit_stopwords.txt', encoding='utf8').readlines() if k.strip() != '']
stopword_list_scu = [k.strip() for k in open('../../stopwords/scu_stopwords.txt', encoding='utf8').readlines() if k.strip() != '']
stopword_list = stopword_list_cn+stopword_list_scu+stopword_list_hit
# print(len(stopword_list))
plt.rcParams["font.sans-serif"]=["SimHei"]
plt.rcParams['axes.unicode_minus'] = False
# with open("./data.pkl", "rb") as dataFile:
#     data = pickle.load(dataFile)
with open('../../data/fake_data.txt','r',encoding='utf-8') as file:
    fake_data = pd.DataFrame()
    fake_data['text']=file.readlines()
fake_data["target"]='fake'
# fake_data = data[data["target"] == "fake"]
# print(fake_data.shape)
with open('../../data/yangshi_data.txt','r',encoding='utf-8') as file:
    true_data = pd.DataFrame()
    true_data['text']=file.readlines()
true_data["target"]='true'
# fake_data = data[data["target"] == "fake"]
# print(true_data.shape)
all_data = pd.concat([true_data,fake_data])

from sklearn.utils import shuffle
all_data = shuffle(all_data)
all_data['text'] =all_data['text'].apply(lambda x:x.replace('\n',''))
# print(all_data.head(10))
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(all_data['text'], all_data['target'], test_size=0.2, random_state=38)
X_train= X_train.reset_index(drop=True)
y_train= y_train.reset_index(drop=True)
X_test= X_test.reset_index(drop=True)
y_test= y_test.reset_index(drop=True)

#sentiment emotion
senti_emotion_train_df  =pd.DataFrame()
from  utils.data_preprocessing import emotion_sentiment_convert
senti_emotion_train_df['hao'],senti_emotion_train_df['le'],senti_emotion_train_df['ai'],senti_emotion_train_df['nu'],senti_emotion_train_df['ju'],\
senti_emotion_train_df['e'],senti_emotion_train_df['jing'],senti_emotion_train_df['pos'],senti_emotion_train_df['neg']= zip(*X_train.apply(lambda x:emotion_sentiment_convert(x)))
# print(senti_emotion_train_df)

train = []
for line in [' '.join([text for text in jieba.lcut(text) if text not in stopword_list] )for text in X_train]:
    words = line.split(' ')
    train.append(words)
from gensim import corpora, models, similarities
dictionary = corpora.Dictionary(train)
# corpus[0]: [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1),...]
# corpus是把每条新闻ID化后的结果，每个元素是新闻中的每个词语，在字典中的ID和频率
corpus = [dictionary.doc2bow(text) for text in train]
lda = models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=20)
#
# topic_list = lda.print_topics(20)
# print("10个主题的单词分布为：\n")
# for topic in topic_list:
#     print(topic)
vec_train_arrs =[]
for cor in corpus:
    vec_tuple = lda.get_document_topics(cor,minimum_probability=0)
    vec_arr = [ tuple[1] for tuple in vec_tuple]

    vec_train_arrs.append(vec_arr)
# print(len(vec_train_arrs))

vec_X_train = pd.concat([X_train, pd.DataFrame(vec_train_arrs),senti_emotion_train_df], axis=1)
print(vec_X_train.shape)

#test

test = []
for line in [' '.join([text for text in jieba.lcut(text) if text not in stopword_list] )for text in X_test]:
    words = line.split(' ')
    test.append(words)
test_corpus = [dictionary.doc2bow(text) for text in test]
vec_test_arrs =[]
for cor in test_corpus:
    vec_tuple = lda.get_document_topics(cor,minimum_probability=0)
    vec_arr = [ tuple[1] for tuple in vec_tuple]

    vec_test_arrs.append(vec_arr)
#sentiment emotion analysis   test
senti_emotion_test_df  =pd.DataFrame()
senti_emotion_test_df['hao'],senti_emotion_test_df['le'],senti_emotion_test_df['ai'],senti_emotion_test_df['nu'],senti_emotion_test_df['ju'],\
senti_emotion_test_df['e'],senti_emotion_test_df['jing'],senti_emotion_test_df['pos'],senti_emotion_test_df['neg']= zip(*X_test.apply(lambda x:emotion_sentiment_convert(x)))


vec_X_test= pd.concat([X_test, pd.DataFrame(vec_test_arrs),senti_emotion_test_df], axis=1)
print("****")
print(vec_X_test)
print(y_test)
import pickle
with open("../conDataAndModel/x_train.pkl", "wb") as dataFile:
    pickle.dump(vec_X_train,dataFile)
with open("../conDataAndModel/x_test.pkl", "wb") as dataFile:
    pickle.dump(vec_X_test,dataFile)
with open("../conDataAndModel/y_train.pkl", "wb") as dataFile:
    pickle.dump(y_train,dataFile)
with open("../conDataAndModel/y_test.pkl", "wb") as dataFile:
    pickle.dump(y_test,dataFile)
with open("../conDataAndModel/lda_model.pkl", "wb") as dataFile:
    pickle.dump(lda,dataFile)
with open("../conDataAndModel/lda_dictionary.pkl", "wb") as dataFile:
    pickle.dump(dictionary,dataFile)


# print(lda.get_document_topics(dictionary.doc2bow([text for text in jieba.lcut("今天，直播走进江西赣州寻乌县高布村。“歪果仁”星悦，能在这里学会客家话吗？“草原歌王”腾格尔，与赣南山村有着怎样的缘分？村里的第一书记，为啥能“变年轻”？看↓（总台央视记者郭一淳裴奔）") if text not in stopword_list]),minimum_probability=0))