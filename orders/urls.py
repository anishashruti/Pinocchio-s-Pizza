from django.urls import path
from .views import user_order_list_view
from . import views
from django.conf.urls import url


urlpatterns = [
    path("", views.home, name="home"),
    path('about/', views.about,name='about'),
    path('toppings/<str:category>/<str:name>/', views.toppings,name='toppings'),
    path('menu/', views.menu,name='menu'),
    path('sub/', views.menu1,name='sub'),
    path('pizza/', views.pizza,name='pizza'),
    path("add/<str:category>/<str:size>/<str:name>/<str:price>", views.add, name="add"),
    path("delete/<str:category>/<str:size>/<str:name>/<str:price>", views.delete, name="delete"),
    path('order_placed/', views.order_placed,name='order_placed'),
    path('Cart/<str:username>', user_order_list_view.as_view(),name='MyCart'),
    path('success', views.success,name='success'),
    path('checkout/', views.checkout, name='checkout'),
]
