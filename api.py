#--------------load libs-----------
from flask import request, redirect,jsonify
from model import *
from flask_login import current_user
from appUtlits import *
from app import *
from styling import *
from json import load as loader_fun
import asyncio
from dashboard.charting import *
#likapi
@app.route('/ren')
def blue():
    con_chart=contentChart(1)
    return jsonify(con_chart.render())
@app.route('/liking/<id>')
def likeing(id):return jsonify({'lnum':99})
@app.route('/unliking/<id>')
def unliking(id):return jsonify({'lnum':99})
@app.route('/getter/<p>')
def gety(p):
    print(current_user.id)
    return {'status':'ok'} 
#load post
@app.route('/load')
def ret():
    return jsonify({'data':app.dm.loadnew()})
#load post
@app.route('/userpost/<id>')
def uposts(id):
    page=request.args.get('page')
    return jsonify({'data':app.dm.loadby(page_num=int(page),filter=(Post.user_id==id))})
@app.post('/AIeditor')
def applying():
    text=asyncio.run(app.dm.writing(request.form.get('edited')))
    #print(text['res'])
    return text['res'][7:-4]
@app.route('/loadg')
def loadG():
    return app.dm.group_load()
@app.route('/ask', methods=['POST']) 
def askAI():
    print(request.form)
    data=app.dm.AIanswer(request.form.get('prompt'))
    print('result is',data)
    return jsonify({'ans':data})
@app.route('/adds', methods=['POST']) 
def add_posts():
    return createPost(request,user_id=current_user.id)

@app.route('/load_groups')
def Gload():return jsonify(app.dm.group_loading())
@app.route('/edit/personal',methods=['POST'])
def peredit():
    id = 1 #current_user.id
    data = request.form
    image=request.files.get('img')
    #cover = request.files.get('cover')
    #cover.save(app.config['UPLOAD_FOLDER']+cover.filename)
    if image:
        image.save(os.path.join('static/images/user/', str(id)+'.'+image.filename.split('.')[-1]))
    data=dict(data)
    editUser(id,**data)
    return jsonify({'status':'ok'})
@app.route('/edit/contact')
def editContact():
   data=request.form
   setContact(1,data)
   return jsonify({'status':'ok'})
@app.route('/edit/massegeing')
def editMassage():
    return jsonify({'status':'ok'})
