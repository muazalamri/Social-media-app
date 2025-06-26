#--------------load libs-----------
from flask import render_template, request,jsonify
from model import *
from flask_login import login_required,current_user
from appUtlits import *
from app import *
from styling import *
import asyncio
from dashboard.utltis import *


#---------------ROUTES-----------------
#Route for the home page
@app.route('/ut')
def seed():return 'content:'+str(content(1))+'<br>interaction:'+str(interaction(1))+'<br>comments:'+str(comments(1))
@app.route('/dashapi')
def dash():
    print('@@'*200)
    return jsonify(content(1))
@login_required
@app.route('/')
def home():return render_template('index.html',modal=True,user_name='muaz',event_list=app.dm.event(),
                                  posts_com=app.dm.loadnew(),sugs=app.dm.suggester(),**app.dm.start())
#route /load
@app.route('/group')
def gro():return render_template('group.html',user_name='muaz',groups=app.dm.group_load(),**app.dm.start())
@app.route('/editor',methods=['GET','POST'])
def editing():
    return render_template('editor.html',**app.dm.start())
@app.route('/posts_list')
def posts_list():
    return render_template('listing.html',**app.dm.start())
#my posts route
@app.route('/myposts')
def mon():return render_template('myposts.html',user_name='muaz',**app.dm.start())
@app.route('/moneytize/<postId>')
def moneytize(postId):
    data=app.dm.loadpost(postId)
    return render_template('moneytize.html',user_name='muaz',**data,**app.dm.start()).format(text=data['text'])
#general routing
@app.route('/posts/<id>')
def routers(id):
    data=app.dm.loadpost(id)
    return render_template('moneytize.html',user_name='muaz',**data,**app.dm.start()).format(text=data['text'])
#general routing
@app.route('/<route>')
def router(route):return render_template(f'{route}',user_name='muaz',**app.dm.start())
#general routing
@app.route('/add_event')
def createEvent():
    return render_template('create-event.html',user_name='muaz',**app.dm.start())
@app.route('/add_group')
def createGroup():
    return render_template('create-group.html',user_name='muaz',**app.dm.start())
#veiw group detail route
@app.route('/group-detail/<Gname>')
def gro_det(Gname):
    if app.dm.check(Gname):
        group=load_data(Group,filter=(Group.name==Gname))[0]
        group.visits+=1
        db.session.commit()
        return render_template('group-detail.html',modal=True,user_name='muaz',Gname=Gname,**app.dm.meping(Gname),**app.dm.start())
    else:
        return render_template('GROUP NOT FUNDED.html')

#profile route
@app.route('/profile/<id>')
def prof(id): return render_template('profile.html',fris=app.dm.my_fri(1),posts_com=app.dm.loadby((User.id==id)),pimgs=app.dm.proimg_load(1),**app.dm.getpro(1),**app.dm.start())
@app.route('/profile-edit')
def prof_edit(): return render_template('profile-edit.html',**app.dm.getpro(1),**app.dm.start())
#events route
@app.route('/event')
def event_list(): return render_template('events.html',allevent=app.dm.all_event())
#friend list route
@app.route('/myfri')
def NEW():return render_template('friend-list.html',sugs=app.dm.fri_data(1))
@app.route('/fri_request')
def requestsList():return render_template('friend-request.html',sug_users=app.dm.suggested(),requests=app.dm.req(1))
#profile images routel
@app.route('/proimg')
def proimg(): return render_template('profile-images.html',imgs=['g']*7)
#event detail route
@app.route('/event-detail/<name>')
def edetail(name): return render_template('event-detail.html',modal=True,**app.dm.edata(),**app.dm.start())


#None connected to db need work
@app.route('/search')
def search():return render_template('search.html',results=app.dm.search(request.args.get('target')))
@app.route('/podcast')
def podcast():
    return render_template('podcast.html',podcasts=app.dm.podcast(),Top=app.dm.Top(),FORYOU=app.dm.FORYOU(),Choise=app.dm.Choise(),Trendingpod=app.dm.Trendingpod(),Recent=app.dm.Recent(),Audio=app.dm.Audio(),new=app.dm.New(),subs=app.dm.podSubject(),recent=app.dm.Recent(),**app.dm.start())
@app.route('/subject')
def podcastsubject():
    return render_template('subject.html',titles={'podcasts':app.dm.podcast(),'Top':app.dm.Top(),'FORYOU':app.dm.FORYOU(),'Choise':app.dm.Choise(),'Trendingpod':app.dm.Trendingpod(),'Recent':app.dm.Recent(),'Audio':app.dm.Audio(),'new':app.dm.New(),'subs':app.dm.podSubject(),'recent':app.dm.Recent()},**app.dm.start())
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html',**app.dm.start())
@app.route('/podcasts/<name>')
def podcasts(name):
    return render_template('podcasts.html',podcasts=app.dm.podcast(),id=name,**app.dm.podData(name),**app.dm.start())
@app.route('/edit-post')
def blog_main():
    return render_template(f'edit-post.html',**app.dm.start())
@app.route('/asset',methods=['POST','GET'])
def reply():
    if request.method == 'POST':
        data = request.form.get('Qu')
        app.dm.answer(data)
        return render_template('asset.html',**app.dm.start()).format(rep=app.dm.answer(data))
    else:
        return render_template('asset.html',rep='',**app.dm.start())