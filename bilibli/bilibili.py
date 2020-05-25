import pandas as pd
import numpy as np 
from datetime import datetime
import time
import xlsxwriter

df = pd.read_excel(r"./b站科技区.xlsx")
# print("数据总数为\t", df.shape)

print("各字段的数量")
# print(df.info())

print("缺失值数量")
df_null = df.isnull().sum()
# print(df_null)

# 删除控制
df = df.dropna()
# print(df.info())

df = df.drop_duplicates()
# print(df.info())

# 提取所需关键词
df = df[['分区', 'author','date','coins','danmu','favorite','likes','replay','share','view']]
print("关键词的前五项")
print(df.head())

group_list = []
name_list = ["科学科普","社科人文","机械","野生技术协会","星海","汽车"] 
# 对数据进行分区
sc = df.loc[df['分区']=='科学科普']
so = df.loc[df['分区']=='社科人文']
ma = df.loc[df['分区']=='机械']
tec = df.loc[df['分区']=='野生技术协会']
mi = df.loc[df['分区']=='星海'] # 一般发布军事内容
car = df.loc[df['分区']=='汽车']

group_list.append(sc)
group_list.append(so)
group_list.append(ma)
group_list.append(tec)
group_list.append(mi)
group_list.append(car)

group_name_list = list(zip(group_list,name_list))

# 科学科普的分区信息
print("科学科普的分区信息")
sc.info()
print("\n *3")

def transform_label(x):
    if x == 111:
        label = '高价值up主'
    elif x == 101:
        label = '高价值拖更up主'
    elif x == 11:
        label = '高质量内容高深up主'
    elif x == 1:
        label = '高质量内容高深拖更up主'
    elif x == 110:
        label = '接地气活跃up主'
    elif x == 10:
        label = '活跃up主'
    elif x == 100:
        label = '接地气up主'
    elif x == 0:
        label = '还在成长的up主'
    return label

def calcKey(group,name):
    count = group.groupby('author')['date'].count().reset_index()
    count.columns = ['author','times']
    # 剔除掉发布视频少于5的up主
    com_m = count[count['times'] > 5]
    #com_m = pd.merge(count,I,on='author',how='inner')
        
    print('信息为')
    com_m.info()
    print("\n *5")
    last = group.groupby('author')['date'].max()
    late = group.groupby('author')['date'].min()

    F = round((last-late).dt.days/sc.groupby('author')['date'].count()).reset_index()   
    F.columns =['author', 'F']
    F = pd.merge(com_m, F,on='author', how='inner')
    print('统计为')
    print(F.describe())
    F = F.loc[F['F'] > 0]
    print("\n*5")
    # 构建I值
    danmu = group.groupby('author')['danmu'].sum()
    replay = group.groupby('author')['replay'].sum()
    view = group.groupby('author')['view'].sum()
    count = group.groupby('author')['date'].count()
    I =round((danmu+replay)/view/count*100,2).reset_index() #
    I.columns=['author','I']
    F_I = pd.merge(F,I,on='author',how='inner')
    print(F_I.head())
    print("\n *5 ")

    # 计算L值
    group['L'] =(group['likes']+group['coins']*2+group['favorite']*3)/group['view']*100
    L =(group.groupby('author')['L'].sum()/group.groupby('author')['date'].count()).reset_index()
    L.columns =['author', 'L']
    IFL = pd.merge(F_I, L, on='author',how='inner')
    IFL = IFL[['author', 'I','F','L']]

    print(IFL.head())
    print("\n * 5")
    IFL['I_SCORE'] = pd.cut(IFL['I'], bins=[0, 0.03, 0.06, 0.11, 1000],
                        labels=[1,2,3,4], right=False).astype(float)
    IFL['F_SCORE'] = pd.cut(IFL['F'], bins=[0, 7, 15, 30, 90, 1000],
                        labels=[5,4,3,2,1], right=False).astype(float)
    IFL['L_SCORE'] = pd.cut(IFL['L'], bins=[0, 5.39, 9.07, 15.58, 1000],
                        labels=[1,2,3,4], right=False).astype(float)
    # 1为大于均值 0为小于均值
    IFL['I是否大于平均值'] =(IFL['I_SCORE'] > IFL['I_SCORE'].mean()) *1
    IFL['F是否大于平均值'] =(IFL['F_SCORE'] > IFL['F_SCORE'].mean()) *1
    IFL['L是否大于平均值'] =(IFL['L_SCORE'] > IFL['L_SCORE'].mean()) *1
    IFL['人群数值'] =(IFL['I是否大于平均值'] * 100) +(IFL['F是否大于平均值'] *10) +(IFL['L是否大于平均值'] *1)
    IFL['人群类型'] = IFL['人群数值'].apply(transform_label)

    cat = IFL['人群类型'].value_counts().reset_index()
    cat['人数占比'] = cat['人群类型'] / cat['人群类型'].sum()
    print(cat)
    print(IFL.head())

    # high = IFL.loc[IFL['人群类型']=='高价值up主']
    # rank = high[['author', 'L', 'I', 'F']].sort_values('L', ascending=False)
    name_xlsx = name + '.xlsx'
    IFL.to_excel(name_xlsx, encoding='utf-8')
    pass

for data in group_name_list:
    calcKey(data[0],data[1])

