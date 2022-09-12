from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from api.models import Template
from api.permissions import IsAuthorizedUser
from api.serializers import TemplatesSerializer


class HomeView(TemplateView):
    template_name = 'index.html'


@api_view(['GET', 'PUT', 'POST'])
@permission_classes([IsAuthorizedUser])
def templates_list(request):
    if request.method == 'GET':
        templates = Template.objects.all()
        serializer = TemplatesSerializer(templates, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        request.data['is_directory'] = False
        request.data['file_name'] = request.data.get('title')
        request.data['file_content'] = request.data.get('content')
        serializer = TemplatesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        serializer = TemplatesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthorizedUser])
def templates_detail(request, id):

    try:
        templates = Template.objects.get(id=id)
    except Template.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TemplatesSerializer(templates)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TemplatesSerializer(templates, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        templates.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
