from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from snippets.models import Snippet
from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer
from snippets.serializers import UserSerializer


# Next we're going to replace the SnippetList, SnippetDetail and SnippetHighlight view classes.
# We can remove the three views, and again replace them with a single class.
# This time we've used the ModelViewSet class in order to get the complete set of default read and write operations.
#
# Notice that we've also used the @action decorator to create a custom action, named highlight.
# This decorator can be used to add any custom endpoints that don't fit into the standard create/update/delete style.
# Custom actions which use the @action decorator will respond to GET requests by default.
# We can use the methods argument if we wanted an action that responded to POST requests.
#
# The URLs for custom actions by default depend on the method name itself.
# If you want to change the way url should be constructed, you can include url_path as a decorator keyword argument.
class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# Here we've used the ReadOnlyModelViewSet class to automatically provide the default 'read-only' operations.
# We're still setting the queryset and serializer_class attributes exactly as we did when we were using regular views,
# but we no longer need to provide the same information to two separate classes.
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })
