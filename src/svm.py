import re
import random

w=[] # 模型参数
C=100 # 松弛变量
# learning_rate=0.00005
learning_rate=0.0001


for i in range(123): # 共123维
    r=random.random()
    w.append(r)  
b=random.random()
with open("data/svm/train", "r") as f: # 读取训练集
    x_train=[] # 用于存储训练数据
    x_validate=[] # 用于存储验证数据
    y_train=[] # 用于存储训练数据的标签值
    y_validate=[] # 用于存储验证数据的标签值
    i=1  # 设置指示值用于提取验证集
    for line in f.readlines():
        if i%100==0:  # 按照 1：14 的比例从训练集中选取验证集
            x_validate.append([]) # 列表嵌套列表
            x_validate[-1]=[0]*123  # 初始全为0
            if line[0]=='-':     # 记录标签
                y_validate.append('-1')
            else:
                y_validate.append('+1')
            line=re.findall(r"\d+\.?\d*",line) # 运用正则表达式提取数字
            line=line[1:]                  # 第一个值为标签，略过
            for j in range(len(line)): 
                if j%2==0:     
                    x_validate[-1][int(line[j])-1]=int(line[j+1]) #对应feature赋value
        else:
            x_train.append([]) # 列表嵌套列表
            x_train[-1]=[0]*123  # 初始全为0
            if line[0]=='-':     # 记录标签
                y_train.append('-1')
            else:
                y_train.append('+1')
            line=re.findall(r"\d+\.?\d*",line) # 运用正则表达式提取数字
            line=line[1:]                 # 第一个值为标签，略过
            for j in range(len(line)): 
                if j%2==0:     
                    x_train[-1][int(line[j])-1]=int(line[j+1]) # 对应feature赋value       
        i+=1
acc = [] # 存储所有的精度，最后输出最大值

for k in range(len(y_train)): # 遍历训练集进行训练
    
    a=0
    for l in range(123):
        a+=x_train[k][l]*w[l]
    for m in range(123):
        if (int(y_train[k])*(a+b))>=1:
            der=0             # 求出 L 偏导
        else:
            der=-(int(y_train[k])*x_train[k][m])  # 求出 L 偏导
        delta=w[m]+C*der   # 求出梯度
        w[m]-=learning_rate*delta
    if k%1000==0:  # 每训练1000次，进行验证准确率
        correct=0
        for o in range(len(y_validate)):
            f_w=0  # 代表预测值
            for p in range(123):
                f_w+=w[p]*float(x_validate[o][p])
            f_w+=b
            if f_w>0:
                prediction='+1'
            else:
                prediction='-1'
            if prediction==y_validate[o]:
                correct+=1    # 统计预测准确次数
        accuracy=round((correct/len(y_validate))*100, 4)  # 计算准确率，以百分比输出, 保留四位小数
        acc.append(accuracy)
        print('After ',k,' training step(s),validation accuracy is', round(accuracy,4))
         # 输出实时准确率     

print('\n For all, the best accuracy is ', max(acc))

with open("data/svm/test", "r") as test: # 读取测试集
    x_test=[] # 用于存储测试集
    for line in test.readlines():
        x_test.append([]) # 列表嵌套列表
        x_test[-1]=[0]*123
        line=re.findall(r"\d+\.?\d*",line) # 运用正则表达式提取数字
        for j in range(len(line)): # 第一个值为标签，略过
            if j%2==0:
                x_test[-1][int(line[j])-1]=int(line[j+1]) # 对应feature赋value


def testing():

    for i in range(len(x_test)):   # 进行测试
        f_p=0
        positive=0
        negetive=0
        for j in range(123):
            f_p+=w[j]*x_test[i][j]
        f_p+=b

        if f_p>0:
            positive = positive+1
            print('+1')
            
        else:
            negetive = negetive+1
            print('-1')

# testing()