import stripe
from django.conf import settings
from django.contrib.auth.models import User
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


class WishItemSerializer(serializers.ModelSerializer):
    """
    wish_list is assigned in WishItemCreateList view.
    """
    user = UserSerializer(read_only=True)
    wish_list = serializers.PrimaryKeyRelatedField(read_only=True)
    pledges = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = WishItem
        fields = "__all__"


class WishListSerializer(serializers.ModelSerializer):

    items = WishItemSerializer(many=True, read_only=True)

    user = UserSerializer(read_only=True)

    class Meta:
        model = WishList
        fields = "__all__"


class ShippingAddressSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ShippingAddress
        fields = "__all__"




class PledgeSerializer(serializers.ModelSerializer):
    """
    For displaying Pledges.
    """

    user = UserSerializer(read_only=True)
    wish_item = WishItemSerializer(read_only=True)

    class Meta:
        model = Pledge
        fields = ("amount", "user", "wish_item")


class ChargeSerializer(serializers.Serializer):
    """
    Make a charge to stripe with a charge token. Create a pledge with that
    amount if charge is successful.
    """
    token = serializers.CharField(max_length=60)
    wish_id = serializers.IntegerField()
    amount = serializers.IntegerField()

    def create(self, validated_data):

        stripe.api_key = settings.STRIPE_SECRET_KEY
        amount = int(validated_data["amount"])
        token = validated_data['token']
        user = validated_data['user']
        wish_item = WishItem.objects.get(pk=validated_data['wish_id'])

        try:
            charge = stripe.Charge.create(
                amount=amount * 100,
                currency="usd",
                source=token,
                description="test charge"
            )
            return Pledge.objects.create(amount=amount, charge_id=charge["id"],
                                         user=user, wish_item=wish_item)

        except stripe.error.CardError as e:
            pass
