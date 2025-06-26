from app import app
from loaders import *
from appUtlits import *
from auth import *
from rank import rank
from coldstart import *
from api import *
from UX_UI import *
from search import *
from ac import push
from web import *
setup=False
setups=True
if setup:
    with app.app_context():
        db.drop_all()
        db.create_all()
        startup()
        print('='*20,'pushing')
        push()
        print('*'*20,'pushed')
        setup=False
else:
    with app.app_context():
        db.create_all()
app.dm=DataManager()
app.ranker=rank
#------------Create the database and ta---------------
#-----------App runing-------------------
app.run()