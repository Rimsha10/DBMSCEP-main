#Programmer Defined
#____________IMPORTS_________________
from django.contrib import admin
from django.urls import path
from . import views
from .views import Signup , Login , logout,Profile, EditProfile
from django.urls import include, path
#____________HOME____________________
urlpatterns = [
    path('',views.index,name='index'),
#____________ABOUT____________________
    path('about/',views.about,name='about'),
#____________CONTACT____________________
    path('contact/',views.contact,name='contact'),
#__________________PRODUCTS PART_________________________
    path('products/',views.products,name='products'),
#__________________ProductDetails________________
    path('products/<int:id>',views.product_detail,name='product_detail'),
#__________________LOGIN_REGISTER_________________________
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', views.logout , name='logout'),
#____________PROFILE____________________
    path('profile/', Profile.as_view(), name='profile'),
   path("edit_profile/",EditProfile.as_view(),name="edit_profile"),
#____________________CART_____________________________
    path('cart', views.cart, name='cart'),
#________________________CHECKOUT__________________
    path('update_item/', views.updateItem, name="checkout"),
    path('checkout', views.checkout, name='checkout'),
    path('process_order/', views.processOrder, name='process_order'),
] 
