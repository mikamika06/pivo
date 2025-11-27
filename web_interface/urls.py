from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list_view, name='product_list'),
    path('<int:pk>/', views.product_detail_view, name='product_detail'),
    path('create/', views.product_create_view, name='product_create'),
    path('<int:pk>/update/', views.product_update_view, name='product_update'),
    path('<int:pk>/delete/', views.product_delete_view, name='product_delete'),
    
    path('external/', views.external_products_list_view, name='external_products_list'),
    path('external/<int:pk>/delete/', views.external_product_delete_view, name='external_product_delete'),
]
