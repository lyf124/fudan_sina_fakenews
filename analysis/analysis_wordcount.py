import pandas as pd
from matplotlib import pyplot as plt
import pickle
import jieba
from wordcloud import WordCloud
stopword_list_cn = [k.strip() for k in open('../stopwords/cn_stopwords.txt', encoding='utf8').readlines() if k.strip() != '']
stopword_list_hit = [k.strip() for k in open('../stopwords/hit_stopwords.txt', encoding='utf8').readlines() if k.strip() != '']
stopword_list_scu = [k.strip() for k in open('../stopwords/scu_stopwords.txt', encoding='utf8').readlines() if k.strip() != '']
stopword_list = stopword_list_cn+stopword_list_scu+stopword_list_hit
print(len(stopword_list))
plt.rcParams["font.sans-serif"]=["SimHei"]
plt.rcParams['axes.unicode_minus'] = False
# with open("./data.pkl", "rb") as dataFile:
#     data = pickle.load(dataFile)
with open('../data/yangshi_data.txt', 'r', encoding='utf-8') as file:
    data = pd.DataFrame()
    data['text']=file.readlines()[0:3000]
data["target"]='fake'
fake_data = data[data["target"] == "fake"]
print(fake_data)
all_words = ' '.join([' '.join([text for text in jieba.lcut(text) if text not in stopword_list] )for text in fake_data.text])
print(all_words)
count_words = []
for line in [' '.join([text for text in jieba.lcut(text) if text not in stopword_list] )for text in fake_data.text]:
    words = line.split(' ')
    count_words = count_words + words


import  collections
word_counts = collections.Counter(count_words) # 对分词做词频统计
word_counts_top10 = word_counts.most_common(100) # 获取前10最高频的词
print (word_counts_top10)
wordcloud = WordCloud(width= 800, height= 500,
max_font_size = 110,
collocations = False).generate(all_words)

plt.figure(figsize=(10,8))
plt.imshow(wordcloud, interpolation='bilinear')

plt.axis("off")
plt.show()

# from wordcloud import WordCloud
# real_data = data[data["target"] == "true"]
# all_words = ' '.join([text for text in fake_data.text])
# wordcloud = WordCloud(width= 800, height= 500, max_font_size = 110,
# collocations = False).generate(all_words)
# plt.figure(figsize=(10,7))
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")
# plt.show()