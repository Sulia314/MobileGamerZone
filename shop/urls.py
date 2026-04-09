from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('support/', views.support, name='support'),        # Новое
    path('compare/', views.compare, name='compare'),        # Новое
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
]