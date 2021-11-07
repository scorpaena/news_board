from news_board.celery_config import app
from .models import PostUpvote


@app.task
def reset_post_upvotes():
    PostUpvote.objects.all().delete()
