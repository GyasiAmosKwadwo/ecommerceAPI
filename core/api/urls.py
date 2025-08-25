from django.urls import path
from . import views

urlpatterns = [
    path('category/', views.categoryList.as_view()),
    path('category/<int:id>/', views.detailCategory.as_view()),
    path('product/', views.productList.as_view()),
    path('product/<int:id>/', views.detailProduct.as_view()),
]