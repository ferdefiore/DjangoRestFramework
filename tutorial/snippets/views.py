from rest_framework import generics
from rest_framework import mixins

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


# Using mixins
# One of the big wins of using class-based views is that it allows us to easily compose reusable bits of behaviour.
# The create/retrieve/update/delete operations that we've been using so far are going to be pretty similar for any
# model-backed API views we create. Those bits of common behaviour are implemented in REST framework's mixin classes.
# Let's take a look at how we can compose the views by using the mixin classes. Here's our views.py module again.
# We'll take a moment to examine exactly what's happening here. We're building our view using GenericAPIView,
# and adding in ListModelMixin and CreateModelMixin.
#
# The base class provides the core functionality, and the mixin classes provide the .list() and .create() actions.
# We're then explicitly binding the get and post methods to the appropriate actions. Simple enough stuff so far.
# Pretty similar. Again we're using the GenericAPIView class to provide the core functionality,
# and adding in mixins to provide the .retrieve(), .update() and .destroy() actions.

class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
