import stripe
from django.conf import settings
from django.core.management import BaseCommand
from django.utils import timezone

from wish_list_items.models import WishList


def item_refund(item):
    """
    Only use for items that are not fully funded.
    Refund all pledges on an item.
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY
    for pledge in item.pledges.all():
        try:
            refund = stripe.Refund.create(
                charge=pledge.charge_id
            )

        except stripe.error.InvalidRequestError as e:
            pass

        pledge.amount = 0
        pledge.save()


class Command(BaseCommand):
    """
    expiring_lists is a queryset of all lists that are active but have passed
    their deadline. These lists are deactivated and refunds are issued for
    all pledges on items that are not fully funded.
    """

    def handle(self, *args, **options):

        now = timezone.now().date()

        expiring_lists = WishList.objects.filter(active=True).\
            filter(deadline__lte=now)

        for old_list in expiring_lists:
            old_list.active = False
            old_list.save()

            for item in old_list.items.all():
                if not item.fully_funded:
                    item_refund(item)
