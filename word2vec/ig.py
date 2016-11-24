## -*- coding: utf-8 -*-
import re
import jieba
jieba.load_userdict('userdict.txt')
jieba.enable_parallel(2) # 开启并行分词模式，参数为并行进程数
import sys
import os
from gensim.models import Word2Vec,word2vec
import codecs


def get_stopWords(stopWords_fn):
    with open(stopWords_fn, 'r') as f:
        stopWords_set = {line.strip('\n').decode('utf-8') for line in f}
    return stopWords_set


def train_news(fin_name, fout_name):
    #r = '，|。|《|》|“|”|！|、|；|：|？|<|>|-|\+|…|［|］|　|１|２|３|４|５|６|７|８|９|０|Ａ|Ｂ|Ｕ|Ｖ|Ｗ|Ｘ|Ｙ|Ｚ|ａ|ｂ|ｃ|ｄ|ｅ|ｆ|ｇ|ｈ|ｉ|ｊ|ｋ|ｌ|ｍ|ｎ|ｏ|ｐ|ｑ|ｒ|ｓ|ｔ|ｕ|ｖ|ｗ|ｘ|ｙ|ｚ|【|】|（|）|（|）|'
    r="【|】|[|]|（|）|\(|\)|-|\+|/|\\\|~|\*".decode("utf-8")

    fin = open(fin_name)
    fout = open(fout_name, 'w+')
    a = []
    
    f_fenci=codecs.open('fenci.dat','w',"utf-8")

    print u"载入停用词"
    stopWords_set = get_stopWords('stopwords.txt')
    print "载入训练样本..."
    count_read=0
    for line in fin.readlines():
        count_read+=1
        if count_read%10000==0:
            print "训练样本数 ："+"%d"%count_read
        s=line.decode("utf-8").strip().split("||",1)
        if len(s)>1:
            f_fenci.write(s[1]+"\n")
            category=s[0]
            #ss=re.split(dr,s[1])
            line = re.sub(r,u" ",s[1])
            # 创建一个字符串列表
            string_list = []
            # 对每行字符串（数据）进行分词
            seg = jieba.cut(line)
            # 将每段话的分词结果加入列表里
            filter_seg = [word for word in seg if word not in stopWords_set and word!=" " and word!='\n' and word!="" and not word.isdigit()]
            for i in filter_seg:
                string_list.append(category)
                string_list.append(i)
            a.append(string_list)

            for i in string_list:
                f_fenci.write(i+"\\")
            f_fenci.write("\n")

    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    for k in a:
        for j in k:
            fout.write(j)   # "贝恩施"
            fout.write(' ')
        #fout.write('\n')
    fin.close()
    fout.close()


def creat_model(fin_name_in, model_out):
    # 模型的加载
    sentences = word2vec.Text8Corpus(fin_name_in)  # 加载语料
    print u"正在训练模型" + model_out + '\n'
    # 训练skip-gram模型,默认window=5
    model = word2vec.Word2Vec(sentences, size=100, sg=1, min_count=4, iter=40, workers=20)
    # 使用一些词语来限定,分为正向和负向的
    model.save(model_out)
    print u"模型训练完毕" + model_out + '\n'





def disp_similar(name, model_out):
    print u"开始装载模型\n"
    model = word2vec.Word2Vec.load(model_out)

    for w in model.most_similar(name,topn=100):
        print w[0], w[1]



if __name__ == '__main__':

    fin_name = 'train.data'
    fout_name = 'get.txt'
    model_out = 'model.txt'

    print u"开始分词" + fin_name
    train_news(fin_name, fout_name)
    print u"分词结束" + fout_name + u"\n开始训练模型"
    creat_model(fout_name, model_out)
    print "over!"

    #str = input("输入想要知道的变量：")
    disp_similar(u'贝恩施', model_out)

    #disp_similar(str, model_out)
