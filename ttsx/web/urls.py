from django.conf.urls import url

from web import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^register/', views.register, name='register'),
    url(r'^goodslist/(?P<page>\d+)/(?P<class_f>\d+)/(?P<subclass>[0\u4e00-\u9fa5]+)/(?P<price_state>\d+)/(?P<popularity_state>\d+)/', views.goodslist, name='goodslist'),
    url(r'^goods/', views.goods, name='goods'),
    url(r'^upshopping/', views.upshopping, name='upshopping'),
    url(r'^shopping/', views.shopping, name='shopping'),
    url(r'^addshopping/', views.addshopping, name='addshopping'),
    url(r'^cutshopping/', views.cutshopping, name='cutshopping'),
    url(r'^delshopping/', views.delshopping, name='delshopping'),
    url(r'^check/', views.check, name='check'),
    url(r'^total/', views.total, name='total'),
    url(r'^check_all/', views.check_all, name='check_all'),

    url(r'^dispose_order/', views.dispose_order, name='dispose_order'),
    url(r'^order/', views.order, name='order'),
    url(r'^uporder/', views.uporder, name='uporder'),
    url(r'^user_center_info/', views.user_center_info, name='user_center_info'),
    url(r'^user_center_order/', views.user_center_order, name='user_center_order'),
    url(r'^user_center_site/', views.user_center_site, name='user_center_site'),
    url(r'^check_address/', views.check_address, name='check_address'),
    url(r'^show_site/', views.show_site, name='show_site'),
    url(r'^del_site/', views.del_site, name='del_site'),
]
