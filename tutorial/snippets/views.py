from rest_framework import generics

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


# Using the mixin classes we've rewritten the views to use slightly less code than before,
# but we can go one step further. REST framework provides a set of already mixed-in generic views
# that we can use to trim down our views.py module even more.
class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
