import pickle
import pandas as pd
#设置显示的最大列、宽等参数，消除打印不完全中间的省略号
pd.set_option("display.width",1000)
#加了这一行那表格就不会分段出现了
pd.set_option("display.width",1000)
#显示所有列
pd.set_option("display.max_columns",None)
#显示所有行
pd.set_option("display.max_rows",None)
with open("data_true_senti.pkl", "rb") as dataFile:
    data = pickle.load(dataFile)
print(data.describe())