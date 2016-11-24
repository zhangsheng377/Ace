## -*- coding: utf-8 -*-
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

r="【|】|[|]|（|）|\(|\)|-|\+|/|\\\|~|\*".decode("utf-8")

def get_stopWords(stopWords_fn):
    with open(stopWords_fn, 'r') as f:
        stopWords_set = {line.strip('\n').decode('utf-8') for line in f}
    return stopWords_set

if __name__ == '__main__':

    model_out = 'model.txt'

    print u"开始装载模型\n"
    model = word2vec.Word2Vec.load(model_out)

    print u"载入停用词"
    stopWords_set = get_stopWords('stopwords.txt')
    print "正在生成测试结果文件..."
    for s in f_test:
        line = re.sub(r,u" ",s.decode("utf-8"))
        # 创建一个字符串列表
        string_list = []
        # 对每行字符串（数据）进行分词            
        seg = jieba.cut(line)
        # 将每段话的分词结果加入列表里
        filter_seg = [word for word in seg if word not in stopWords_set and word!=" " and word!='\n' and word!="" and not word.isdigit()]
                        
        scores={}
        for i in filter_seg:
            if i in model.vocab:
                for w in model.most_similar(i,topn=1000):
                    if w[0].isdigit():
                        #print w[1]
                        if scores.has_key(w[0]):
                            scores[w[0]]+=w[1]
                        else:
                            scores[w[0]]=w[1]
            
        if len(scores)>0:
            score_max=max(scores.values())
            for c in scores:
                if scores[c]==score_max:
                    category=c
                    break
        else:
            category="0"
        f_testanswer.write(category+"\n")
            

    print "测试结果文件testanswer.data生成完毕"

f_test.close()
f_testanswer.close()


''''
    for w in model.most_similar(u'beiens',topn=1000):
        if w[0].isdigit():
            print w[0], w[1]
    print ""
'''
''''
    for w in model.similar_by_vector([u'贝恩施',u"玩具"]):
        print w[0], w[1]
    print ""
'''