#encoding=utf-8

import jieba
jieba.load_userdict("userdict.txt")
jieba.enable_parallel(2) # 开启并行分词模式，参数为并行进程数
import re
import sys
import codecs
import cPickle

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
f_parameter_categorys=open('parameter_categorys.dat','wb')
f_parameter_words=open('parameter_words.dat','wb')

class CATEGORY:
    class INWORD:
        def __init__(self):
            self.incount=0
            self.weight=0.0
    def __init__(self):
        self.inwords={}
        self.count_sample=0

class WORD:
    def __init__(self):
        self.incategorys={}
        self.count=0

words={}
categorys={}

count_read=0
if __name__=='__main__':
    print "开始训练..."
    for s in f_data:
        count_read+=1
        if count_read%10000==0:
            print "训练样本数 ："+"%d"%count_read
        ss=s.decode("utf-8").strip().split("||",1)
        if len(ss)>1:
            if debug:
                #print ss[1]
                f_fenci.write(ss[0]+"\\"+ss[1]+"\n")
            category=ss[0]
            sss=re.split(dr,ss[1])
            if not categorys.has_key(category):
                categorys[category]=CATEGORY()
            categorys[category].count_sample+=1
            for ssss in sss:
                #result=jieba.cut(ssss, cut_all=True)
                result=jieba.cut(ssss)
                for r in result :
                    if r not in stopwords and r!=" " and r!='\n' and r!="":
                        if not words.has_key(r):
                            words[r]=WORD()
                        if not words[r].incategorys.has_key(category):
                            words[r].incategorys[category]=0
                        words[r].count+=1
                        if not categorys[category].inwords.has_key(r):
                            categorys[category].inwords[r]=CATEGORY.INWORD()
                        categorys[category].inwords[r].incount+=1
                        if debug:
                            #sys.stdout.write(r+'\\')
                            f_fenci.write(r+"\\")
            if debug:
                #sys.stdout.write("\n")
                f_fenci.write("\n")
    print "正在总体训练中..."
    for w in words:
        for c in words[w].incategorys:
            categorys[c].inwords[w].weight=1.0*categorys[c].inwords[w].incount/words[w].count
            #if debug:
               # print w,c,categorys[c].inwords[w].incount,words[w].count,categorys[c].inwords[w].weight
    
    print "\n训练结束，正在保存..."
    cPickle.dump(words,f_parameter_words)
    cPickle.dump(categorys,f_parameter_categorys)
    print "保存完毕"

f_data.close()
f_fenci.close()
f_parameter_words.close()
f_parameter_categorys.close()  
    
                