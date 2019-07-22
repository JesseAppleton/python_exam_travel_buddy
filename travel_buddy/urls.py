from django.urls import path
from apps.travel_app import views

urlpatterns = [
    path('', views.index),
    path('main', views.main),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('travels', views.dashboard),
    path('travel/new', views.new),
    path('create', views.create),
    path('travel/<int:id>', views.view_trip),
    path('travel/<int:id>/delete', views.remove),
    path('travel/<int:id>/join', views.join),
    path('travel/<int:id>/unjoin', views.unjoin),

]
