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

    # this is to show user data
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
    user = UserSerializer(read_only=True)

    class Meta:
        model = Pledge
        fields = ("user", "amount")

    def create(self, validated_data):

        stripe.api_key = 'sk_test_0Qpguvhry6396ZdPSX8Y12Sd'
        amount = int(validated_data["amount"]) * 100
        token = self._kwargs['data']['stripeToken']
        user = User.objects.get(pk=self._kwargs['data']['user_id'])
        wish_item = WishItem.objects.get(pk=self._kwargs['data']['item_id'])

        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token,
                description="test charge"
            )
            return Pledge.objects.create(amount=amount, charge_id=charge["id"],
                                         user=user, wish_item=wish_item)

        except stripe.error.CardError as e:
            pass


"""
fields cover both input and output.
Model serializer populates fields with that model's fields.
read_only means that it is not required. Just for display.


# this is to show user data
# make it read only because you will have the user in the view request from
a token.
user = UserSerializer(read_only=True)


Can not create a pledge on a pledge end point.
Have a standard Pledge serializer and then a separate serializer.

Check that WishItem actually saves a WishList!

Don't put variables into fields that we do not want to use or display.
No reason to show extra information.


"""

# # In View
# class DetailPledge(generics.RetrieveAPIView):
#     queryset = Pledge.objecs.all()
#     serializer_class = PledgeSerializer

# class ListPledge(generics.ListAPIView):
#     queryset = Pledge.objects.all()
#     serializer_class = PledgeSerializer

# Don't forget to add urls.
#
# class ChargeSerializer(serializers.Serializer):
#     token = serializers.CharField(max_length=128)
#     user_id = serializers.IntegerField()  # Not needed?
#     item_id = serializers.IntegerField()
#     amount = serializers.IntegerField()
#
#     def create(self, validated_data):
#         stripe.api_key = 'sk_test_0Qpguvhry6396ZdPSX8Y12Sd'
#         amount = validated_data["amount"]
#
#         token = validated_data['stripeToken']
#         user = validated_data['user']
#         wish_item = validated_data['item_id']
#
#         # fake charge from class
#         #charge_id = "fake data"
#
#         try:
#             charge = stripe.Charge.create(
#                 amount=amount * 100,
#                 currency="usd",
#                 source=token,
#                 description="test charge"
#             )
#             pledge = Pledge.objects.create(amount=amount, charge_id=charge['id'],
#                                          user=user, wish_item=wish_item)
#             return pledge
#
#         except:
#             pass
#

# View
# class CreateCharge(APIView):
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#
#     def post(self, request, format=None):
#         serializer = ChargeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(None, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# Add url


"""
Post to charges {chirp_id, amount, charge_token}
"""

# Use django.request logging