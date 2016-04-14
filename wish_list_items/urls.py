from django.conf.urls import url

from wish_list_items.views import UserList, UserDetail, WishListCreateList,\
    WishListDetailUpdateDelete, WishItemCreateList, WishItemDetailUpdateDelete,\
    PledgeCreateList, PledgeDetailUpdateDelete

urlpatterns = [
    url(r'^users/$', UserList.as_view(), name="list_users"),
    url(r'^users/(?P<pk>\d+)/$', UserDetail.as_view(), name="detail_user"),
    url(r'^wishlist/$', WishListCreateList.as_view(), name="list_wish_lists"),
    url(r'^wishlist/(?P<pk>\d+)/$', WishListDetailUpdateDelete.as_view(), name="detail_wish_list"),
    url(r'^wishitem/$', WishItemCreateList.as_view(), name="list_wish_items"),
    url(r'^wishitem/(?P<pk>\d+)/$', WishItemDetailUpdateDelete.as_view(), name="detail_wish_item"),
    url(r'^pledge/$', PledgeCreateList.as_view(), name="list_pledges"),
    url(r'^pledge/(?P<pk>\d+)/$', PledgeDetailUpdateDelete.as_view(), name="detail_pledges"),
]
