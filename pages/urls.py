from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('find-product/', views.find_product, name='find_product'),

]