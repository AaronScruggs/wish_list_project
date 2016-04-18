from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from datetime import datetime
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from wish_list_items.models import ShippingAddress, WishList, WishItem


class UserTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="Tester",
                                             email="test@gmail.com",
                                             password="pass_word")

        self.url = reverse("list_users")

    def test_create_user(self):
        data = {"username": "Tester2", "password": "pass_word",
                "email": "test@gmail"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_retrieve_user(self):
        response = self.client.get(self.url,{"pk": self.user.id},
                                   format="json")
        self.assertEqual(response.data[0]['username'], self.user.username)


class ShippingAdressTest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(username="Tester",
                                             email="test@gmail.com",
                                             password="pass_word")

        self.user2 = User.objects.create_user(username="tester2",
                                              password="pass_word")

        self.address1 = ShippingAddress.objects.create(address="122 LVB",
                                                       city="Las Vegas",
                                                       state="NV",
                                                       zip_code="89122",
                                                       user=self.user)
        self.url = reverse("list_address")

    def test_shipping_address_create(self):
        """
        Running this test with self.user throws a unique contraint error.
        """
        token = Token.objects.get(user_id=self.user2.id)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        data = {"address": "123 LVB", "city": "Las Vegas", "state": "NV",
                "zip_code": "89111", "user": self.user2.id}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ShippingAddress.objects.count(), 2)

    def test_retrieve_address(self):
        response = self.client.get(self.url, {"pk": self.address1.id},
                                   format="json")
        self.assertEqual(response.data[0]["address"], self.address1.address)


class WishListTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="Tester",
                                             email="test@gmail.com",
                                             password="pass_word")
        self.wish_list = WishList.objects.create(title="Christmas",
                                                 deadline=datetime.now(),
                                                 user=self.user)

        self.url = reverse("list_wish_lists")

    def test_wish_list_create(self):
        token = Token.objects.get(user_id=self.user.id)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        data = {"title": "test title", "deadline": "2016-01-01",
                "user": self.user.id}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WishList.objects.count(), 2)

    def test_retrieve_wish_list(self):
        response = self.client.get(self.url, {"pk": self.wish_list.id},
                                   format="json")
        self.assertEqual(response.data[0]["title"], self.wish_list.title)

    def test_wish_list_expired(self):
        self.assertTrue(self.wish_list.expired)


class WishItemTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="Tester",
                                             email="test@gmail.com",
                                             password="pass_word")

        self.wish_list = WishList.objects.create(title="Christmas",
                                                 deadline=datetime.now(),
                                                 user=self.user)

        self.wish_item = WishItem.objects.create(title="test item",
                                                 price=200,
                                                 wish_list=self.wish_list)

        self.url = reverse("list_wish_items")

    def test_wish_item_create(self):
        token = Token.objects.get(user_id=self.user.id)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        data = {"title": "test title", "price": 300,
                "wish_list": self.wish_list.id}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WishItem.objects.count(), 2)
