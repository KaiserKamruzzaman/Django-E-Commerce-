from django.urls import path
from . import views

app_name='ecom_app'

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('login/',views.userLogin,name='userLogin'),
    path('register/',views.register,name='register'),
    path('logout/',views.userLogout,name='userLogout'),


    # api section----------------------------------------------
    path('updateItem/', views.updateItem, name='updateItem'),
    path('process_order/', views.process_order, name='process_order')
]
