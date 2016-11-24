#encoding=utf-8

import jieba
jieba.load_userdict("userdict.txt")
jieba.enable_parallel(2) # 开启并行分词模式，参数为并行进程数
import re
import sys
import codecs
from gensim.models import Word2Vec,word2vec

debug=True

#dr="[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf-8")
dr="【|】|[|]|（|）|\(|\)|-|\+|/|\\\|~|\*".decode("utf-8")

print "读取停止词..."
stopwords={line.strip().decode("utf-8") for line in open('stopwords.txt').readlines()}  #读取停止词文件并保存到列表stopwords
#for ts in stopwords:
 #   print ts
print "停止词读取完毕"

f_data=codecs.open('train.data','r')
f_fenci=codecs.open('fenci.dat','w',"utf-8")

count_read=0
if __name__=='__main__':
    print "开始训练..."
    sentences=[]
    for s in f_data:
        count_read+=1
        if count_read%10000==0:
            print "训练样本数 ："+"%d"%count_read
        ss=s.decode("utf-8").strip().split("||",1)
        sentence=""
        if len(ss)>1:
            if debug:
                #print ss[1]
                f_fenci.write(ss[1]+"\n")
            category=ss[0]
            sss=re.split(dr,ss[1])
            for ssss in sss:
                #result=jieba.cut(ssss, cut_all=True)
                result=jieba.cut(ssss)
                for r in result :
                    if r not in stopwords and r!=" " and r!='\n' and r!="":
                        sentence+=r+" "
                        if debug:
                            #sys.stdout.write(r+'\\')
                            f_fenci.write(r+"\\")
            sentence=category+" "+sentence+"\n"
            sentences.append(sentence)
            if debug:
                #sys.stdout.write("\n")
                f_fenci.write("\n")
    print "正在总体训练中..."
    print "预计1小时..."
    #sentences = word2vec.Text8Corpus(fin_name_in)
    model = word2vec.Word2Vec(sentences, size=500, sg=1, min_count=4, iter=40, workers=2)
    print "\n训练结束，正在保存..."
    model.save('model.txt')
    print "保存完毕"

f_data.close()
f_fenci.close() 
    
                