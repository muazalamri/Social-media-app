'my app functions module'
from rsa import *
from model import *
import os
import json
from flask_login import current_user
from sqlalchemy.sql import and_
def writeFeedback(user_id,ftype,toId,text):
    if not os.path.exists(f'feedbacks/{ftype}'):
        os.makedirs(f'feedbacks/{ftype}')
    with open(f'feedbacks/{ftype}/{toId}.json','a') as f:
        json.dump({'from':user_id,'text':text},f)
def addResponse(response,userId):
    add_to_db(Rsponse,**response,user_id=userId)
def setCustom(jsonData,user_id):
    data=json.load(jsonData)
    add_to_db(Customize,**data,user_id=user_id)
def setContact(id,data):
    user = load_data(User, filter=(User.id == id), limit=1)[0]
    links = user.links
    for i in ['face_book','you_tube','linkedin','x','instagram','web_site']:
        if links.filter(SocialLink.type==i).count()!=0:
            link = load_data(SocialLink,filter=and_(SocialLink.type==i,SocialLink.user_id==id),limit=1)[0]
            setattr(link,i,data[i])
        else:
            link = add_to_db(SocialLink,user_id=id,type=i,link=data[i])
            db.session.add(link)
        db.session.commit()
def like(post_id,user_id,interaction):
    'take post_id,user_id,interaction'
    add_to_db(Like,{'post_id':post_id,'user_id':user_id,'interaction':interaction})
def commentingPost(post_id,comment,user_id):
    id=add_to_db(Comment,**{'comment':comment,'user_id':user_id,'post_id':post_id})
    return id
def jionEvent(id,Eventid):
    appender(User,Event,id,Eventid,'event_memberships')
def unfollow(id,toUnfollowId):
    remover(User,User,id,toUnfollowId,'following')
def likeComment(comment_id,user_id,interaction):
    add_to_db(LikeComment,{'comment_id':comment_id,'user_id':user_id,'interaction':interaction})
def follow(id,toFollowId):
    appender(User,User,id,toFollowId,'following')
def createPodcast(user_id,**kwargs):
    add_to_db(Podcast,{'user_id':user_id,**kwargs})
def createPlayList(user_id,*ids,**kwargs):
    fatherId=add_to_db(PodcastPlayList,kwargs)
    appender(PodcastPlayList,Podcast,fatherId,ids)

def leave(id,**kwargs):
    pass
def send(id,**kwargs):
    pass
def askToFri(id,**kwargs):#to edit
    appender(User,User,'friendships',**kwargs)
def Privacy(id,key,value):
    add_to_db(Privacy,{'user_id':id,'key':key,'value':value})

def taransolate(id,**kwargs):
    pass
def createPost(request,user_id):
    text = request.form.get('Text')
    video_files = request.files.getlist('videoin')
    zip_files = request.files.getlist('zipInput')
    gif_files = request.files.getlist('gifInput')
    model_files = request.files.getlist('modelInput')

    postId=add_to_db(Post,user_id=user_id,text=text)
    post=load_data(Post,id=postId)[0]
    clip=False
    postId=str(postId)
    # Save the uploaded video files
    for video in video_files:
        if video:
            if post.videos==None:
                post.videos=''
            clip=True
            video.save(os.path.join(app.config['UPLOAD_FOLDER'],postId+'_vid_'+video.filename))
            post.videos+=video.filename+','
    if clip:
        post.videos=post.videos[:-1]
        clip=False
            
            

    # Save the uploaded zip file
    for zip_file in zip_files:
        if zip_file:
            if post.zips==None:
                post.zips=''
            clip=True
            zip_file.save(os.path.join(app.config['UPLOAD_FOLDER'],postId+'_zip_'+zip_file.filename))
            post.zips+=zip_file.filename+','
    if clip:
        post.zips=post.zips[:-1]
        clip=False
        

    # Save the uploaded gif file
    for gif_file in gif_files:
        if gif_file:
            if post.gifs==None:
                post.gifs=''
            clip=True
            gif_file.save(os.path.join(app.config['UPLOAD_FOLDER'],postId+'_gif_'+ gif_file.filename))
            post.gifs+=gif_file.filename+','
    if clip:
        post.gifs=post.gifs[:-1]
        clip=False

    # Save the uploaded 3D model file
    for model_file in model_files:
        if model_file:
            if post.models==None:
                post.models=''
            clip=True
            model_file.save(os.path.join(app.config['UPLOAD_FOLDER'],postId+'_model_'+model_file.filename))
            post.models+=model_file.filename+','
    if clip:
        post.models=post.models[:-1]
        clip=False

    return jsonify({'status':'ok'})
