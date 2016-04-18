from django.contrib import admin

from wish_list_items.models import WishList, WishItem, Pledge


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "deadline")


@admin.register(WishItem)
class WishItemAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "image", "visible", "item_url",
                    "wish_list")


@admin.register(Pledge)
class PledgeAdmin(admin.ModelAdmin):
    list_display = ("amount", "user", "wish_item")



