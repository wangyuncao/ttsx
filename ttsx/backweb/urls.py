from django.conf.urls import url

from backweb import views

urlpatterns = [
    url(r'^login/', views.login, name='login'),
    url(r'^index/', views.index, name='index'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^addclassify/', views.addclassify, name='addclassify'),
    url(r'^goods/', views.goods, name='goods'),
    url(r'^addgoods/', views.addgoods, name='addgoods'),
    url(r'^upclassification/', views.upclassification, name='upclassification'),
    url(r'^carousel/', views.carousel, name='carousel'),
    url(r'^static/', views.static, name='static'),
    url(r'^pattern/', views.pattern, name='pattern'),
    url(r'^addpattern/', views.addpattern, name='addpattern'),
    url(r'^goods_recommend/', views.goods_recommend, name='goods_recommend'),
    url(r'^goods_new/', views.goods_new, name='goods_new'),
    url(r'^goods_del/', views.goods_del, name='goods_del'),
    url(r'^order/', views.order, name='order'),
    url(r'^uporder/', views.uporder, name='uporder'),
    url(r'^user_show/', views.user_show, name='user_show'),
    url(r'^is_root/', views.is_root, name='is_root'),
    url(r'^distribution/', views.distribution, name='distribution'),
    url(r'^adddistribution/', views.adddistribution, name='adddistribution'),
]
