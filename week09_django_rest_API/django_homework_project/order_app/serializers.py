from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import Order

User = get_user_model()

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    buyer = serializers.ReadOnlyField(source='buyer.username')

    class Meta:
        model = Order
        fields = ['id', 'product_id', 'buyer', 'cancel_flag', 'createtime']

class CreateUserSerializer(serializers.HyperlinkedModelSerializer):
    # 創建用戶序列
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'password']

    def validate(self, attrs):
        #對密碼進行加密
        attrs['password'] = make_password(attrs['password'])
        return attrs

class UserSerializer(serializers.HyperlinkedModelSerializer):
    orders = OrderSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'orders']