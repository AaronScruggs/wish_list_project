from django.contrib.auth.models import User
from django.views.generic import ListView
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response

from wish_list_items.models import WishList, WishItem, Pledge, ShippingAddress
from wish_list_items.permissions import IsOwnerOrReadOnly
from wish_list_items.serializers import UserSerializer, ChargeSerializer
from wish_list_items.serializers import WishListSerializer,\
    WishItemSerializer, PledgeSerializer, ShippingAddressSerializer


class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ShippingAddressListCreate(generics.ListCreateAPIView):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ShippingAddressDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class WishListAll(generics.ListAPIView):
    """
    An unfiltered display of all wishlists.
    """
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer


class WishListCreateList(generics.ListCreateAPIView):

    serializer_class = WishListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return WishList.objects.filter(
            user=self.request.user).order_by("created_time")


class WishListDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    # override get queryset, filter on request.user
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class WishItemCreateList(generics.ListCreateAPIView):
    queryset = WishItem.objects.all()
    serializer_class = WishItemSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        list_id = self.request.data['wish_list']
        serializer.save(wish_list=WishList.objects.get(pk=list_id))


class WishItemDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = WishItem.objects.all()
    serializer_class = WishItemSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class PledgeList(generics.ListAPIView):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer


class PledgeDetail(generics.RetrieveAPIView):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer


class ChargeCreate(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, format=None):
        serializer = ChargeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(None, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestPage(ListView):
    """
    This is a page used for testing stripe payments locally. Not for live site.
    """
    template_name = "wish_list_items/stripe_test.html"
    context_object_name = "items"
    queryset = WishList.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = 1
        context['item'] = 3
        context['amount'] = 99
        return context
