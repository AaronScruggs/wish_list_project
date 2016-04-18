from django.contrib.auth.models import User
from django.views.generic import ListView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from wish_list_items.models import WishList, WishItem, Pledge, ShippingAddress
from wish_list_items.permissions import IsOwnerOrReadOnly
from wish_list_items.serializers import UserSerializer
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


class WishListCreateList(generics.ListCreateAPIView):
    queryset = WishList.objects.order_by("-created_time")
    serializer_class = WishListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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


class PledgeCreateList(generics.ListCreateAPIView):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer
    #permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):

        # serializer.save(user=self.request.user) would be better. I am
        # not sure why it throws an error.

        serializer.save(user=self.request.user)


class PledgeDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer
    permission_classes = (IsOwnerOrReadOnly,)


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
