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

from Search import views

urlpatterns = [
    path('', views.search),
    path('details/<int:pet_pk>/', views.details),
    path('verify/<int:pet_pk>/', views.verify),
    path('details/addcomment/<int:pet_pk>/<int:comment_pk>/', views.addcomment),
    path('<int:category_pk>/', views.category),
    path('<int:category_pk>/<int:kind_pk>/', views.kind),
]
