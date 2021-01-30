from django.urls import path, include
from order_app import views

urlpatterns = [
    path('', views.OrderViewSet),
    path('create/', views.order_create),
    path('<int:id>/cancel/', views.order_cancelling),
]