#encoding=utf-8

import random
import codecs

rate=1000

f_data=codecs.open('train.data_backup','r')
f_train=codecs.open('train.data','w',"utf-8")
f_test=codecs.open('test.data','w',"utf-8")
f_answer=codecs.open('answer.data','w',"utf-8")

count_read=0
if __name__=='__main__':
    for s in f_data:
        count_read+=1
        if count_read%10000==0:
            print "读入样本数 ："+"%d"%count_read
        ss=s.decode("utf-8").strip().split("||",1)
        if len(ss)>1:
            if random.randint(1,rate)==1:
                f_test.write(ss[1]+"\n")
                f_answer.write(ss[0]+"\n")
            else:
                f_train.write(s.decode("utf-8"))
    print "init over"

f_data.close()
f_train.close()
f_test.close()
f_answer.close()