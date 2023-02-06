from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import * 
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'role',
            'first_name',
            'last_name'
        )

    def create(self, validated_data):
        auth_user = User.objects.create_user(**validated_data)
        return auth_user

#1) serializer for roomtype
class Roomtype_serializer(serializers.ModelSerializer):
    class Meta:
        model=Roomtype
        fields="__all__"

#2) serializer for rooms
class Rooms_serializer(serializers.ModelSerializer):
    class Meta:
        model=Rooms
        fields="__all__"  

#3) serializer for booking
class Booking_serializer(serializers.ModelSerializer):
    class Meta:
        model=Booking
        fields="__all__"  
