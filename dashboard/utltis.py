import sys

sys.path.append('../')

from model import *
from datetime import datetime, date, timedelta
def filtering(elementlist,time,time_prototype):
    datetime=lambda s : getattr(s,time_prototype)
    date=lambda s : getattr(datetime(s),'date')()
    return list(filter((lambda s:date(s)==time),elementlist))
def lsum(data):
    num=0
    for i in data:
        num+=i
    return num

def genDateRange(start_year, end_year, start_month=1, end_month=12, start_day=1, end_day=31):
    """
    Generate a list of valid dates in YYYY-MM-DD format between specified ranges
    
    Args:
        start_year: Starting year (inclusive)
        end_year: Ending year (inclusive)
        start_month: Starting month (default 1)
        end_month: Ending month (default 12)
        start_day: Starting day (default 1)
        end_day: Ending day (default 31)
    
    Returns:
        List of date strings in YYYY-MM-DD format
    """
    date_list = []
    
    try:
        start_date = date(start_year, start_month, start_day)
        end_date = date(end_year, end_month, end_day)
        
        if start_date > end_date:
            raise ValueError("Start date must be before end date")
            
        current_date = start_date
        
        while current_date <= end_date:
            date_list.append(current_date.isoformat())
            current_date += timedelta(days=1)
            
    except ValueError as e:
        print(f"Invalid date parameters: {e}")
        return []
    
    return date_list
post_filter=lambda posts,d : [post for post in posts if (post.timestamp.date() if hasattr(post.timestamp, 'date') else post.timestamp) == d]
event_filter=lambda events,d : [event for event in events if (event.date.date() if hasattr(event.date, 'date') else event.date) == d]
podcast_filter=lambda podcasts,d : [podcast for podcast in podcasts if (podcast.time.date() if hasattr(podcast.time, 'date') else podcast.time) == d]
def content(user_id,start=(2025,4,26),end=(2025,5,14)):
    contents = {'date':{},'labels':[],'posts':[],'events':[],'podcasts':[]}
    posts = load_data(Post, exists_field='user_id', exists_value=user_id)
    podcasts = load_data(Podcast, exists_field='user_id', exists_value=user_id)
    events = load_data(Event, exists_field='manager_id', exists_value=user_id)
    
    # Extract dates from each model (converting datetime to date if needed)
    post_dates = [post.timestamp.date() if hasattr(post.timestamp, 'date') else post.timestamp for post in posts]
    podcast_dates = [podcast.time.date() if hasattr(podcast.time, 'date') else podcast.time for podcast in podcasts]
    event_dates = [event.date.date() if hasattr(event.date, 'date') else event.date for event in events]
    
    # Combine and get unique dates
    dates = list(set(post_dates + podcast_dates + event_dates))
    
    for d in dates:
        date_str = d.isoformat()  # Convert date to string in YYYY-MM-DD format
        contents['date'][date_str]=d
    for i in genDateRange(start[0],end[0],start[1],end[1],start[2],end[2]):
        contents['labels']+=[i]
        if i not in contents['date']:
            contents['posts'].append(0)
            contents['events'].append(0)
            contents['podcasts'].append(0)
        else :
            contents['posts'].append(len(post_filter(posts,contents['date'][i])))
            contents['events'].append(len(event_filter(events,contents['date'][i])))
            contents['podcasts'].append(len(podcast_filter(podcasts,contents['date'][i])))
    return contents

def interaction(user_id,start=(2025,4,26),end=(2025,5,14)):
    interactions = {'date':{},'labels':[],'posts':[],'events':[],'podcasts':[]}
    posts = load_data(Post, exists_field='user_id', exists_value=user_id)
    podcasts = load_data(Podcast, exists_field='user_id', exists_value=user_id)
    events = load_data(Event, exists_field='manager_id', exists_value=user_id)
    
    # Extract dates from each model
    post_dates = [post.timestamp.date() if hasattr(post.timestamp, 'date') else post.timestamp for post in posts]
    podcast_dates = [podcast.time.date() if hasattr(podcast.time, 'date') else podcast.time for podcast in podcasts]
    event_dates = [event.date.date() if hasattr(event.date, 'date') else event.date for event in events]
    
    # Combine and get unique dates
    dates = list(set(post_dates + podcast_dates + event_dates))

    for d in dates:
        date_str = d.isoformat()  # Convert date to string in YYYY-MM-DD format
        interactions['date'][date_str]=d
    for i in genDateRange(start[0],end[0],start[1],end[1],start[2],end[2]):
        interactions['labels']+=[i]
        if i not in interactions['date']:
            interactions['posts'].append(0)
            interactions['events'].append(0)
            interactions['podcasts'].append(0)
        else :
            interactions['posts']+=([lsum([post.likes.count() for post in (post_filter(posts,interactions['date'][i]))])])
            interactions['events']+=([lsum([event.likes.count() for event in (event_filter(events,interactions['date'][i]))])])
            interactions['podcasts']+=([lsum([podcast.likes.count() for podcast in (podcast_filter(podcasts,interactions['date'][i]))])])
    return interactions

def comments(user_id,start=(2025,4,26),end=(2025,5,14)):
    comments = {'date':{},'labels':[],'posts':[],'podcasts':[]}
    posts = load_data(Post, exists_field='user_id', exists_value=user_id)
    podcasts = load_data(Podcast, exists_field='user_id', exists_value=user_id)
    
    # Extract dates from posts and podcasts with comments
    post_dates = [post.timestamp.date() if hasattr(post.timestamp, 'date') else post.timestamp 
                 for post in posts if post.comments.count() > 0]
    podcast_dates = [podcast.time.date() if hasattr(podcast.time, 'date') else podcast.time 
                    for podcast in podcasts if podcast.comments.count() > 0]
    
    # Combine and get unique dates
    dates = list(set(post_dates + podcast_dates))
    
    for d in dates:
        date_str = d.isoformat()  # Convert date to string in YYYY-MM-DD format
        comments['date'][date_str]=d
    for i in genDateRange(start[0],end[0],start[1],end[1],start[2],end[2]):
        comments['labels']+=[i]
        if i not in comments['date']:
            comments['posts'].append(0)
            comments['podcasts'].append(0)
        else :
            comments['posts']+=([lsum([post.comments.count() for post in (post_filter(posts,comments['date'][i]))])])
            comments['podcasts']+=([lsum([podcast.comments.count() for podcast in (podcast_filter(podcasts,comments['date'][i]))])])
    return comments
    '''for d in dates:
        date_str = d.isoformat()
        comments[date_str] = {
            'posts': len([post.comments.count() for post in posts 
                     if ((post.timestamp.date() if hasattr(post.timestamp, 'date') else post.timestamp) == d) 
                     and (post.comments.count() > 0)]),
            'podcasts': len([podcast.comments.count() for podcast in podcasts 
                        if ((podcast.time.date() if hasattr(podcast.time, 'date') else podcast.time) == d) 
                        and (podcast.comments.count() > 0)])
        }
    return comments'''
def earning(self,user_id):
    user = load_data(User, filter=(User.id == user_id), limit=1)[0]
    posts = user.posts
    podcasts = user.podcasts
    events = user.events
    adminship = user.group_admins
if __name__=='__main__':
    contents(1)
    interactions(1)
    comments(1)
    