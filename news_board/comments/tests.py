from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

from posts.models import Post
from .models import Comment

User = get_user_model()


class CommentTestCase(TestCase):
    maxDiff = None

    def setUp(self):
        self.client = APIClient()
        self.client_anonymous = APIClient()

        self.user = User.objects.create_user(
            email="foo@bar.com",
            username="foo",
            password="Bar123$%",
        )

        self.client.login(username="foo", password="Bar123$%")

        self.payload_post = {
            "title": "foo",
            "link": "https://example.com",
            "author": self.user,
        }
        self.post = Post.objects.create(**self.payload_post)

        self.payload_comment = {
            "post": self.post,
            "content": "first",
            "author": self.user,
        }
        self.comment = Comment.objects.create(**self.payload_comment)

    def test_comment_get(self):
        response = self.client.get("/api/comments/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_comment_get_anonymous(self):
        response = self.client_anonymous.get("/api/comments/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_comment_create(self):
        request = self.client.post(
            "/api/comments/",
            data={
                "post": self.post.id,
                "content": "second",
            },
        )
        comment = Comment.objects.last()
        self.assertEqual(request.status_code, 201)
        self.assertEqual(comment.content, "second")

    def test_comment_create_anonymous(self):
        request = self.client_anonymous.post(
            "/api/comments/",
            data={
                "post": self.post.id,
                "content": "foo content",
            },
        )
        self.assertEqual(request.status_code, 403)

    def test_comment_update(self):
        request = self.client.patch(
            f"/api/comments/{self.comment.id}/",
            data={
                "content": "first updated",
            },
        )
        comment = Comment.objects.first()
        self.assertEqual(request.status_code, 200)
        self.assertEqual(comment.content, "first updated")

    def test_comment_update_anonymous(self):
        request = self.client_anonymous.patch(
            f"/api/comments/{self.comment.id}/", data={"content": "first updated"}
        )
        self.assertEqual(request.status_code, 403)