def CreateEvent(mangerId,**kwargs):
    add_to_db(Event,kwargs)
def editEvent(id,**kwargs):
    event=Event.query.filter_by(id=id).first()
    for key in kwargs:
        setattr(event,key,kwargs[key])
    db.session.commit()
def deletEvent(user_id,id,**kwargs):
    event=load_data(Event,id=id)
    if event.manager_id==user_id:
        db.session.delete(event)
        db.session.commit()
def editPost(id,**kwargs):
    setData(Post,id,kwargs)
    db.session.commit()
def deletPost(id,**kwargs):
    post=load_data(Post,id)
    db.session.delete(post)
    db.session.commit()
def editGroup(id,**kwargs):
    setData(Group,id,kwargs)
def deletGroup(id,**kwargs):
    group=load_data(Group,id=id)
    db.session.delete(group)
    db.session.commit()
def editUser(id,**kwargs):
    user=User.query.filter_by(id=id).first()
    for key in kwargs:
        setattr(user,key,kwargs[key])
    db.session.commit()
def deletUser(id,**kwargs):
    user=load_data(User,id=id)[0]
    db.session.delete(user)
    db.session.commit()


def Upgrade(id):
    user=load_data(User,id=id)[0]
    user.premium=1
    db.session.commit()
def Downgrade(id):
    user=load_data(User,id=id)[0]
    user.premium=0
    db.session.commit()
def addFriend(id,friendId):
    user = load_data(User, filter=(User.id == id), limit=1)[0]
    friend = load_data(User, filter=(User.id == friendId), limit=1)[0]
    user.friends.append(friend)
    db.session.commit()
    
def bookMarkMassage(id,**kwargs):
    pass
def unreadMassage(id,**kwargs):
    pass
def DeletMassage(id,**kwargs):
    pass
def transFareMassage(id,**kwargs):
    pass
def AddMassageLabel(id,**kwargs):
    pass
def handelFile(file,path):
    with open(path,'wb') as f:
        f.write(file)
def feedbackUser(id,**kwargs):
    writeFeedback(id,'user',**kwargs)
def feedbackEvent(id,**kwargs): 
    writeFeedback(id,'event',**kwargs)
def feedbackGroup(id,**kwargs):
    writeFeedback(id,'group',**kwargs)
def feedbackPost(id,**kwargs):
    writeFeedback(id,'post',**kwargs)
def createGroup(user_id,**kwargs):
    group=Group(**kwargs)
    db.session.add(group)
    db.session.commit()
    addGroupAdmin(user_id=user_id,group_id=group.id)
    db.session.commit()
    return group.id
def addGroupAdmin(user_id,group_id):
    user = load_data(User, filter=(User.id == user_id), limit=1)[0]
    group = load_data(Group, filter=(Group.id == group_id), limit=1)[0]
    group.admins.append(user)
    db.session.commit()
def InvaiteToGroup(id,**kwargs):
    pass
def editAccountSitting(id,**kwargs):
    pass
def joinGroup(user_id,group_id):
    user=load_data(User,id=user_id)[0]
    group=load_data(Group,id=group_id)
    user.group_memberships.append(group)
    db.session.commit()
def GroupMebber(group):
    members = group.members.all()
    return members
def eventManager(id,user_id):
    event=Event.query.filter_by(id=id).first()
    event.manager=load_data(User,id=id)[0].id
    db.session.commit()
def eventMembers(event):
    members = event.members.all()
    return members