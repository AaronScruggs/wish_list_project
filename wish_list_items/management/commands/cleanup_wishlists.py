from django.core.management import BaseCommand
from django.utils import timezone

from wish_list_items.models import WishList


class Command(BaseCommand):

    def handle(self, *args, **options):

        now = timezone.now().date()
        # only bring in expired and active objects.
        WishList.objects.filter(active=True).filter(deadline__lte=now).update(active=False)

        # for wish_list in wish_lists:
        #     if wish_list.expired:
        #         wish_list.active = False
        #         wish_list.save()
        #         # Add Stripe refund for all items here!
        #         # Probably create a helper function for that and call
        #         # it in one line.
