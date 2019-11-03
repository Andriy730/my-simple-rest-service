from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework import generics
from django.http import Http404
from django.contrib.auth.models import User

from .serializers import AdvertisementSerializer, UserSerializer
from .models import Advertisement, Tag
from .permissions import IsOwnerOrReadOnly, IsTheSameUserOrReadOnly


class AdvertisementsView(APIView):
    """List all advertisements"""

    def get(self, request):
        advertisements = Advertisement.objects.all()
        serializer = AdvertisementSerializer(advertisements, many=True)
        return Response({"advertisements": serializer.data})


class AdvertisementCreatView(APIView):
    """Create a new advertisement"""
    permission_classes = [permissions.IsAuthenticated,
     IsOwnerOrReadOnly]

    def post(self, request):
        serializer = AdvertisementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UsersAdvetisementsView(generics.ListAPIView):
    """List all advertisements for authenticated user"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        return Advertisement.objects.filter(owner=self.request.user)


class AdvertisementView(APIView):
    """Retrieve, update or delete advertisement instance"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
    IsOwnerOrReadOnly]

    def get_object(self, id):
        try:
            return Advertisement.objects.get(id=id)
        except Advertisement.DoesNotExist:
            raise Http404

    def get(self, request, id):
        advert = self.get_object(id)
        serializer = AdvertisementSerializer(advert)
        return Response(serializer.data)

    def put(self, request, id):
        advert = self.get_object(id)
        serializer = AdvertisementSerializer(advert, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        advert = self.get_object(id)
        advert.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AdvertisementsByTagsView(generics.ListAPIView):
    """List all advertisements that have given tags"""
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        queryset = Advertisement.objects.all()
        tags = self.request.query_params.get('tags').split(',')
        for tag in tags:
            try:
                tag = '#' + tag.strip()
                tag_id = Tag.objects.get(name=tag).id
                queryset = queryset.filter(tags__in=[tag_id])
            except Tag.DoesNotExist:
                return Advertisement.objects.none()
        return queryset

class RegisterView(APIView):
    """Register new User"""

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    """Retrieve, update or delete user instance"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
    IsTheSameUserOrReadOnly]

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, username):
        user = self.get_object(username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, username):
        user = self.get_object(username)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        user = self.get_object(username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
