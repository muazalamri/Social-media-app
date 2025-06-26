from model import *
from datetime import datetime
import json
from rsa import *
from coldstart import startup
import markdown
from random import randint as random
from styling import *
from sqlalchemy.sql import and_
from pydub import AudioSegment
from search import searchFun
from agent import Asseten
import asyncio
asset=Asseten()
def get_audio_length(file_path):
    audio = AudioSegment.from_file(file_path)
    return len(audio) / 1000
def section():
   sec=int(open('num.index','r',encoding='utf-8').read())
   open('num.index','w',encoding='utf-8').write(str(sec+1))
   return sec
class DataManager:
    'creater to use on loading data from db'
    def answer(self,prompt):
        data=asyncio.run(asset.answer(prompt))
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@',data)
        return {'<br><h1>'+i+':</h1>':'<br>'+md_to_html(str(data[i])).replace('\n','<br>') for i in data }
    def AIanswer(self,prompt):
        data=asyncio.run(asset.answer(prompt))
        return md_to_html(str(data['answer'])).replace('\n','<br>')
    async def AItopicer(self,prompt):
        print('prompt--------->',prompt)
        text=await asset.topicer(prompt) 
        return {'res':text}
    async def writing(self,text):
        text=await asset.write(text)
        return {'res':text}
        
    def loadnew(self):
        #startup()
        indexs=[random(1,db.session.query(Post).count()) for i in range(10)]
        posts = load_data(Post, limit=6,filter=(Post.id.in_(indexs)))
        return [{
            'section':section(),
            'id': post.id,
            'sender': post.author.username,
            'senderid': post.author.id,
            'title': md_to_html(post.title),
            'text': md_to_html(post.text),
            'withmed': False,#bool(post.media),
            #'media': post.media.split(',') if post.media else [],
            'time': self.calculate_time_diff(post.timestamp),
            'Likes': post.likes.count(),
            'liker': [like.user.username for like in self.sub_v(post.likes)],
            'other': post.likes.count() > 5,
            'num_com': post.comments.count(),
            'senderimg': f'/static/images/user/{post.user_id}.jpg',
            'comer': [{'name': comment.author.username, 'img': f'/static/images/user/{comment.user_id}.jpg', 'time': self.calculate_time_diff(comment.timestamp), 'text': comment.comment} for comment in self.sub_v(post.comments)],
            'com_other': post.comments.count() > 5,
            'num_share': post.shares,
            'flowed': id in [followed.id for followed in post.author.followed]
        } for post in posts]
    def loadpost(self,id):
        post = load_data(Post,id=id)[0]
        return {
            'id': post.id,
            'sender': post.author.username,
            'senderid': post.author.id,
            'type': post.type,
            'text':md_to_html(post.text),
            'withmed': False,#bool(post.media),
            #'media': post.media.split(',') if post.media else [],
            'time': self.calculate_time_diff(post.timestamp),
            'Likes': post.likes.count(),
            'likers': [like.user.username for like in self.sub_v(post.likes)],
            'other': post.likes.count() > 5,
            'num_com': post.comments.count(),
            'senderimg': f'/static/images/user/{post.user_id}.jpg',
            'comers': [{'name': comment.author.username, 'img': f'/static/images/user/{comment.user_id}.jpg', 'time': self.calculate_time_diff(comment.timestamp), 'text': comment.comment} for comment in self.sub_v(post.comments)],
            'com_other': post.comments.count() > 5,
            'num_share': post.shares,
            'flowed': id in [followed.id for followed in post.author.followed]
        }
    def loadby(self,filter=None):
        #startup()
        posts = load_data(Post, limit=6,filter=filter)
        return [{
            'id': post.id,
            'sender': post.author.username,
            'senderid': post.author.id,
            'type': post.type,
            'text': md_to_html(post.text),
            'withmed': False,#bool(post.media),
            #'media': post.media.split(',') if post.media else [],
            'time': self.calculate_time_diff(post.timestamp),
            'Likes': post.likes.count(),
            'liker': [like.user.username for like in self.sub_v(post.likes)],
            'other': post.likes.count() > 5,
            'num_com': post.comments.count(),
            'senderimg': f'/static/images/user/{post.user_id}.jpg',
            'comer': [{'name': comment.author.username, 'img': f'/static/images/user/{comment.user_id}.jpg', 'time': self.calculate_time_diff(comment.timestamp), 'text': comment.comment} for comment in self.sub_v(post.comments)],
            'com_other': post.comments.count() > 5,
            'num_share': post.shares,
            'flowed': id in [followed.id for followed in post.author.followed]
        } for post in posts]
    @staticmethod
    def sub_v(value):
        return value if value.count() < 5 else value[:5]
    def search(self,target):
        return searchFun(target)

    def edata(self,id=1):
        event = load_data(Event,filter=(Event.id==id), limit=1)[0]
        return {
            'ename': event.manager.username,
            'etype': event.type,
            'emeb': [{'name': member.user.username, 'img': f'/static/images/user/{member.user_id}.jpg'} for member in event.members],
            'emebn': (event.members.count()),
            'edisc': event.disc,
            #'eplace': event.place,
            #'eplan': event.plan,
            'eimg': f'/static/images/event/{event.id}.jpg',
            'ejoiners': [{'img': f'/static/images/user/{one["img"]}.jpg'} for one in event.members] * 5,
            'subes': event.subEvents
        }

    def suggester(self):
        indexs=[random(1,db.session.query(Group).count()) for i in range(10)]
        suggestions = load_data(Group,limit=9,filter=(Group.id.in_(indexs)))
        return [{'page_name': suggestion.name, 'shortdis': suggestion.disc, 'img': f'/static/images/group/{suggestion.id}.jpg'} for suggestion in suggestions]

    def event(self):
        events = load_data(Event, limit=6)
        return [{'name': event.name, 'img': f'/static/images/event/{event.id}.jpg', 'time': event.date} for event in events]
    def podSubject(self):
        return [{'img':'/static/images/page-img/n1.jpg','name':'math','podcasts_num':20} for i in range(20)]
    def podcast(self):
        print('get some data')
        indexs=[random(1,db.session.query(Podcast).count()) for i in range(20)]
        podcasts=load_data(Podcast,filter=Podcast.id.in_(indexs))
        return [{'img': podcast.img, 'name': podcast.name, 'disc': podcast.disc,'time': "1:30:17",'lenght':'3m'} for podcast in podcasts]
    def Recent(self):
        indexs=[random(1,db.session.query(Podcast).count()) for i in range(20)]
        podcasts=load_data(Podcast,filter=(Podcast.id.in_(indexs)))
        return [{'img': podcast.img, 'name': podcast.name, 'disc': podcast.disc,'time': "1:30:17",'lenght':'3m'} for podcast in podcasts]
    def Top(self):
        indexs=[random(1,db.session.query(Podcast).count()) for i in range(20)]
        podcasts=load_data(Podcast,filter=Podcast.id.in_(indexs))
        return [{'img': podcast.img, 'name': podcast.name, 'disc': podcast.disc,'time': "1:30:17",'lenght':'3m'} for podcast in podcasts]
    def FORYOU(self,filter=None):
        indexs=[random(1,db.session.query(Podcast).count()) for i in range(20)]
        podcasts=load_data(Podcast,filter=Podcast.id.in_(indexs))
        return [{'img': podcast.img, 'name': podcast.name, 'disc': podcast.disc,'time': "1:30:17",'lenght':'3m'} for podcast in podcasts]
    def Choise(self,filter=None):
        indexs=[random(1,db.session.query(Podcast).count()) for i in range(20)]
        podcasts=load_data(Podcast,filter=Podcast.id.in_(indexs))
        return [{'img': podcast.img, 'name': podcast.name, 'disc': podcast.disc,'time': "1:30:17",'lenght':'3m'} for podcast in podcasts]
    def New(self,filter=None):
        indexs=[random(1,db.session.query(Podcast).count()) for i in range(20)]
        podcasts=load_data(Podcast,filter=Podcast.id.in_(indexs))
        return [{'img': podcast.img, 'name': podcast.name, 'disc': podcast.disc,'time': "1:30:17",'lenght':'3m'} for podcast in podcasts]
    def Trendingpod(self):
        indexs=[random(1,db.session.query(Podcast).count()) for i in range(20)]
        podcasts=load_data(Podcast,filter=Podcast.id.in_(indexs))
        return [{'img': podcast.img, 'name': podcast.name, 'disc': podcast.disc,'time': "1:30:17",'lenght':'3m'} for podcast in podcasts]
    def Audio(self,filter=None):
        indexs=[random(1,db.session.query(Podcast).count()) for i in range(20)]
        podcasts=load_data(Podcast,filter=Podcast.id.in_(indexs))
        return [{'img': podcast.img, 'name': podcast.name, 'disc': podcast.disc,'time': "1:30:17",'lenght':'3m'} for podcast in podcasts]
    #-------------------------subjects routes
    def sub_podcast(self,filter=None):
        indexs=[random(1,db.session.query(Podcast).count()) for i in range(20)]
        podcasts=load_data(Podcast,filter=and_(Podcast.id.in_(indexs),(Podcast.subject==filter)))
        return [{'img': podcast.img, 'name': podcast.name, 'disc': podcast.disc,'time': "1:30:17",'lenght':'3m'} for podcast in podcasts]
    def sub_Recent(self,filter=None):
        indexs=[random(1,db.session.query(Podcast).count()) for i in range(20)]
        podcasts=load_data(Podcast,filter=and_(Podcast.id.in_(indexs),(Podcast.subject==filter)))
        return [{'img': podcast.img, 'name': podcast.name, 'disc': podcast.disc,'time': "1:30:17",'lenght':'3m'} for podcast in podcasts]
    def sub_Top(self,filter=None):
        indexs=[random(1,db.session.query(Podcast).count()) for i in range(20)]
        podcasts=load_data(Podcast,filter=and_(Podcast.id.in_(indexs),(Podcast.subject==filter)))
        return [{'img': podcast.img, 'name': podcast.name, 'disc': podcast.disc,'time': "1:30:17",'lenght':'3m'} for podcast in podcasts]
    def sub_FORYOU(self,filter=None):
        indexs=[random(1,db.session.query(Podcast).count()) for i in range(20)]
        podcasts=load_data(Podcast,filter=and_(Podcast.id.in_(indexs),(Podcast.subject==filter)))
        return [{'img': podcast.img, 'name': podcast.name, 'disc': podcast.disc,'time': "1:30:17",'lenght':'3m'} for podcast in podcasts]
    def sub_Choise(self,filter=None):
        indexs=[random(1,db.session.query(Podcast).count()) for i in range(20)]
        podcasts=load_data(Podcast,filter=and_(Podcast.id.in_(indexs),(Podcast.subject==filter)))
        return [{'img': podcast.img, 'name': podcast.name, 'disc': podcast.disc,'time': "1:30:17",'lenght':'3m'} for podcast in podcasts]
    def sub_New(self,filter=None):
        indexs=[random(1,db.session.query(Podcast).count()) for i in range(20)]
        podcasts=load_data(Podcast,filter=and_(Podcast.id.in_(indexs),(Podcast.subject==filter)))
        return [{'img': podcast.img, 'name': podcast.name, 'disc': podcast.disc,'time': "1:30:17",'lenght':'3m'} for podcast in podcasts]
    def sub_Trendingpod(self,filter=None):
        indexs=[random(1,db.session.query(Podcast).count()) for i in range(20)]
        podcasts=load_data(Podcast,filter=and_(Podcast.id.in_(indexs),(Podcast.subject==filter)))
        return [{'img': podcast.img, 'name': podcast.name, 'disc': podcast.disc,'time': "1:30:17",'lenght':'3m'} for podcast in podcasts]
    def sub_AudioBook(self,filter=None):
        indexs=[random(1,db.session.query(Podcast).count()) for i in range(20)]
        podcasts=load_data(Podcast,filter=and_(Podcast.id.in_(indexs),(Podcast.subject==filter)))#(Podcast.subject==filter)
    def podData(self,name):
        podcast = load_data(Podcast,filter=(Podcast.name==name), limit=1)[0]
        return {
            'name': podcast.name,
            'img':podcast.img,
            'disc':podcast.disc,
            'likes':len(podcast.likes),
            'liker': [like.user.username for like in podcast.likes[:5]],
            'other': len(podcast.likes) > 5,
            'num_com': len(podcast.comments),
            'comer': [{'name':comment.author.username,'img':f'/static/images/user/{comment.user_id}.jpg','time':self.calculate_time_diff(comment.timestamp),'text':comment.comment} for comment in podcast.comments[:5]],
            'num_share': podcast.shares,
            'com_other': len(podcast.comments) > 5
        }
    def users(self,id):
        user = load_data(User,filter=(User.id==id), limit=1)[0]
        return {'img': f'/static/images/user/{user.id}.jpg'}

    def notify(self):#to modify
        notifications = load_data(User, limit=5)
        return [{'img': f'/static/images/user/{user.id}.jpg', 'name': user.username, 'time': '3 hours'} for user in notifications]

    def infos_counter(self):#to modify
        return load_data(User, limit=1)[0].id

    def massage_loader(self,id):#to modify
        messages = load_data(Message, limit=5)
        return [{'img': f'/static/images/user/{message.sender_id}.jpg', 'name': message.sender.username, 'time': self.calculate_time_diff(message.timestamp)} for message in messages]

    def fri(self, id):
        user = load_data(User, filter=(User.id == id), limit=1)[0]
        friends = user.friendships
        return (friends.count())>5, friends.count(), [{'name': friend.username, 'img': f'/static/images/user/{friend.id}.jpg', 'fri': friend.friendships.count()} for friend in self.sub_v(friends)]

    def start(self):
        dic = {
            'infos_num': self.infos_counter(),
            'massages': self.massage_loader(1),
            'infos': self.notify()
        }
        dic['more'], dic['fri_num'], dic['friends'] = self.fri(1)
        return dic

    def group_load(self):
        groups = load_data(Group, limit=6)
        return [{'img': group.img,'mebs':group.group_members.all(),'member':group.group_members.count(),'posts':group.posts.count(), 'backImg': f'/static/images/group/8.jpg', 'name': group.name, 'disc': group.disc, 'visit': group.visits,'id':group.id}for group in groups]
    def group_loading(self):
        groups = load_data(Group, limit=6)
        return [{'img': group.img,'mebs':[{'id':member.id} for member in group.group_members.all()],'member':group.group_members.count(),'posts':group.posts.count(), 'backImg': f'/static/images/group/8.jpg', 'name': group.name, 'disc': group.disc, 'visit': group.visits,'id':group.id}for group in groups]
    def meping(self,Gname):
        group=load_data(Group,filter=(Group.name==Gname))[0]
        return {'img': group.img,'mebs':group.group_members.all(),'member':group.group_members.count(),'posts':group.posts.count(), 'backImg': f'/static/images/group/8.jpg', 'name': group.name, 'disc': group.disc, 'visit': group.visits,'id':group.id}
    def gpost(self):
        posts = load_data(Post, limit=1)
        return [{'img': f'/static/images/user/{post.user_id}.jpg', 'name': post.author.username, 'time': 'Just Now', 'med': f'/static/images/page-img/52.jpg'} for post in posts]

    def dital(self, id):
        group = load_data(Group, filter=(Group.id == id), limit=1)[0]
        return {'det': group.disc, 'type': 'public'}

    def list_group(self):
        groups = load_data(Group)
        return [group.name for group in groups]

    def check(self, name):
        return name in self.list_group()

    def getpro(self, id):
        follower_count = db.session.query(followers).filter(followers.c.followed_id == id).count()
        following_count = db.session.query(followers).filter(followers.c.follower_id == id).count()
        posts_num = db.session.query(Post).filter(Post.user_id == id).count()
        user = db.session.query(User).filter(User.id == id).first()
        
        return {
            'pfollowing': following_count,
            'name': user.username,
            'img': f'/static/images/user/{id}.jpg',
            'edu': user.edu,
            'working': user.work,
            'pfollowers': follower_count,
            'posts_num': posts_num,
            'uemail': user.email,
            'job': user.job,
            'con': user.con
        }

    def openMedF(self, id):
        return [None]

    def proimg_load(self, id):
        posts = [post.images for post in load_data(Post, exists_field='user_id', exists_value=id)]
        links = []
        for i in posts:
            if i is not None:
                links += [*i.split(',')]
        return links
    def my_fri(self, id):
        # Load friends where the user is the sender
        sent_friends = db.session.query(User).join(friends, friends.c.receiver_id == User.id).filter(friends.c.sender_id == id).all()
        # Load friends where the user is the receiver
        received_friends = db.session.query(User).join(friends, friends.c.sender_id == User.id).filter(friends.c.receiver_id == id).all()
        
        # Combine the data from both sent and received friends
        data = [
            {'img': f'/static/images/user/{friend.id}.jpg', 'name': friend.username, 'state': 'sent'} for friend in sent_friends
        ] + [
            {'img': f'/static/images/user/{friend.id}.jpg', 'name': friend.username, 'state': 'received'} for friend in received_friends
        ]
        
        return data

    def load_event(self):
        events = load_data(Event, limit=5)
        people = [
                load_data(Relation, exists_field='to_id', exists_value=event.id) for event in events # type: ignore
                      ] + [
                load_data(Relation, filter=range, exists_field='from_id', exists_value=event.id) for event in events # type: ignore
                 ]
        return [{'img': f'/static/images/event/{event.id}.jpg', 'name': event.manager.username, 'year': event.date.year, 'mon': event.date.month, 'day': event.date.day, 'disc': event.disc, 'people': [{'img': '/static/images/user/05.jpg'}]} for event in events]

    def all_event(self, Event=Event):
        events = load_data(Event, limit=5)
        return [{'img': f'/static/images/event/{event.id}.jpg', 'mon': event.date.month, 'day': event.date.day, 'year': event.date.year, 'name': event.name, 'disc': event.disc, 'meb': [{'img': '/static/images/user/9.jpg'}] * 3} for event in events]

    def fri_data(self,id):
        me = load_data(User, id=id)[0]
        return [{'back': f'/static/images/page-img/profile-bg{friend.id}.jpg', 'img': f'/static/images/user/{friend.id}.jpg', 'name': friend.username, 'disc': friend.job, 'uname': '@' + friend.username, 'follow': False} for friend in me.friendships.all()]
    def req(self,id):
        req_List=load_data(User,id=id)[0].friendships.all()
        return [{'name':fri.username,'fri_num':fri.friendships.count(),'id':fri.id}for fri in req_List]
    def suggested(self):return [{'name':fri.username,'fri_num':fri.friendships.count(),'id':fri.id}for fri in load_data(User)]
    def calculate_time_diff(self,timestamp):
        now = datetime.utcnow()
        diff = now - timestamp
        if diff.days > 0:
            return f"{diff.days} days ago"
        elif diff.seconds // 3600 > 0:
            return f"{diff.seconds // 3600} hours ago"
        elif diff.seconds // 60 > 0:
            return f"{diff.seconds // 60} minutes ago"
        else:
            return "just now"
    #to edit
    def blog_index(id):
        return {'title':'','routes':[{}],'icon':'','links':[{}]}
    def postsLikeDate(user_id):
        posts = load_data(Post, exists_field='user_id', exists_value=user_id)
        likes = [post.likes for post in posts]
        return likes