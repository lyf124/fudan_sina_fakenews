import numpy as np
import pandas as pd
from pyspark import SparkContext
import pymysql
#打开数据库连接
conn = pymysql.connect('sanofirx.chc4t2faiq4z.rds.cn-north-1.amazonaws.com.cn',user = "sanofirx",passwd = "1qazzaq!",db='sanofirx')

cursor = conn.cursor()
# sql ='SELECT  title,department,gender,professionInfo,specialFunction,purchase,market,teamImpact,' \
#      'priority,status,newConcentStatus FROM `bb_client_sfa`'

sql ='SELECT passNum FROM `rr_document_exam_result`'
cursor.execute(sql)
data = cursor.fetchall()
columnDes = cursor.description #获取连接对象的描述信息
columnNames = [columnDes[i][0] for i in range(len(columnDes))]
df = pd.DataFrame([list(i) for i in data],columns=columnNames)
print (str(df['passNum'].value_counts()))