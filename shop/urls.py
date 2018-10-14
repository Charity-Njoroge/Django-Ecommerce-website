
from django.conf.urls import url
from . import views

app_name = 'shop'

urlpatterns = [
    #url to fetch all products 
    url(r'^$', views.home, name='home'),
       #url to fetch all products 
    url(r'^product_list/$', views.product_list, name='product_list'),
    #products we be filtered by a given category
    url(r'^(?P<category_slug>[-\w]+)/$', views.product_list, name='product_list_by_category'),
    #url for specific product
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),
    #url for the user profile
    url(r'^profile/$', views.userProfile, name='profile'),
]
