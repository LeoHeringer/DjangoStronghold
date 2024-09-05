import logging
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import User
from .serializers import UserSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

logger = logging.getLogger(__name__)

class UserPagination(PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'page_size'
    max_page_size = 100

pagination_param = [
    openapi.Parameter('page', openapi.IN_QUERY, description="Número da página", type=openapi.TYPE_INTEGER),
    openapi.Parameter('page_size', openapi.IN_QUERY, description="Tamanho da página", type=openapi.TYPE_INTEGER),
]

@swagger_auto_schema(method='get', manual_parameters=pagination_param, responses={200: UserSerializer(many=True)})
@swagger_auto_schema(method='post', request_body=UserSerializer, responses={201: UserSerializer})
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
        except IntegrityError as e:
            logger.error(f"Integrity error: {e}")
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            return Response({"error": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@swagger_auto_schema(method='get', responses={200: UserSerializer})
@swagger_auto_schema(method='delete', responses={204: 'No Content', 404: 'Not Found'})
@api_view(['GET', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        logger.warning(f"User with id {pk} not found.")
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        user.delete()
        logger.info(f"User with id {pk} deleted.")
        return Response(status=status.HTTP_204_NO_CONTENT)
