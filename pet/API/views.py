from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions

from .models import *
from .serializers import *


class UserMe(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(status=status.HTTP_200_OK, data={'id': user.id,
                                                         'email': user.email,
                                                         'is_superuser': user.is_superuser})


class FilmAll(viewsets.ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy', 'create']:
            return [permissions.IsAdminUser()]
        if self.action in ['list']:
            return [permissions.AllowAny()]


class ReviewAll(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy', 'create']:
            return [permissions.IsAuthenticated()]
        if self.action in ['list']:
            return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
