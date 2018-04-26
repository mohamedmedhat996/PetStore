"""PetStore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path

from Home import views

urlpatterns = [
    path('login/', views.login_f),
    path('delete/', views.delete),
    path('recover/', views.recover),
    path('recover/<int:user_pk>/<int:code>/', views.recover_p),
    path('activate/', views.activate),
    path('activate/<int:user_pk>/<int:code>/', views.activate_u),
    path('profile/', views.profile),
    path('logout/', views.logout_f),
    path('signup/', views.signup),
    path('addpaymentmethod/<int:number>/', views.addpaymentmethod),
]
