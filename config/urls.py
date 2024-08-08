"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from base import views
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('admin/', admin.site.urls),
    
    #Cart
    path('cart/remove/<str:pk>/',views.remove_from_cart),
    path('cart/add/',views.AddCartView.as_view()),
    path('cart/',views.CartListView.as_view()),

    #account
    path('signup/',views.SignupView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('login/',views.Login.as_view()),
    path('account/',views.AccountUpdateView.as_view()),
    path('profile/',views.ProfileUpdateView.as_view()),
    

    #Order
    path('order/<str:pk>/',views.OrderDetailView.as_view()),
    path('order/',views.OrderListView.as_view()),
    
    #Pay
    path('pay/checkout/',views.PayWithStripe.as_view()),
    path('pay/success/',views.PaySuccessView.as_view()),
    path('pay/cancel/',views.PayCancelView.as_view()),
    
    #Item
    path('tags/<str:pk>/',views.TagListView.as_view()),
    path('category/<str:pk>/',views.CategoryListView.as_view()),
    path('items/<str:pk>/', views.ItemDetailView.as_view()),
    
    path('',views.ListView.as_view()),
]
