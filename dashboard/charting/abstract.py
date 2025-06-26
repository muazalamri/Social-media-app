class style:
    def __init__(self,lineTension=0,backgroundColor='transparent',borderColor='#007bff'
            ,borderWidth=4,pointBackgroundColor='#007bff'):
        self.lineTension=lineTension
        self.backgroundColor=backgroundColor
        self.borderWidth=borderWidth
        self.borderColor=borderColor
        self.pointBackgroundColor=backgroundColor
    def render(self):
        return {
            'lineTension':self.lineTension,'backgroundColor':self.backgroundColor
            ,'borderColor':self.borderColor,'borderWidth':self.borderWidth,
            'pointBackgroundColor':self.pointBackgroundColor
        }
class dataset:
    def __init__(self,data,style=style(),*args,**kwargs):
        self.style=style
        self.data=data
    def render(self,maxval=None):
        if maxval is not None:
            scale=maxval/max(self.data)
            self.data=[i*scale for i in data]
        return {
            'data':self.data,
            **self.style.render()
            }
class Labels:
    def __init__(self,labels):
        self.labels=labels
    def render(self):
        return self.labels
class options:
    def __init__(self,display=False,boxPadding=3):
        self.opt=self.setoption(display,boxPadding)
    def setoption(self,display,boxPadding):
        return {
              'plugins': {
                'legend': {
                  'display': display
                },
                'tooltip': {
                  'boxPadding': boxPadding
                }
              }
            }
    def render(self):
        return self.opt
class chart:
    def __init__(self,labels,datasets,options=options(),chart_type='line',display=False,boxPadding=3):
        self.labels=labels.render()
        self.datasets=[i.render() for i in datasets]
        self.options=options.render()
    def render(self):
        return  {
                     'type': 'line',
                     'data':{
                         'labels':self.labels,
                         'datasets':self.datasets
                     },
                     **self.options
                }
            