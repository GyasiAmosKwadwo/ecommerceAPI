from django.shortcuts import render
from rest_framework import generics
from .serializers import CategorySerializer, ProductSerializer
from .models import Category, Product
# Create your views here.

class categoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class detailCategory(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'

class productList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class detailProduct(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
