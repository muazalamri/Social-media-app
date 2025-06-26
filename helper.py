import os
s=lambda j:[i for i in os.listdir() if (len(i.split('.'))==2)&(i.split('.')[-1]=='html')]
dict_re=lambda dic,old,new :{i:dic[i].replace(old,new) for i in dic}
dicter=lambda s:{i:open(i,'r',encoding='utf-8').read() for i in s}
def re_dir(dic):
    for i in dic:
        open(i,'w',encoding='utf-8').write(dic[i])