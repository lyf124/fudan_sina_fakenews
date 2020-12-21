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
with open("../conDataAndModel/x_train.pkl", "rb") as dataFile:
    x_train = pickle.load(dataFile)
with open("../conDataAndModel/x_test.pkl", "rb") as dataFile:
    x_test = pickle.load(dataFile)
with open("../conDataAndModel/y_train.pkl", "rb") as dataFile:
    y_train = pickle.load(dataFile)
with open("../conDataAndModel/y_test.pkl", "rb") as dataFile:
    y_test = pickle.load(dataFile)
with open("../conDataAndModel/lda_model.pkl", "rb") as dataFile:
    lda_model = pickle.load(dataFile)
with open("../conDataAndModel/lda_dictionary.pkl", "rb") as dataFile:
    dictionary = pickle.load(dataFile)

print(x_train.shape,y_train.shape,x_test.shape,y_test.shape)
from sklearn import preprocessing
le = preprocessing.LabelEncoder()

y_train = le.fit_transform(y_train)
y_test = le.transform(y_test)
from xgboost import XGBClassifier

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler,MinMaxScaler
randomforest_model = RandomForestClassifier(n_estimators=10, max_depth=10)


x_train = x_train.drop(['text'],axis=1)
x_test = x_test.drop(['text'],axis=1)
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)
# 计算分类正确率
from sklearn.metrics import accuracy_score
model = XGBClassifier()
model.fit(x_train, y_train)
print(x_test)
y_pred = model.predict(x_test)
print(y_pred)
print(y_test)
accuracy = accuracy_score(y_test, y_pred)
from sklearn.metrics import f1_score
print("Accuracy: %.2f%%" % (accuracy * 100.0))
f1_score = f1_score(y_test, y_pred, average='macro')
print("F1: %.2f%%" % (f1_score * 100.0))
with open("../conDataAndModel/xgb_model.pkl", "wb") as dataFile:
    pickle.dump(model,dataFile)
with open("../conDataAndModel/le_label.pkl", "wb") as dataFile:
    pickle.dump(le,dataFile)
with open("../conDataAndModel/scaler.pkl", "wb") as dataFile:
    pickle.dump(scaler,dataFile)