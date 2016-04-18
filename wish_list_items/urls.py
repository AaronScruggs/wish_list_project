from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token

from wish_list_items.views import UserListCreate, UserDetail, WishListCreateList,\
    WishListDetailUpdateDelete, WishItemCreateList, WishItemDetailUpdateDelete,\
    PledgeCreateList, PledgeDetailUpdateDelete, TestPage,\
    ShippingAddressListCreate, ShippingAddressDetailUpdateDelete

urlpatterns = [
    url(r'^users/$', UserListCreate.as_view(), name="list_users"),
    url(r'^users/(?P<pk>\d+)/$', UserDetail.as_view(), name="detail_user"),
    url(r'^address/$', ShippingAddressListCreate.as_view(),
        name="list_address"),
    url(r'^address/(?P<pk>\d+)/$', ShippingAddressDetailUpdateDelete.as_view(),
        name="detail_address"),
    url(r'^wishlist/$', WishListCreateList.as_view(), name="list_wish_lists"),
    url(r'^wishlist/(?P<pk>\d+)/$', WishListDetailUpdateDelete.as_view(),
        name="detail_wish_list"),
    url(r'^wishitem/$', WishItemCreateList.as_view(), name="list_wish_items"),
    url(r'^wishitem/(?P<pk>\d+)/$', WishItemDetailUpdateDelete.as_view(),
        name="detail_wish_item"),
    url(r'^pledge/$', PledgeCreateList.as_view(), name="list_pledges"),
    url(r'^pledge/(?P<pk>\d+)/$', PledgeDetailUpdateDelete.as_view(),
        name="detail_pledges"),
    url(r'api-token-auth/$', obtain_auth_token),
    url(r'^test/$', TestPage.as_view(), name="test"),
    url(r'^stripesubmit/$', PledgeCreateList.as_view(), name="test_submit"),

]
