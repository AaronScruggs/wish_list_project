from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from datetime import datetime

from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class WishList(models.Model):

    title = models.CharField(max_length=255)
    deadline = models.DateField()

    # Turn to false rather than delete
    active = models.BooleanField(default=True)

    user = models.ForeignKey(User, related_name="lists")

    created_time = models.DateTimeField(auto_now_add=True)

    @property
    def expired(self):
        # Added to avoid naive vs aware date comparison.
        end_date = datetime.combine(self.deadline, datetime.min.time())
        return datetime.now() > end_date

    def __str__(self):
        return self.title


class WishItem(models.Model):

    title = models.CharField(max_length=255)
    price = models.IntegerField()

    image = models.ImageField(upload_to="wishlist_images/",
                              null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    item_link = models.URLField(null=True, blank=True)

    visible = models.BooleanField(default=True)
    item_url = models.URLField(null=True, blank=True)

    wish_list = models.ForeignKey(WishList, related_name="items")

    @property
    def pledged_amount(self):
        total_pledges = self.pledges.aggregate(Sum("amount"))
        if total_pledges['amount__sum']:
            return total_pledges['amount__sum']
        else:
            return 0

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
    charge_id = models.CharField(max_length=128)

    user = models.ForeignKey(User, related_name="pledges")
    wish_item = models.ForeignKey(WishItem, related_name="pledges")

    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} pledged on {}".format(self.amount, self.wish_item)


class ShippingAddress(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)

    # might change to ForeignKey
    user = models.OneToOneField(User)

    def __str__(self):
        return self.address
