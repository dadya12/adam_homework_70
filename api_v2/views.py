import json

from django.shortcuts import get_object_or_404
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from webapp.models import Article
from api_v2.serializers import ArticleSerializer, ArticleModelSerializer


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed(['GET'])


def json_echo_view(request, *args, **kwargs):
    answer = {
        'message': 'Hello World!',
        'method': request.method
    }
    if request.body:
        answer['content'] = json.loads(request.body)
    return JsonResponse(answer)


class ArticleView(APIView):

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk:
            article = get_object_or_404(Article, pk=pk)
            serializer = ArticleModelSerializer(article)
            return Response(serializer.data)
        articles = Article.objects.order_by('-created_at')
        articles_list = ArticleModelSerializer(articles, many=True).data
        return Response(articles_list)

    def post(self, request, *args, **kwargs):
        serializer = ArticleModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)
        if pk:
            serializer = ArticleModelSerializer(article, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            serializer = ArticleModelSerializer(article, data=request.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)
        if pk:
            article.delete()
            return Response({'deleted_id': pk})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)