import stripe
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from rest_framework import serializers

from wish_list_items.models import WishList, WishItem, Pledge, ShippingAddress


class UserSerializer(serializers.ModelSerializer):
    lists = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    pledges = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "pledges", "lists", "password")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ShippingAddressSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ShippingAddress
        fields = "__all__"


class WishListSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    user = UserSerializer(read_only=True)

    class Meta:
        model = WishList
        fields = "__all__"


class WishItemSerializer(serializers.ModelSerializer):
    wish_list = WishListSerializer(read_only=True)
    pledges = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = WishItem
        fields = "__all__"


class PledgeSerializer(serializers.ModelSerializer):
    wish_item = WishItemSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    amount = serializers.IntegerField()
    charge_id = serializers.CharField(max_length=64)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = Pledge
        fields = "__all__"

    def create(self, validated_data):
        stripe.api_key = 'sk_test_0Qpguvhry6396ZdPSX8Y12Sd'
        amount = validated_data["amount"] * 100

        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=validated_data["token"],
                description="test charge"
            )
            return Pledge.objects.create(amount=amount, charge_id=charge["id"])

        except stripe.error.CardError as e:
            pass

