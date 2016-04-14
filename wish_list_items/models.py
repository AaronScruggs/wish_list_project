from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.utils import timezone


class WishList(models.Model):

    title = models.CharField(max_length=255)
    deadline = models.DateTimeField()
    active = models.BooleanField(default=True)

    user = models.ForeignKey(User, related_name="lists")

    created_time = models.DateTimeField(auto_now_add=True)

    @property
    def expired(self):
        return timezone.now() > self.deadline

    def __str__(self):
        return self.title


class WishItem(models.Model):

    title = models.CharField(max_length=255)
    price = models.IntegerField()
    image = models.ImageField(upload_to="wishlist_images/",
                              null=True, blank=True)

    visible = models.BooleanField(default=True)
    item_url = models.URLField()

    wish_list = models.ForeignKey(WishList, related_name="items")

    @property
    def pledged_amount(self):
        total_pledges = self.pledges.aggregate(Sum("amount"))
        return total_pledges['amount__sum']

    @property
    def remaining_amount(self):
        return self.price - self.pledged_amount

    @property
    def fully_funded(self):
        return self.pledged_amount >= self.price

    def __str__(self):
        return self.title


class Pledge(models.Model):

    amount = models.IntegerField()

    user = models.ForeignKey(User, related_name="pledges")
    wish_item = models.ForeignKey(WishItem, related_name="pledges")

    #payment_id = models.IntegerField()

    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} pledged on {}".format(self.amount, self.wish_item)


class ShippingAddress(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)

    def __str__(self):
        return self.address
