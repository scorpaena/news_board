from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .serializers import PostSerializer, PostUpvoteSerializer
from .models import Post, PostUpvote


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PostUpvoteView(generics.CreateAPIView):
    queryset = PostUpvote.objects.all()
    serializer_class = PostUpvoteSerializer
    permission_classes = [IsAuthenticated]
