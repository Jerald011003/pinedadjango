from django.contrib.auth.models import User
from base.models import Product, Order, OrderItem, ShippingAddress
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import api_view,permission_classes
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
# Create your views here.
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .serializer import ProductSerializer,UserSerializer,UserSerializerWithToken, OrderSerializer, UserUpdateSerializer
from .products import products
from .serializer import ProductSerializer
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response


import logging

@api_view(['GET'])
def getRoutes(request):
    return Response('Hello World')

@api_view(['GET'])
def getProducts(request):
    # return Response(products)
    products=Product.objects.all()
    serializer=ProductSerializer(products,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProduct(request,pk):
    # product=None
    # for i in products:
    #     if i['_id']==pk:
    #         product=i
    #         break
    # return Response(product)
    product=Product.objects.get(_id=pk)
    serializer=ProductSerializer(product,many=False)
    return Response(serializer.data)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self,attrs):
        data=super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k,v in serializer.items():
            data[k]=v
    

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer
    
        


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def  getUserProfiles(request):
    user=request.user
    serializer=UserSerializer(user,many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def  getUsers(request):
    user=User.objects.all()
    serializer=UserSerializer(user,many=True)
    return Response(serializer.data)


# register the new users

@api_view(['POST'])
def registerUser(request):
    data=request.data
    print('registerUser() - received data:', data)
    try:

        user=User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )
        print('registerUser() - created user:', user)
        serializer=UserSerializerWithToken(user,many=False)
        return Response(serializer.data)
    except:
        message={'details':'USER WITH THIS EMAIL ALREADY EXIST'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST)

    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)
    data = request.data
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']

    if data['password'] != '':
        user.password = make_password(data['password'])
    user.save()
    return Response(serializer.data)


# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def updateUserProfile(request):
#     user =request.user 
#     serializer = UserSerializerWithToken(user,many = False)
#     data = request.data
#     user.first_name = data['name']
#     user.username = data['email']
#     user.email = data['email']
#     if data['password'] !="":
#         user.password= make_password(data['password'])
#     user.save()
#     return Response(serializer.data)

@api_view(['POST'])
@permission_classes ([IsAuthenticated]) 
def addorderItems (request):
    user = request.user
    data = request.data
    
    orderItems = data['orderItems']
    if orderItems and len (orderItems) == 0: return Response({'detail': 'No Order Item'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        order = Order.objects.create(
            user=user,
            paymentMethod=data['paymentMethod'], 
            taxPrice=data['taxPrice'], 
            shippingPrice=data['shippingPrice'], 
            totalPrice=data['totalPrice']
        )
        shipping = ShippingAddress.objects.create(
            order=order,
            address=data['shippingAddress']['address'],
            city=data['shippingAddress']['city'], 
            postalCode=data['shippingAddress']['postalCode'],
            country=data['shippingAddress']['country'],
        )

        for i in orderItems:
            product = Product.objects.get(_id=i['product']) 
            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                qty=i['qty'],
                price=i['price'],
                image=product.image.url,
            )
            product.countInStock -= item.qty
            product.save()
            serializer = OrderSerializer (order, many=False)
            return Response(serializer.data)

@api_view(['GET'])
@permission_classes ([IsAuthenticated]) 
def getMyOrders (request):
    user = request.user
    orders = user.order_set.all()
    serializer = OrderSerializer (orders, many=True) 
    return Response (serializer.data)

@api_view(['PUT'])
@permission_classes ([IsAuthenticated]) 
def updateOrdertoPaid (request, pk):
    order = Order.objects.get(_id=pk)
    order.isPaid = True
    order.paidAt = datetime.now() 
    order.save()
    return Response("Order was paid")

def getOrders(request):
    user = request.user
    print(user)
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getOrderById(request, pk):

    user = request.user

    try:
        order = Order.objects.get(_id=pk)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            Response({'detail': 'Not Authorized  to view this order'},
                     status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail': 'Order does not exist'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getUsers(request):
    
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateOrderToDelivered(request, pk):
    order = Order.objects.get(_id=pk)
    order.isDeliver = True
    order.deliveredAt = datetime.now()
    order.save()
    return Response('Order was Delivered')

# chubanes
class GetUserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        try:
            user = self.request.user
            username = user.username

            user_profile = User.objects.get(id=user.id)
            user_profile_serialized = UserSerializer(user_profile)

            return Response({ 'profile': user_profile_serialized.data, 'username': str(username) })
        except User.DoesNotExist:
            return Response({ 'error': 'User does not exist' }, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({ 'error': 'Something went wrong when retrieving profile' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

logger = logging.getLogger(__name__)

# class UpdateUserProfileView(APIView):
#     # permission_classes = [IsAuthenticated]

#     def put(self, request, format=None):
#         try:
#             user = self.request.user

#             data = self.request.data
#             logger.debug(f"Received data: {data}")
#             user_update_serializer = UserUpdateSerializer(user, data=data, partial=True)
#             user_update_serializer.is_valid(raise_exception=True)
#             user_update_serializer.save()

#             user_serializer = UserSerializer(user)

#             return Response(user_serializer.data)
#         except Exception as e:
#             logger.exception(e)
#             return Response({ 'error': 'Something went wrong when updating profile' }, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['PUT'])
# def UpdateUserProfileView(request):
#     try:
#         user = request.user
#         data = request.data
#         logger.debug(f"Received data: {data}")
#         user_update_serializer = UserUpdateSerializer(user, data=data, partial=True)
#         user_update_serializer.is_valid(raise_exception=True)
#         user_update_serializer.save()
#         user_serializer = UserSerializer(user)
#         return Response(user_serializer.data)
#     except Exception as e:
#         logger.exception(e)
#         return Response({ 'error': 'Something went wrong when updating profile' }, status=status.HTTP_400_BAD_REQUEST)
