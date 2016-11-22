#encoding=utf-8

import codecs

f_answer=codecs.open('answer.data','r')
f_testanswer=codecs.open('testanswer.data','r')

if __name__=='__main__':
    answer=f_answer.readlines()
    testanswer=f_testanswer.readlines()
    length=len(answer)
    if length!=len(testanswer):
        print "answer.data与testanswer.data不匹配"
    else:
        count=0
        for i in range(length):
            if answer[i]==testanswer[i]:
                count+=1
        print "success rate : "+"%f"%(1.0*count/length)