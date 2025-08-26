from rest_framework import serializers
from .models import * 
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
        
class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Customer
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Employee
        fields = '__all__'

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = table
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    table = TableSerializer()
    class Meta:
        model = Reservation
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    product = ProductSerializer(many=True)
    class Meta:
        model = Cart
        fields = '__all__'

    def create(self, validated_data):
        products_data = validated_data.pop('product')
        cart = Cart.objects.create(**validated_data)
        for product_data in products_data:
            product, created = Product.objects.get_or_create(**product_data)
            cart.product.add(product)
        return cart
    
    def update(self, instance, validated_data):
        products_data = validated_data.pop('product')
        instance.user = validated_data.get('user', instance.user)
        instance.save()

        instance.product.clear()
        for product_data in products_data:
            product, created = Product.objects.get_or_create(**product_data)
            instance.product.add(product)
        return instance
    
class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    cart = CartSerializer()
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        cart_data = validated_data.pop('cart')
        user, created = User.objects.get_or_create(**user_data)
        cart, created = Cart.objects.get_or_create(**cart_data)
        order = Order.objects.create(user=user, cart=cart, **validated_data)
        return order
    
class DeliverySerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    class Meta:
        model = delivery
        fields = '__all__'

    def create(self, validated_data):
        order_data = validated_data.pop('order')
        order, created = Order.objects.get_or_create(**order_data)
        delivery_instance = delivery.objects.create(order=order, **validated_data)
        return delivery_instance
    
    def update(self, instance, validated_data):
        order_data = validated_data.pop('order')
        instance.status = validated_data.get('status', instance.status)
        instance.date = validated_data.get('date', instance.date)
        instance.save()

        order, created = Order.objects.get_or_create(**order_data)
        instance.order = order
        instance.save()
        return instance
    
class ReservationSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    table = TableSerializer()
    class Meta:
        model = Reservation
        fields = '__all__'

    def create(self, validated_data):
        owner_data = validated_data.pop('owner')
        table_data = validated_data.pop('table')
        owner, created = User.objects.get_or_create(**owner_data)
        table, created = table.objects.get_or_create(**table_data)
        reservation = Reservation.objects.create(owner=owner, table=table, **validated_data)
        return reservation
    
    def update(self, instance, validated_data):
        owner_data = validated_data.pop('owner')
        table_data = validated_data.pop('table')
        instance.status = validated_data.get('status', instance.status)
        instance.no_of_people = validated_data.get('no_of_people', instance.no_of_people)
        instance.date = validated_data.get('date', instance.date)
        instance.save()

        owner, created = User.objects.get_or_create(**owner_data)
        table, created = table.objects.get_or_create(**table_data)
        instance.owner = owner
        instance.table = table
        instance.save()
        return instance
    
class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Employee
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user, created = User.objects.get_or_create(**user_data)
        employee = Employee.objects.create(user=user, **validated_data)
        return employee
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        instance.position = validated_data.get('position', instance.position)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.address = validated_data.get('address', instance.address)
        instance.save()

        user, created = User.objects.get_or_create(**user_data)
        instance.user = user
        instance.save()
        return instance
    
