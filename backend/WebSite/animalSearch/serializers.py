from rest_framework import serializers
from .models import Pet_Report, Blog, Review, Pet_type, Breed, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'photo', 'email', 'phone']


class Pet_Report_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Pet_Report
        fields = '__all__'


class Blog_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'


class Review_Serializer(serializers.ModelSerializer):
    user_id = UserSerializer(read_only=True)
    class Meta:
        model = Review
        fields = '__all__'


class Pet_type_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Pet_type
        fields = '__all__'


class Breed_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = '__all__'




"""
Запросы к БД нужные сайту

Получение списка Объявлений
Получение объявления по id
Получение блогов
Получение животный + пород (для формы)
Получение списка отзывов

"""