

本文在[我用加强版RFM模型，轻松扒出B站优质up主！（含数据+实战代码）](https://blog.csdn.net/SeizeeveryDay/article/details/106293880)的基础上，完成了对B站科技区的UP主的爬取，最后附上数据和代码。



## 原始数据展示

![](https://s1.ax1x.com/2020/05/25/tCnuTA.png)

* coins：投硬币数
* danmu：弹幕数
* favorite：收藏数
* likes：点赞数
* replay：评论数
* share：分享数
* view：播放量

数据总数

```python
# print("数据总数为\t", df.shape)
```



![](https://s1.ax1x.com/2020/05/25/tCn0f0.png)

各字段数目

```python
print("各字段的数量")
# print(df.info())
```



![](https://s1.ax1x.com/2020/05/25/tCnhfx.png)

缺失值数目

```python
print("缺失值数量")
df_null = df.isnull().sum()
# print(df_null)
```

![](https://s1.ax1x.com/2020/05/25/tCupjS.png)



删除空值

```python
df = df.dropna()
# print(df.info())
```

![](https://s1.ax1x.com/2020/05/25/tCuBEd.png)



删除重复值

```python
df = df.drop_duplicates()
# print(df.info())
```



提取关键词

```python
# 提取所需关键词
df = df[['分区', 'author','date','coins','danmu','favorite','likes','replay','share','view']]
print("关键词的前五项")
print(df.head())
```



对数据进行整合，方便以后的遍历

```python
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
```



RFM模型是衡量客户价值和创利能力的重要工具和手段。通过一个客户近期购买行为、购买的总体频率以及消费金额三项指标来描述客户的价值状况。

R：最近一次消费时间（最近一次消费到参考时间的间隔）

F：消费的频率(消费了多少次）

M：消费的金额 （总消费金额）

但RFM模型并不能评价视频的质量，所以在这里针对up主的视频信息构建了IFL模型，以评估视频的质量。



**I(Interaction_rate)：**

I值反映的是平均每个视频的互动率，互动率越高，表明其视频更能产生用户的共鸣，使其有话题感。

![img](https://mmbiz.qpic.cn/mmbiz_png/jGeK1U7D2GIha6QZ1RweRlw3o3DGpIFbrY0CJgB9RpW0VKjOXPvGJF6LCuggNgI4mYJ1XFXguqtCE1UxWwKHEw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

**F(Frequence)：**

F值表示的是每个视频的平均发布周期，每个视频之间的发布周期越短，说明内容生产者创作视频的时间也就越短，创作时间太长，不是忠实粉丝的用户可能将其遗忘。

![img](https://mmbiz.qpic.cn/mmbiz_png/jGeK1U7D2GIha6QZ1RweRlw3o3DGpIFbvZay9EM8CelIADd25wpTs4V94UpI5j1bgKnwOb4WYjN6ia05r5ojTrg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)



**L(Like_rate)：**

L值表示的是统计时间内发布视频的平均点赞率，越大表示视频质量越稳定，用户对up主的认可度也就越高。



![img](https://mmbiz.qpic.cn/mmbiz_png/jGeK1U7D2GLFvzSIXPBuktDa2z5tD3Y2AiaQTv3IcsM01zA9HpwqfxwKJoMeSOI72qfVx1PVW1gAJEFKEUc4VHA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)



### 关键词构造

F值：首先，先筛选出发布视频大于5的up主，视频播放量在5W以上的视频数少于5，说明可能是有些视频标题取得好播放量才高，而不是视频质量稳定的up主。

```python
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
    print("\n*5")
```

![img](https://mmbiz.qpic.cn/mmbiz_png/jGeK1U7D2GIha6QZ1RweRlw3o3DGpIFb3qS7WCkSwtiaalPImDuj9RGWMV3T95mmPM6GribYQFHFEUKatxCB8GUQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

通过describe()方法发现，最晚发布日期与最早发布日期为0的现象，猜测是在同一天内发布了大量的视频。

```
# 查找的一天内发布视频数大于5的人
F.loc[F['F'].idxmin()]
```



![img](https://mmbiz.qpic.cn/mmbiz_png/jGeK1U7D2GIha6QZ1RweRlw3o3DGpIFb7Pjn8SuxU43Q9yFo6ic5ErD8WDrGHn3Q5xvt8xYebEBHNhr5pZkh6og/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

![img](https://mmbiz.qpic.cn/mmbiz_png/jGeK1U7D2GIha6QZ1RweRlw3o3DGpIFbNn7bCialUqD4vRjeAEA0w67Q8rB0yoRH1ibxELVh27uwJ5BDFwKr0kFw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)



其视频皆为转载，将其剔除统计范围内。

```python
F = F.loc[F['F'] > 0]
```



I值计算

```python
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
```



L值计算

```python
 # 计算L值
    group['L'] =(group['likes']+group['coins']*2+group['favorite']*3)/group['view']*100
    L =(group.groupby('author')['L'].sum()/group.groupby('author')['date'].count()).reset_index()
    L.columns =['author', 'L']
    IFL = pd.merge(F_I, L, on='author',how='inner')
    IFL = IFL[['author', 'I','F','L']]

```



### 维度打分

维度确认的核心是分值确定，按照设定的标准，我们给每个消费者的I/F/L值打分，分值的大小取决于我们的偏好，**即我们越喜欢的行为，打的分数就越高**：

- I值，I代表了up主视频的平均评论率，这个值越大，就说明其视频越能使用户有话题，当I值越大时，分值越大。
- F值表示视频的平均发布周期，我们当然想要经常看到，所以这个值越大时，分值越小。
- L值表示发布视频的平均点赞率，S值越大时，质量越稳定，分值也就越大。I/S值根据四分位数打分，F值根据更新周期打分。

```python
IFL.describe()
```

![img](https://mmbiz.qpic.cn/mmbiz_png/jGeK1U7D2GIha6QZ1RweRlw3o3DGpIFbVj81oicElgPQ1ppnBC4uDP8SXFlkw3ibmBKYBP8mL4whaM1cqgUKDe7g/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

#### I值打分：

![img](https://mmbiz.qpic.cn/mmbiz_png/jGeK1U7D2GIha6QZ1RweRlw3o3DGpIFbMY5MzD2KxxibJLrUXENKITl662FUGnpgic7Jc3yZfYXdlo6UdqFmicMdA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

#### L值打分：

![img](https://mmbiz.qpic.cn/mmbiz_png/jGeK1U7D2GIha6QZ1RweRlw3o3DGpIFb6rOB9loOobp0spEJT2QPicMYtKTTiayBTnhRrRs7CVxaphpZfOC2fSxQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

#### F值根据发布周期打分：

![img](https://mmbiz.qpic.cn/mmbiz_png/jGeK1U7D2GIha6QZ1RweRlw3o3DGpIFbJaXP9FrvSUmtfic3STuVEd2clAj4JGY9xgE1vN3tVHaiakRWvke4Dx8Q/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)



#### 分值计算

```python
	IFL['I_SCORE'] = pd.cut(IFL['I'], bins=[0, 0.03, 0.06, 0.11, 1000],
                        labels=[1,2,3,4], right=False).astype(float)
    IFL['F_SCORE'] = pd.cut(IFL['F'], bins=[0, 7, 15, 30, 90, 1000],
                        labels=[5,4,3,2,1], right=False).astype(float)
    IFL['L_SCORE'] = pd.cut(IFL['L'], bins=[0, 5.39, 9.07, 15.58, 1000],
                        labels=[1,2,3,4], right=False).astype(float)
```



#### 判断用户的分值是否大于平均值：

```python
	IFL['I是否大于平均值'] =(IFL['I_SCORE'] > IFL['I_SCORE'].mean()) *1
    IFL['F是否大于平均值'] =(IFL['F_SCORE'] > IFL['F_SCORE'].mean()) *1
    IFL['L是否大于平均值'] =(IFL['L_SCORE'] > IFL['L_SCORE'].mean()) *1
```



### 客户分层

RFM经典的分层会按照R/F/M每一项指标是否高于平均值，把用户划分为8类，我们根据根据案例中的情况进行划分，具体像下面表格这样：

![img](https://mmbiz.qpic.cn/mmbiz_png/jGeK1U7D2GIha6QZ1RweRlw3o3DGpIFbO8pkeqrJJtf2iaqROVvnysQ8sLVhnkZk6fbIEwarAQczu1LOiaNWwrVw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

#### 引入人群数值的辅助列，把之前判断的I\F\S是否大于均值的三个值串联起来：

```python
    IFL['人群数值'] =(IFL['I是否大于平均值'] * 100) +(IFL['F是否大于平均值'] *10) +(IFL['L是否大于平均值'] *1)

```

#### 构建判断函数，通过判断人群数值的值，来返回对应标签：

![img](https://mmbiz.qpic.cn/mmbiz_png/jGeK1U7D2GIha6QZ1RweRlw3o3DGpIFbOmlce8o6L9qJLklPw2UE9QEAThicbC6toicDSiadI4AqEMjbvRwO3M9FQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

#### 将标签分类函数应用到人群数值列：

```python
    IFL['人群类型'] = IFL['人群数值'].apply(transform_label)

```

### 结果存储

```python
	name_xlsx = name + '.xlsx'

  	IFL.to_excel(name_xlsx, encoding='utf-8')
```

![](https://s1.ax1x.com/2020/05/25/tCMAS0.png)



完整代码和数据结果：https://github.com/Mryanhehe/bilibili

