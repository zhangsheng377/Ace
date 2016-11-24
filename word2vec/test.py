#encoding=utf-8

import jieba
jieba.load_userdict("userdict.txt")
jieba.enable_parallel(2) # 开启并行分词模式，参数为并行进程数
import re
import sys
import codecs
from gensim.models import Word2Vec,word2vec

debug=False

f_test=codecs.open('test.data','r')
f_testanswer=codecs.open('testanswer.data','w',"utf-8")

print "读取模型文件..."
model = word2vec.Word2Vec.load('model.txt')

dr="【|】|[|]|（|）|\(|\)|-|\+|/|\\\|~|\*".decode("utf-8")
print "读取停止词..."
stopwords={line.strip().decode("utf-8") for line in open('stopwords.txt').readlines()}  #读取停止词文件并保存到列表stopwords

if __name__=='__main__':
    print "正在生成测试结果文件..."
    for s in f_test:
        ss=re.split(dr,s)
        sentence=[]
        for sss in ss:
            #result=jieba.cut(sss, cut_all=True)
            result=jieba.cut(sss)
            for r in result :
                if r not in stopwords and r!=" " and r!='\n' and r!="":
                    sentence.append(r)
        if len(sentence)>0:
            for w in model.most_similar("823"):
                print w[0], w[1]
        #d=dict([(k,v) for k,v in scores.items() if v==max(scores.values())])
        #print category
        #f_testanswer.write(category+"\n")
    print "测试结果文件testanswer.data生成完毕"

f_test.close()
f_testanswer.close()