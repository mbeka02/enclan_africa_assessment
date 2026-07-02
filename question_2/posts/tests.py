from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class PostAPITests(APITestCase):
    """Test suite for the blog posts CRUD API."""

    def setUp(self):
        # Create two users with auth tokens
        self.user1 = User.objects.create_user(username="alice", password="pass1234")
        self.user2 = User.objects.create_user(username="bob", password="pass1234")
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)
        self.post_data = {"title": "Test Post", "content": "Hello, world!"}

    def auth(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def clear_auth(self):
        self.client.credentials()

    # -- Create --

    def test_create_post_authenticated(self):
        self.auth(self.token1)
        resp = self.client.post("/api/posts/", self.post_data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data["title"], "Test Post")
        self.assertEqual(resp.data["author"], "alice")

    def test_create_post_unauthenticated(self):
        resp = self.client.post("/api/posts/", self.post_data)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # -- Read --

    def test_list_posts_unauthenticated(self):
        """Unauthenticated users can list posts."""
        self.auth(self.token1)
        self.client.post("/api/posts/", self.post_data)
        self.clear_auth()
        resp = self.client.get("/api/posts/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)

    def test_retrieve_post(self):
        self.auth(self.token1)
        create_resp = self.client.post("/api/posts/", self.post_data)
        self.clear_auth()
        resp = self.client.get(f"/api/posts/{create_resp.data['id']}/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["title"], "Test Post")

    # -- Update --

    def test_update_own_post(self):
        self.auth(self.token1)
        create_resp = self.client.post("/api/posts/", self.post_data)
        resp = self.client.put(
            f"/api/posts/{create_resp.data['id']}/",
            {"title": "Updated", "content": "New content"},
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["title"], "Updated")

    def test_update_other_users_post(self):
        """A user cannot edit another user's post."""
        self.auth(self.token1)
        create_resp = self.client.post("/api/posts/", self.post_data)
        self.auth(self.token2)
        resp = self.client.put(
            f"/api/posts/{create_resp.data['id']}/",
            {"title": "Hacked", "content": "Nope"},
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    # -- Delete --

    def test_delete_own_post(self):
        self.auth(self.token1)
        create_resp = self.client.post("/api/posts/", self.post_data)
        resp = self.client.delete(f"/api/posts/{create_resp.data['id']}/")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_other_users_post(self):
        """A user cannot delete another user's post."""
        self.auth(self.token1)
        create_resp = self.client.post("/api/posts/", self.post_data)
        self.auth(self.token2)
        resp = self.client.delete(f"/api/posts/{create_resp.data['id']}/")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    # -- Token endpoint --

    def test_obtain_token(self):
        resp = self.client.post(
            "/api/token/", {"username": "alice", "password": "pass1234"}
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("token", resp.data)
