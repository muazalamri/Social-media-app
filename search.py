from numpy import array
from model import *
#from simularty import simualrty
def searchDict(data,target,types,threhold):
    results=[]
    for place in data:
        if data[place]['type'] in types:
            for value in data[place]['data']():
                value['source']=rank(value['data'],target)

                if value['source']>threhold:results.append(value)
    return results

def sentence_simularity(text,target):
    '''text=sentencer(text)
    return array(simualrty()).sum/(100*len(text))'''
    return 0.05
def intersection(text,target):
    text,target=list(set(text.split())),list(set(target.split()))
    array([int(i in text) for i in target]).sum()
    return array([(1 if i in text else 0) for i in target]).sum()
def sentencer(text:str):
    sapretors=['.',',',';',':']
    text=text.split(sapretors[0])
    for sapretor in sapretors:
        new=[]
        for i in text:
            new+=i.split(sapretor)
    return new
def rank(text,target,alpa=1):
    res=len(target)/max(max(list(map(len,sentencer(text)))),1)
    factor=min(0.9,alpa*max(res,0.1))
    return intersection(text,target)
def searchFun(target,threhold=0.5,types=['posts','groups','massegs','person'],postfilter=None,groupfilter=None,massagesfilter=None,personfilter=None):
    places={
        'posts':{'type':'posts','data':lambda : [{'type':'post','id':post.id ,'data':post.text} for post in load_data(Post,filter=postfilter)]},
        'groups':{'type':'groups','data':lambda : [{'type':'group','id':group.id ,'data':group.name+' & '+group.disc} for group in load_data(Group,filter=groupfilter)]},
        'massages':{'type':'massegs','data':lambda : [{'type':'massage','id':massage.id ,'data':massage.text} for massage in load_data(Message,filter=massagesfilter)]},
        'person':{'type':'person','data':lambda : [{'type':'person','id':person.id ,'data':person.username} for person in load_data(User,filter=personfilter)]}
    }
    return searchDict(places,target,types,threhold)