@app.route('/uploading', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = file.filename
        file.save(app.config['UPLOAD_FOLDER']+ filename)
        return 'File successfully uploaded'
@app.route('/add_event', methods=['POST'])
def add_event():
    if request.method == 'POST':
        data = request.form
        data=dict(data)
        data['date']=datetime.strptime(data['date'], '%Y-%m-%d')
        data['manager_id']=1
        CreateEvent(1,**data)
        return redirect('/')

@app.route('/add', methods=['GET', 'POST'])  # Handle both GET and POST on root
def adding():
    # Access form data
    try:
        data = request.form  # Accesses multipart/form-data
        T_value = data.get('Text')  # Assuming you have a field named 'T'
        print(f"Received T: {T_value}")
        add_to_db(Post,user_id=1,text=text)
        # Access file data
        if 'fileInput' in request.files:
            file = request.files['fileInput']
            if file.filename != '':
                # process file, save it,...
                pass
        return jsonify({'message': 'Data received successfully!', 'T_value': T_value})
    except Exception as e:
        print(f"Error handling POST request: {e}")
        return "Bad Request - Error processing form data", 400

@app.route('/liking')
def add_like():
    postId = request.args.get("post")
    interaction = request.args.get("interaction")
    user_id=1
    alrady=db.session.query(Like).filter(and_(Like.post_id==postId,Like.interaction==interaction)).count()==0
    if alrady:
        add_to_db(Like,**{'post_id':postId,'user_id':user_id,'interaction':interaction})
        return jsonify({'status':'ok'})
    return jsonify({'status':'done'})
@app.route('/add_like_comment', methods=['POST'])
def add_like_comment():
    if request.method == 'POST':
        data = request.form
        data['user_id']=current_user.id
        add_to_db(likeComment,**data)
        return jsonify({'status':'ok'})
@app.route('/addFri')
def add_friend():
    fri=request.args.get('to')
    id=1
    user=load_data(User,id=id)[0]
    user.friendships.append(load_data(User,id=fri)[0])
    db.session.commit()
    return jsonify({'status':'ok'})

@app.route('/add_follow', methods=['POST'])
def add_follow():
    if request.method == 'POST':
        data = request.form
        data['user_id']=current_user.id
        add_to_db(follow,**data)
        return jsonify({'status':'ok'})
@app.route('/add_group', methods=['POST'])
def add_agroup():
    id = 1  # Replace with the appropriate value
    data = request.form
    data = dict(data)
    if 'img' not in request.files:
        return "Image file is required", 400
    img = request.files['img']

    count = db.session.query(Group).count()
    path = f'static/images/group/{count+1}.{img.filename.split(".")[-1]}'

    # Ensure the directory exists
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    img.save(path)
    print('___' * 20, 'add new group')

    id = createGroup(id, **data, img=path)
    return redirect('/')
@app.route('/mycoms')
def pri():return str(app.dm.comments(1))
@app.route('/myint')
def interactioning():return str(app.dm.interaction(1))
@app.route('/elementcomment', methods=['POST'])
def elementcomment():
    data = request.form
    if data['type']=='post':
        id=1
        post=load_data(Post,id=data['id'])[0]
        post.comments.append(Comment(user_id=id,comment=data['text']))
        db.session.commit()
    elif data['type']=='podcast':
        id=1
        podcast=load_data(Podcast,id=data['id'])[0]
        podcast.comments.append(PodcastComment(user_id=id,comment=data['text']))
        db.session.commit()
    elif data['type']=='playlist':
        id=1
        playlist=load_data(PodcastPlayList,id=data['id'])[0]
        playlist.comments.append(PodcastPlayListComment(user_id=id,comment=data['text']))
        db.session.commit()
    elif data['type']=='event':
        id=1
        event=load_data(Event,id=data['id'])[0]
        event.comments.append(Comment(user_id=id,comment=data['text']))
        db.session.commit()
    elif data['type']=='group':
        id=1
        group=load_data(Group,id=data['id'])[0]
        group.comments.append(Comment(user_id=id,comment=data['text']))
        db.session.commit()
    
    return jsonify({'status': 'ok'})
@app.route('/join')
def jionGroup():
    id=1
    to=request.args.get('to')
    add_to_group
    return 
@app.route('/follow')#not work
def follower():
    id=1
    to=request.args.get('to')
    load_data(User,id=id)[0].following.append(load_data(User,id=to)[0])
    return jsonify({'status': 'ok'})
@app.route('/elementlike', methods=['POST'])
def elementlike():
    data = request.form
    if data['type']=='post':
        id=1
        post=load_data(Post,id=data['id'])[0]
        post.likes.append(Like(user_id=id,interaction=data['interaction']))
        db.session.commit()
    elif data['type']=='podcast':
        id=1
        podcast=load_data(Podcast,id=data['id'])[0]
        podcast.likes.append(PodcastLike(user_id=id,interaction=data['interaction']))
        db.session.commit()
    elif data['type']=='playlist':
        id=1
        playlist=load_data(PodcastPlayList,id=data['id'])[0]
        playlist.likes.append(PodcastPlayListLike(user_id=id,interaction=data['interaction']))
        db.session.commit()
    elif data['type']=='event':
        id=1
        event=load_data(Event,id=data['id'])[0]
        event.likes.append(Elike(user_id=id,interaction=data['interaction']))
        db.session.commit()
    elif data['type']=='group':
        id=1
        group=load_data(Group,id=data['id'])[0]
        group.likes.append(glike(user_id=id,interaction=data['interaction']))
        db.session.commit()
    
    return jsonify({'status': 'ok'})


    
@app.route('/commentPost', methods=['POST'])
def comP():
    id=1
    data=request.form
    comid=commentingPost(data['id'],data['commentText'],id)
    comment=load_data(Comment,id=comid)[0]
    return jsonify({'name': comment.author.username, 'img': f'/static/images/user/{comment.user_id}.jpg', 'time': app.dm.calculate_time_diff(comment.timestamp), 'text': comment.comment})
@app.route('/add_podcast', methods=['POST'])
def add_podcast():
    if request.method == 'POST':
        data = request.form
        createPodcast(current_user.id,**data)
        return redirect('/')
@app.route('/add_playList', methods=['POST'])
def add_playList():
    if request.method == 'POST':
        data = request.form
        id = request.form.getlist('id')
        createPlayList(current_user.id,*id,**data)
        return redirect('/')
@app.route('/commet_podcast', methods=['POST'])
def commet_podcast():
    if request.method == 'POST':
        data = request.form
        data['user_id']=current_user.id
        add_to_db(PodcastComment,**data)
        return jsonify({'status':'ok'})
@app.route('/like_podcast', methods=['POST'])
def like_podcast():
    if request.method == 'POST':
        data = request.form
        data['user_id']=current_user.id
        add_to_db(PodcastLike,**data)
        return jsonify({'status':'ok'})
@app.route('/like_playlist', methods=['POST'])
def like_playlist():
    if request.method == 'POST':
        data = request.form
        data['user_id']=current_user.id
        add_to_db(PodcastPlayListLike,**data)
        return jsonify({'status':'ok'})
@app.route('/add_to_group', methods=['POST'])
def add_to_group():
    id=1
    to=request.args.get('to')
    group=load_data(Group,id=to)[0]
    group.group_members.append(load_data(User,id=id)[0])
    return redirect(f'/group-detail/{group.name}')
@app.route('/personalize')
def personing():
    id=1
    #data=dict(loader_fun(open(f'json/personalize/{id}.json','rb')))
    return jsonify({'data':[{
    "type":"class",
    "value":"header-title",
    "attribute":"style.background-color",
    "newValue":"red"
    },{
  "type": "class",
  "value": "iq-sidebar",
  "attribute": "style.cssFloat",
  "newValue": "right"
    }]})
@app.route('/add_to_event', methods=['POST'])
def add_to_event():
    if request.method == 'POST':
        data = request.form
        event=load_data(Event,filter=(Event.id==data['event_id']),limit=1)[0]
        joinEvent(current_user,event)
        return redirect('/')
@app.route('/add_to_playlist', methods=['POST'])
def add_to_playlist():
    if request.method == 'POST':
        data = request.form
        playlist=load_data(PodcastPlayList,filter=(PodcastPlayList.id==data['playlist_id']),limit=1)[0]
        playlist.items.append(load_data(Podcast,filter=(Podcast.id==data['podcast_id']),limit=1)[0])
        db.session.commit()
        return jsonify({'status':'ok'})
@app.route('/view_podcast', methods=['POST'])
def view_podcast():
    if request.method == 'POST':
        data = request.form
        podcast=load_data(Podcast,filter=(Podcast.id==data['podcast_id']),limit=1)[0]
        podcast.views+=1
        db.session.commit()
        return jsonify({'status':'ok'})
@app.route('/view_playlist', methods=['POST'])
def view_playlist():
    if request.method == 'POST':
        data = request.form
        playlist=load_data(PodcastPlayList,filter=(PodcastPlayList.id==data['playlist_id']),limit=1)[0]
        playlist.views+=1
        db.session.commit()
        return jsonify({'status':'ok'})
@app.route('/podcast_listening', methods=['POST'])
def podcast_listening():
    if request.method == 'POST':
        data = request.form
        if PodcastListen.query.filter_by(user_id=current_user.id,podcast_id=data['podcast_id']).first():
            listening=PodcastListen.query.filter_by(user_id=current_user.id,podcast_id=data['podcast_id']).first()
            listening.percent=data['percent']
            db.session.commit()
            return jsonify({'status':'ok'})
        else:
            listening=PodcastListen(user_id=current_user.id,podcast_id=data['podcast_id'],time=data['time'])
            db.session.add(listening)
            db.session.commit()
            return jsonify({'status':'ok'})
@app.route('/playlist_listening', methods=['POST'])
def playlist_listening():
    if request.method == 'POST':
        data = request.form
        if PodcastPlayListListen.query.filter_by(user_id=current_user.id,playlist_id=data['playlist_id']).first():
            listening=PodcastPlayListListen.query.filter_by(user_id=current_user.id,playlist_id=data['playlist_id']).first()
            listening.percent=data['percent']
            db.session.commit()
            return jsonify({'status':'ok'})
        else:
            listening=PodcastPlayListListen(user_id=current_user.id,playlist_id=data['playlist_id'],time=data['time'])
            db.session.add(listening)
            db.session.commit()
            return jsonify({'status':'ok'})
@app.route('/video_listening', methods=['POST'])
def video_listening():
    if request.method == 'POST':
        data = request.form
        if VideoWatch.query.filter_by(user_id=current_user.id,video_id=data['video_id']).first():
            listening=VideoWatch.query.filter_by(user_id=current_user.id,video_id=data['video_id']).first()
            listening.percent=data['percent']
            db.session.commit() 
            return jsonify({'status':'ok'})
        else:
            listening=VideoWatch(user_id=current_user.id,video_id=data['video_id'],time=data['time'])
            db.session.add(listening)
            db.session.commit()
            return jsonify({'status':'ok'})
