from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import User
from .serializers import UserSerializer

class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def user_list(request):
    if request.method == 'GET':
        paginator = UserPagination()
        users = User.objects.all()
        result_page = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
