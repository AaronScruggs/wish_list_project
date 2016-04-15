from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from wish_list_items.permissions import IsOwnerOrReadOnly
from django.core.urlresolvers import reverse, reverse_lazy

from wish_list_items.models import WishList, WishItem, Pledge
from wish_list_items.serializers import UserSerializer, WishListSerializer,\
    WishItemSerializer, PledgeSerializer
from django.http import HttpResponseBadRequest
from django.conf import settings
from wish_list_items.serializers import UserSerializer

import stripe


class UserList(generics.ListCreateAPIView):
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


def pledge_payment(request):

    stripe.api_key = settings.STRIPE_SECRET_KEY

    token = request.POST['stripeToken']
    amount = request.POST['amount'] * 100

    try:
        charge = stripe.Charge.create(
            amount=amount,  # amount in cents, again
            currency="usd",
            source=token,
            description="Wish Item Pledge"
        )
    except stripe.error.CardError as e:
        # The card has been declined
        # False, e ?
        return HttpResponseBadRequest()

    return HttpResponseRedirect(reverse('/'))



class RegisterUser(CreateView):

    model = User
    form_class = UserCreationForm
    #template_name = "registration/register.html"
    success_url = reverse_lazy("/")


