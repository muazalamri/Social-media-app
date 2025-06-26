from sqlalchemy import func
from model import Post
def rank():
    'function to rank posts or groups or also events and friend according to app algorism'

    return None
# Function to calculate ranking score
def calculate_ranking_score(post):
    # Example ranking function: likes + 2*comments + 3*shares - age_in_hours
    age_in_hours = (func.julianday(func.now()) - func.julianday(post.timestamp)) * 24
    return post.likes + 2 * post.comments + 3 * post.shares - age_in_hours

# Function to get top N posts according to ranking score
def get_top_posts(n):
    return Post.query.order_by(calculate_ranking_score(Post).desc()).limit(n).all()