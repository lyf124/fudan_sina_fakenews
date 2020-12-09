import pandas as pd
from matplotlib import pyplot as plt
import pickle
import jieba
import warnings
from  utils.data_preprocessing import emotion_sentiment_convert
warnings.filterwarnings("ignore")
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
with open("../conDataAndModel/lda_model.pkl", "rb") as dataFile:
    lda_model = pickle.load(dataFile)
with open("../conDataAndModel/lda_dictionary.pkl", "rb") as dataFile:
    dictionary = pickle.load(dataFile)
with open("../conDataAndModel/xgb_model.pkl", "rb") as dataFile:
    clf_model  =pickle.load(dataFile)
with open("../conDataAndModel/le_label.pkl", "rb") as dataFile:
    label_model = pickle.load(dataFile)
import numpy as np

def test_predict(test_text):
    test_words = [text for text in jieba.lcut(test_text) if text not in stopword_list]
    # print(test_words)
    test_corpus = dictionary.doc2bow(test_words)
    test_tuple = lda_model.get_document_topics(test_corpus, minimum_probability=0)
    test_vec = [tuple[1] for tuple in test_tuple]

    # sentiment emotion analysis   test
    senti_emotion_test_df = pd.DataFrame()
    senti_emotion_test_df['hao'], senti_emotion_test_df['le'], senti_emotion_test_df['ai'], senti_emotion_test_df['nu'], \
    senti_emotion_test_df['ju'], \
    senti_emotion_test_df['e'], senti_emotion_test_df['jing'], senti_emotion_test_df['pos'], senti_emotion_test_df[
        'neg'] = zip(emotion_sentiment_convert(test_text))

    test_df = pd.concat([pd.DataFrame([test_vec]), senti_emotion_test_df], axis=1)

    # print(senti_emotion_test_df)
    y_preidct = clf_model.predict(test_df)
    y_predict_c = label_model.inverse_transform(y_preidct[0])
    return "真实新闻" if y_predict_c=='true' else "谣言"


if __name__ == '__main__':
    test_text = "12月8日，经四川省成都市成华区新冠肺炎疫情防控指挥部研究决定：自12月8日21时起，将成都市成华区崔家店华都云景台小区的风险等级由低风险调整为中风险。成都市成华区其他区域低风险等级不变。"
    print("预测结果:",test_predict(test_text))