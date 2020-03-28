from django.conf.urls import url, include
from django.contrib import admin

from django.contrib.auth import views as auth_views

from django.conf.urls.static import static
from django.conf import settings

from foodyapp import views, api

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),

    url(r'^restaurant/$', views.restaurant_home,
        name = 'restaurant-home'),

#Restaurant - Sign In & Out Fuction and Sign up
    url(r'^restaurant/sign-in/$', auth_views.login,
        {'template_name': 'restaurant/sign_in.html'},
        name = 'restaurant-sign-in'),
    url(r'^restaurant/sign-out', auth_views.logout,
        {'next_page': '/'},
        name = 'restaurant-sign-out'),
    url(r'^restaurant/sign-up/$', views.restaurant_sign_up,
        name ='restaurant-sign-up'),

    url(r'^restaurant/account/$', views.restaurant_account, name ='restaurant-account'),
    url(r'^restaurant/meal/$', views.restaurant_meal, name ='restaurant-meal'),
    url(r'^restaurant/meal/add/$', views.restaurant_add_meal, name ='restaurant-add-meal'),
#Example of editing a page with the link insode that page
    url(r'^restaurant/meal/edit/(?P<meal_id>\d+)/$', views.restaurant_edit_meal, name ='restaurant-edit-meal'),

    url(r'^restaurant/order/$', views.restaurant_order, name ='restaurant-order'),
    url(r'^restaurant/report/$', views.restaurant_report, name ='restaurant-report'),


#Facebook oauth2 API -Sign In/Sign up/Sign out
    url(r'^api/social/', include('rest_framework_social_oauth2.urls')),
    #/covert-token (sign in/sign up)
    #/revoke-token (sign out)

############# APIs ##############
#API for notification#
    url(r'^api/restaurant/order/notification/(?P<last_request_time>.+)/$', api.restaurant_order_notification),
## API for CUSTOMERS
    url(r'^api/customer/restaurants/$', api.customer_get_restaurants),
    url(r'^api/customer/meal/(?P<restaurant_id>\d+)/$', api.customer_get_meals),
    url(r'^api/customer/order/add/$', api.customer_add_order),
    url(r'^api/customer/order/latest/$', api.customer_get_latest_order),
## API for DRIVERS
    url(r'^api/driver/orders/ready/$', api.driver_get_ready_orders),
    url(r'^api/driver/order/pick/$', api.driver_pick_order),
    url(r'^api/driver/order/latest/$', api.driver_get_latest_order),
    url(r'^api/driver/order/complete/$', api.driver_get_complete_order),
    url(r'^api/driver/revenue/$', api.driver_get_revenue),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

 url(r'^api/driver/orders/ready/$', api.driver_get_ready_orders),
    url(r'^api/driver/order/pick/$', api.driver_pick_order),
    url(r'^api/driver/order/latest/$', api.driver_get_latest_order),
    url(r'^api/driver/order/complete/$', api.driver_get_complete_order),
    url(r'^api/driver/revenue/$', api.driver_get_revenue),
