from django.contrib.auth.models import User
from rest_framework import serializers

from wish_list_items.models import WishList, WishItem, Pledge


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


class PledgeCreationSerializer(serializers.Serializer):
    pass








class PledgeSerializer(serializers.ModelSerializer):
    wish_item = WishItemSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Pledge
        fields = "__all__"




