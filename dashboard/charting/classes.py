from .abstract import *
from .__init__ import *
class contentChart(chart):
    def __init__(self,user_id,*args,**kwargs):
        data = content(user_id)
        self.postdata=dataset(data['posts'])
        self.podcastdata=dataset(data['podcasts'])
        self.eventdata=dataset(data['events'])
        labels=Labels(data['labels'])
        super().__init__(labels,[self.postdata,self.podcastdata,self.eventdata])
class flowerChart(chart):
    pass
class interaction(chart):
    pass
class commentChart(chart):
    pass
class earningChart(chart):
    pass