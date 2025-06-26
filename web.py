from flask import render_template, request
from app import *
from styling import *
import asyncio
@app.route('/web/<id>')
def blogy(id):
    print('r:',id) 
    return render_template('web/mainpage.html',w_routes=[{'name':'about','route':'/'},{'name':'home','route':'contact'},{'name':'home','route':'contact'},{'name':'home','route':'contact'},{'name':'home','route':'contact'},{'name':'home','route':'contact'},{'name':'home','route':'contact'}],lw_routes=[{'down':['1','2','3']},{'down':['1','2','3']}])
@app.route('/my_blog',methods=['GET','POST'])
def my_blog():
    if request.method=="GET":
        return render_template('mange.html',**app.dm.start())
    data = asyncio.run(app.dm.AItopicer(request.form.get('topic')))['res'].replace('\n','<br>')
    open('topic/'+request.form.get('topic')+'.txt','w',encoding='utf-8').write(data)
    data=(data[data.index(':')+1:].split('<br>'))
    data=['<div class="btn btn-primary">'+i+'</div>' for i in data if i!='']
    data='<br><br>'.join(data)
    return render_template('mange.html',**app.dm.start()).replace('titles will be here',data)
@app.route('/web/<id>/<postID>')
def blogypost(id,postID):
    return render_template('web/main.html',w_routes=[{'name':'about','route':'/'},{'name':'home','route':'contact'},{'name':'home','route':'contact'},{'name':'home','route':'contact'},{'name':'home','route':'contact'},{'name':'home','route':'contact'},{'name':'home','route':'contact'}],lw_routes=[{'down':['1','2','3']},{'down':['1','2','3']}],socials=[{'name':'NetInfo'}]*5).replace('{html_data_to_replace}',md_to_html(load_data(Post,id=postID)[0].text))#(.replace('<pre>','<p>').replace('</pre>','</p>'))
@app.route('/edit-blog')
def edit_blog():
    return render_template('edit-blog.html',
    list_name="routes",tag_name="route",add_text="add",tags=[{'value':'high','text': 'مهم'},{'value':'normal','text' : 'عادي'},{'value':'low','text' : 'غير مهم'}]
    ,**app.dm.start())
