from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/<int:product_id>/', views.create_order, name='create'),
    path('my/', views.my_orders, name='my_orders'),
    path('courses/', views.my_courses, name='my_courses'),
    path('download/<int:order_id>/', views.download_pdf, name='download'),
]
