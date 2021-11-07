from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

from .models import Post

User = get_user_model()


class PostTestCase(TestCase):
    maxDiff = None

    def setUp(self):
        self.client = APIClient()
        self.client_anonymous = APIClient()

        self.user = User.objects.create_user(
            email="foo@bar.com", username="foo", password="Bar123$%"
        )

        self.client.login(username="foo", password="Bar123$%")

        self.payload_post = {
            "title": "foo",
            "link": "https://example.com",
            "author": self.user,
        }
        self.post = Post.objects.create(**self.payload_post)

    def test_post_create(self):
        request = self.client.post(
            "/api/posts/",
            data={"title": "foo1", "link": "https://example1.com", "author": self.user},
        )
        self.assertEqual(request.status_code, 201)

    def test_post_create_anonymous(self):
        request = self.client_anonymous.post("/api/posts/", data=self.payload_post)
        self.assertEqual(request.status_code, 403)

    def test_post_get(self):
        response = self.client.get("/api/posts/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_post_get_anonymous(self):
        response = self.client_anonymous.get("/api/posts/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_post_detail_get(self):
        response = self.client.get(f"/api/posts/{self.post.id}/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "foo")

    def test_post_detail_get_anonymous(self):
        response = self.client_anonymous.get(f"/api/posts/{self.post.id}/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "foo")

    def test_post_detail_get_404(self):
        response = self.client.get(f"/api/posts/{self.post.id + 1}/", follow=True)
        self.assertEqual(response.status_code, 404)

    def test_post_detail_get_anonymous_404(self):
        response = self.client_anonymous.get(
            f"/api/posts/{self.post.id + 1}/", follow=True
        )
        self.assertEqual(response.status_code, 404)

    def test_post_upvote(self):
        request = self.client.post("/upvote/", data={"post": self.post.id})
        response = self.client.get(f"/api/posts/{self.post.id}/", follow=True)
        self.assertEqual(request.status_code, 201)
        self.assertEqual(response.data["upvotes_amount"], 1)

    def test_post_upvote_anonymous(self):
        request = self.client_anonymous.post("/upvote/", data={"post": self.post.id})
        response = self.client_anonymous.get(f"/api/posts/{self.post.id}/", follow=True)
        self.assertEqual(request.status_code, 403)
        self.assertEqual(response.data["upvotes_amount"], 0)
