from typing import ItemsView
from django.db import models
from rest_framework import serializers
from django.contrib.auth.models import User
from base.models import Order, OrderItem, Product, ShippingAddress
from rest_framework_simplejwt.tokens import RefreshToken




class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields='__all__'


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=User
#         fields = ["id", "email", "username", "password"]

#     def create(self, validated_data):
#         user = User.objects.create(email=validated_data['email'],
#                                        username=validated_data['username']
#                                          )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user


        
class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format="%Y-%m-%d")
    name=serializers.SerializerMethodField(read_only=True)
    _id=serializers.SerializerMethodField(read_only=True)
    isAdmin=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=User
        # fields=['id','_id','username','email','name','isAdmin','password', 'date_joined','first_name' ]
        fields='_all_'
    def get_name(self,obj):
        name=obj.first_name
        if name=="":
            name=obj.email
        return name
    
    def get__id(self,obj):
        return obj.id

    def get_isAdmin(self,obj):
        return obj.is_staff

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')



class UserSerializerWithToken(UserSerializer):
    token=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=User
        fields=['id','_id','username','email','name','isAdmin','token']
    
    def get_token(self,obj):
        token=RefreshToken.for_user(obj)
        return str(token.access_token)
    
class ShippingAddressSerializer (serializers.ModelSerializer): 
    class Meta:
        model = ShippingAddress
        fields = '_all____'

class OrderItemSerializer (serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer (serializers. ModelSerializer):
    orderItems = serializers.SerializerMethodField (read_only=True) 
    shippingAddress = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField (read_only=True)
    class Meta:
        model = Order
        fields = all
    def get_orderItems(self, obj): 
        items = obj.orderitem_set.all()
        serializer = OrderItemSerializer (items, many=True)
        return serializer.data
    def get_shippingAddress (self, obj):
        try:
            address = ShippingAddressSerializer(
                obj.shippingAddress, many=False
            )
        except:
            address = False
        return address
    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer (user, many=False)
        return serializer.data
    


