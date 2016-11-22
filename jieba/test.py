#encoding=utf-8

import jieba
import re
import sys
import codecs
import cPickle

debug=False

class CATEGORY:
    class INWORD:
        def __init__(self):
            self.incount=0
            self.weight=0.0
    def __init__(self):
        self.inwords={}
        self.count_sample=0
class INWORD:
    def __init__(self):
        self.incount=0
        self.weight=0.0

class WORD:
    def __init__(self):
        self.incategorys={}
        self.count=0

f_parameter_words=open('parameter_words.dat','rb')
f_parameter_categorys=open('parameter_categorys.dat','rb')
f_test=codecs.open('test.data','r')
f_testanswer=codecs.open('testanswer.data','w',"utf-8")

print "读取参数配置文件..."
words=cPickle.load(f_parameter_words)
categorys=cPickle.load(f_parameter_categorys)

dr="【|】|[|]|（|）|\(|\)|-|\+|/|\\\|~|\*".decode("utf-8")
print "读取停止词..."
stopwords={line.strip().decode("utf-8") for line in open('stopwords.txt').readlines()}  #读取停止词文件并保存到列表stopwords
print "读取用户字典..."
jieba.load_userdict("userdict.txt")
print "读取完毕"

if __name__=='__main__':
    #if debug:
        #for w in words:
         #   for c in words[w].incategorys:
          #      print w,c,categorys[c].inwords[w].incount,words[w].count,categorys[c].inwords[w].weight
    print "正在生成测试文件..."
    for s in f_test:
        ss=re.split(dr,s)
        scores={}
        for sss in ss:
            result=jieba.cut(sss)
            for r in result :
                if r not in stopwords and r!=" " and r!='\n' and words.has_key(r):
                    for c in words[r].incategorys:
                        if 1.0*categorys[c].inwords[r].incount/categorys[c].count_sample > 0.01:
                            if not scores.has_key(c):
                                scores[c]=0.0
                            scores[c]+=categorys[c].inwords[r].weight
                            #print r,c,categorys[c].inwords[r].weight
        if debug:
            for c in scores:
                print c+" "+'%f'%scores[c]+" \\",
            print ""
        score_max=max(scores.values())
        for c in scores:
            if scores[c]==score_max:
                category=c
                break
        #d=dict([(k,v) for k,v in scores.items() if v==max(scores.values())])
        #print category
        f_testanswer.write(category+"\n")
    print "测试文件testanswer.data生成完毕"

f_parameter_words.close()
f_parameter_categorys.close()
f_test.close()
f_testanswer.close()