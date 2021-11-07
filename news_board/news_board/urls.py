from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

from rest_framework import routers

from posts.views import PostViewSet, PostUpvoteView
from comments.views import CommentViewSet


router = routers.DefaultRouter()

router.register(r"posts", PostViewSet)
router.register(r"comments", CommentViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("upvote/", PostUpvoteView.as_view()),
    url(r"^api/", include((router.urls, "api"), namespace="api")),
]
