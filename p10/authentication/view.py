from typing import Any

from django.db.models.query import QuerySet
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response

from authentication.models import User
from authentication.serializers import UserSerializer


class UserAPIView(APIView):

    def get(self, *args: Any, **kwargs: Any):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserViewset(ReadOnlyModelViewSet[User]):

    serializer_class = UserSerializer

    # def get_queryset(self) -> QuerySet[User, User]:
    #     return User.objects.all()

    def get_queryset(self) -> QuerySet[User, User]:
        queryset = User.objects.filter(is_active=True)
        username = self.request.GET.get("username")
        if username is not None:
            queryset = queryset.filter(username=username)

        return queryset
