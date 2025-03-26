from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("search/", views.searchView, name='search'),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutPage, name="logout"),
    path("register/", views.register, name="register"),
    path("update_item/", views.updateItem, name="update_item"),
    path('delete_selected_items/', views.delete_selected_items, name='delete_selected_items'),
    path("shipping/", views.shipping, name="shipping"), 
    path("productdetail/<int:product_id>/", views.productDetail, name="product_detail")
]