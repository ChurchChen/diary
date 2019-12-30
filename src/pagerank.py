import re
import sys

out_nodes = {}  # 统计含有出度的网页的索引网页情况，字典哈希存储，便于查找
out_degrees = {}  # 统计节点出度个数
r_value = {}  # 用于存储各网页的权值,字典内嵌列表
beta = 0.8
epsilon = 0.006
N = 875713 
n = 0
with open("data/pagerank/web-Google.txt", "r") as f:  # 读取文件
    for line in f.readlines():
        if line[0] == '#':  # 跳过数据集开头的注释部分
            continue
        line = line.strip('\n')  # 清除换行符
        line = re.findall(r"\d+\.?\d*", line)  # 使用正则表达式匹配，提取数字
        if line[0] not in out_nodes.keys():
            out_nodes[line[0]] = []
            out_degrees[line[0]] = 0  # 统计网页的出度，初始为 0
        out_nodes[line[0]].append(line[1])
        out_degrees[line[0]] += 1
        for i in range(2):
            if line[i] not in r_value.keys():
                r_value[line[i]] = [1/N, 0]  # 各网页权值
                n += 1
                if n % 50000 == 0:
                    print(n)
                if n == 100:
                    print(out_nodes)
                    print(out_degrees)
                    print(r_value)
print('n=', n)
outcome = 1
j = 0
k = 0  
# 当 k 为偶数，r_value[][0]作为初始，计算r_value[][1],
# 当 k 为奇数，反之
while outcome > epsilon:
    for node in r_value.keys():  # 将要计算的r_value初始化为 0
        r_value[node][(k+1) % 2] = 0
    for node_m in out_nodes.keys():  # 遍历含有出度的网页
        j += 1
        if j % 50000 == 0:
            print(j)
        for node_b in out_nodes[node_m]:  # 遍历该网页各出度指向的网页
            r_value[node_b][(k+1) % 2] += (beta*r_value[node_m]
                                           [k % 2]/out_degrees[node_m])
    print(j)
    S = 0
    outcome = 0
    for node in r_value.keys():
        S += r_value[node][(k+1) % 2]
    for node in r_value.keys():
        r_value[node][(k+1) % 2] += (1-S)/N
        outcome += abs(r_value[node][k % 2]-r_value[node][(k+1) % 2])
    k += 1
    print('      ', outcome)
print('k=    ', k)
f_value = {}  # 用于存储最终结果
for l in r_value.keys():
    f_value[l] = r_value[l][k % 2]
final = sorted(f_value.items(), key=lambda f_value: f_value[1], reverse=True)

for m in range(100):
    print(final[m][0], end='  ')
    print(final[m][1])
    
    output=sys.stdout 
    outputfile=open("data/pagerank/result.txt", "a") # 将输出结果写入到文件中
    sys.stdout=outputfile

print('done')