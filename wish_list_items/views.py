from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, \
    IsAuthenticated
from wish_list_items.permissions import IsOwnerOrReadOnly
from django.core.urlresolvers import reverse, reverse_lazy

from wish_list_items.models import WishList, WishItem, Pledge, ShippingAddress
from wish_list_items.serializers import UserSerializer, WishListSerializer,\
    WishItemSerializer, PledgeSerializer, ShippingAddressSerializer
from django.http import HttpResponseBadRequest
from django.conf import settings
from wish_list_items.serializers import UserSerializer
from django.views.generic import ListView
import stripe


class UserList(generics.ListCreateAPIView):
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
    #permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        # serializer.save(wish_item=self.request.wish_item)
        # serializer.save(user=self.request.user)

        # Assigning them drectly for local testing!
        serializer.save(wish_item=WishItem.objects.first())
        serializer.save(user=User.objects.first())  # change from default
        # foo='bar'


class PledgeDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class TestPage(ListView):
    template_name = "wish_list_items/stripe_test.html"
    context_object_name = "items"
    queryset = WishList.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = 1
        context['item'] = 1
        return context

#
# def stripe_test(request):
#
#     foo = 'bar'
#
#     token = request.POST["stripeToken"]
#
#     stripe.api_key = 'sk_test_0Qpguvhry6396ZdPSX8Y12Sd'
#
#     #amount = int(float(request.POST['amount']) * 100)
#
#     try:
#         charge = stripe.Charge.create(
#             amount=1000,  # amount in cents, again
#             currency="usd",
#             source=token,
#             description="Donation to chirp"
#         )
#     except stripe.error.CardError as e:
#         # The card has been declined
#         pass
#
#     return HttpResponseRedirect(reverse('list_users'))
