#encoding=utf-8

import jieba
import re

dr="[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf-8")
dn="".decode("utf-8")

s="这是一个伸手不见五指的黑夜。我叫孙悟空，我爱北京，我爱Python和C++。  j  k   s  +    ,   .  。   ，  op"

ss=s.decode("utf-8")
print ss

sss=re.split(dr,ss)
#print sss
for ssss in sss:
    #print ssss
    #l=re.sub(dr, dn, ssss)
    #print l
    result=jieba.cut(ssss)
    #print(" / ".join(result))
    for r in result:
        print r