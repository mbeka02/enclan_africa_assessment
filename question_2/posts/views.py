from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """CRUD viewset for blog posts.

    - List/Retrieve: open to everyone (including unauthenticated users).
    - Create: requires authentication.
    - Update/Delete: restricted to the post's author.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # IsAuthenticatedOrReadOnly: blocks unauthenticated writes
    # IsAuthorOrReadOnly: restricts edits/deletes to the post's author
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        # Attach the logged-in user as the post's author
        serializer.save(author=self.request.user)
