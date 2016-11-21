#import codecs
import cPickle

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

f_parameter_words=file('parameter_words.dat','r')
f_parameter_categorys=file('parameter_categorys.dat','r')

words=cPickle.load(f_parameter_words)
categorys=cPickle.load(f_parameter_categorys)

if __name__=='__main__':
    for w in words:
        for c in words[w].incategorys:
            print w,c,categorys[c].inwords[w].incount,words[w].count,categorys[c].inwords[w].weight