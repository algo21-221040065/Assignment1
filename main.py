import  pandas as pd
import numpy as np
import csv
import math
import matplotlib.pyplot as plt

#选择这篇研报主要是想利用其中的技术面因子做一些数字货币的分析
#动机来源于这次俄乌军事行动后动荡的全球金融市场，因为技术面因子本身有包含行为金融学的某些信息
#想了解股票市场归纳出的情绪指标对于动荡环境下管理相对宽松的数字货币市场是否适用

filename = 'C:/Users/86188/PycharmProjects/Assignment1/data.csv'
data = pd.read_csv(filename)

#从MT4上下载了包括bitcoin cash、eth等八个主流交易品种的三十分钟线数据，时间从2022.01.25至2022.03.12共2048个数据的开、高、低、收、成交价
#整理为同一个csv文件方便读取，以形如H1（High1）来作为列名


#定义计算,文中所有计算式都可以用类似的方法写出此处未列完
def rank(A,N,m):
    #数字货币A(eg:1)的指标m（eg：H代表最高价）在时间节点N在所有货币中的排序值
    range=[]
    for i in range(0,8):
        range.append(data.iloc[N-i][str(m)+str(A)])
    return rank(range)[A-1]

def adv(A,N,n):
    #数字货币A在时间节点N往前n天的平均成交量
    sum=0
    if(N<=n):
        n=N
    for i in range(0,n):
        sum=sum+data.iloc[N-i]["V"+str(A)]
    return sum/n

def Judge(X,Y,Z):
    #若X成立则返回Y，否则返回Z
    if X is True:
        return Y
    else:
        return Z

def returns(A,N):
    #数字货币A在时间节点N的相对昨日收益率
    return data.iloc[N]["C"+str(A)]/data.iloc[N-1]["C"+str(A)]-1

def VWAP(A,N,n):
    #数字货币A在时间节点N往前n天的加权成交价
    sum = 0
    value=0
    if (N <= n):
        n = N
    for i in range(0, n):
        sum = sum + data.iloc[N - i]["V" + str(A)]
        value = value+data.iloc[N - i]["V" + str(A)]*data.iloc[N - i]["C" + str(A)]
    return value / sum

def delay(A,N,m,d):
    #数字货币A的指标m在时间节点N往前d天的值
    if (N< d):
        d=N
    return data.iloc[N-d][str(m)+str(A)]

def delta(A,N,m,d):
    #数字货币A的指标m在时间节点N的值相对往前d天的值的增量
    return iloc[N][str(m)+str(A)]-delay(A,N,m,d)


#定义因子的函数表达式,因为上面已经定义了计算式但文中大多数因子表达式过于繁琐，此处取factor101做例子并乘上一个成交量继续研究

#为了方便分别定义数字货币A在时间节点N的各个指标
def O(A,N):
    return data.iloc[N]["O"+str(A)]

def H(A,N):
    return data.iloc[N]["H"+str(A)]

def L(A,N):
    return data.iloc[N]["L"+str(A)]

def C(A,N):
    return data.iloc[N]["C"+str(A)]

def V(A,N):
    return data.iloc[N]["V"+str(A)]


def factor101(A,N):#定义时间节点N处数字货币A的101号因子值
    return V(A,N)*(C(A,N)-O(A,N))/((H(A,N)-L(A,N))+0.01)

#开始遍历每一个时间节点计算各个数字货币的factor101的值并存入数组
stat=pd.DataFrame(columns=['1','2','3','4','5','6','7','8'])
#定义一个空的dataframe用于逐行输入
for i in range(0,2048):
    stat.loc[i]={'1':factor101(1,i),'2':factor101(2,i),'3':factor101(2,i),'4':factor101(2,i),
                 '5':factor101(2,i),'6':factor101(2,i),'7':factor101(2,i),'8':factor101(2,i)}
stat.to_csv('factor101.csv')

#接下来本来应该进行IC/IR分析决定因子方向就行多空组合，但此处由于已经通过观察得出了应该选择因子值较小的买入，
#进行简单回测，即在每个时间节点进行全部换仓并买入因子排名最靠前的一只一直持有
buy=[]#用于接受每个节点购买的货币编号
for i in range(0,2048):
    min=1
    for j in range(1,9):
        if(stat.values[i][j-1]<=stat.values[i][min-1]):
            min=j
    buy.append(min)

#计算净值序列,假设初始投入1万元
values=[]
values.append(10000)
for i in range(1,2048):
    values.append(values[i-1]*data.iloc[i]["C"+str(buy[i-1])]/data.iloc[i-1]["C"+str(buy[i-1])])
x=range(0,2048)
plt.plot(x,values)
plt.show()#画出净值曲线

#由图看出回撤在可接受范围内
