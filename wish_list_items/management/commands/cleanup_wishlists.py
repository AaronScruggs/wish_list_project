import stripe
from django.core.management import BaseCommand
from django.utils import timezone

from wish_list_items.models import WishList


def item_refund(item):
    """
    Only use for items that are not fully funded.
    Refund all pledges on an item.
    """
    for pledge in item.pledges:
        refund = stripe.Refund.create(
            charge=pledge.charge_id
        )


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

            for item in old_list.items:
                if not item.fully_funded:
                    item_refund(item)
