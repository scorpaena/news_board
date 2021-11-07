from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_psq import PsqMixin, Rule

from .serializers import CommentSerializer, CommentDetailSerializer
from .models import Comment
from .permissions import IsOwnerOrReadOnly


class CommentViewSet(PsqMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    psq_rules = {
        ("update", "partial_update", "destroy"): [
            Rule([IsOwnerOrReadOnly], CommentDetailSerializer)
        ]
    }
