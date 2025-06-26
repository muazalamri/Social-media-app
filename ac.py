from model import *
from os import listdir as ld
from os import rename
def push():
    for i in ld('posts'):
        text=open('posts/'+i,encoding='utf-8').read()
        add_to_db(Post,user_id=1,text=text,title='.'.join([l for l in i.split('.')][1:-1]))

    for i in ld('static/audio'):
        add_to_db(Podcast,user_id=1,name=i.split('.')[0],disc=f'quran No. {i.split(".")[0]}',img='/static/images/user/1.jpg',subject='Quran')