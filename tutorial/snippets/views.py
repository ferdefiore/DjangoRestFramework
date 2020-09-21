from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..snippets.models import Snippet
from ..snippets.serializers import SnippetSerializer


# REST framework provides two wrappers you can use to write API views.
#
# The @api_view decorator for working with function based views.
# The APIView class for working with class-based views.
# These wrappers provide a few bits of functionality such as making sure you receive Request
# instances in your view, and adding context to Response objects so that content negotiation can be performed.
#
# The wrappers also provide behaviour such as returning 405 Method Not Allowed responses when appropriate,
# and handling any ParseError exceptions that occur when accessing request.data with malformed input.

@api_view(['GET', 'POST'])
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
