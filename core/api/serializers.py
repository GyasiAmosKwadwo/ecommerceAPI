from rest_framework import serializers
from .models import Category, Product
from django.contrib.auth.models import User
from rest_framework.relations import PrimaryKeyRelatedField

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Product
        fields = (
            'id', 
            'name', 
            'price', 
            'category', 
            'description', 
            'imageurl', 
            'status', 
            'created_by', 
            'date_created'
        )

class UserSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, queryset=Product.objects.all())
    class Meta:
        model = User
        fields = ['id', 
                  'username', 
                  'email', 
                  'products']