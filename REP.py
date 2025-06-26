from os import listdir as ld
def rep(old,new):
    li=ld('templates')
    codes={'templates/'+i:open('templates/'+i,'r',encoding='utf-8').read() for i in li}
    for i in codes:open(i,'w',encoding='utf-8').write(codes[i].replace(old,new))
#def read()