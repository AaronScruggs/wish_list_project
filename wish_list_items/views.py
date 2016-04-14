from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from wish_list_items.permissions import IsOwnerOrReadOnly

from wish_list_items.models import WishList, WishItem, Pledge
from wish_list_items.serializers import UserSerializer, WishListSerializer,\
    WishItemSerializer, PledgeSerializer

from wish_list_items.serializers import UserSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class WishListCreateList(generics.ListCreateAPIView):
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WishListDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class WishItemCreateList(generics.ListCreateAPIView):
    queryset = WishItem.objects.all()
    serializer_class = WishItemSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(wish_list=self.request.wish_list)


class WishItemDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = WishItem.objects.all()
    serializer_class = WishItemSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class PledgeCreateList(generics.ListCreateAPIView):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(wish_item=self.request.wish_item)
        serializer.save(user=self.request.user)


class PledgeDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer
    permission_classes = (IsOwnerOrReadOnly,)

