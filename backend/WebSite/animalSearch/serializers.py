from rest_framework import serializers
from .models import Pet_Report, Blog, Review, Pet_type, Breed, User
from django.contrib.auth import authenticate

class UserReadSerializer (serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'middle_name',
            'photo',
            'phone',     
        ]
        read_only_fields = ['id', 'email', 'username']

class BlogReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = '__all__'

class BlogWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = [
            'picture',
            'title',
            'description',
            'short_desc'
        ]


class ReviewReadSerializer(serializers.ModelSerializer):

    user_id = UserReadSerializer(read_only = True)

    class Meta:
        model = Review
        fields = '__all__'
    

class ReviewWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = [
            'user_id',
            'photo',
            'text',
            'rating',
        ]


class PetTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pet_type
        fields = '__all__'


class BreedSerializer(serializers.ModelSerializer):

    pet_type_id = PetTypeSerializer(read_only=True)

    class Meta: 
        model = Breed
        fields = '__all__'


class PetReportReadSerializer(serializers.ModelSerializer):

    user_id = UserReadSerializer(read_only = True)
    breed_id = BreedSerializer(read_only = True)

    class Meta:
        model = Pet_Report
        fields = [
            'id',
            'user_id',
            'breed_id', 
            'title',
            'resolved',
            'special_marks',
            'picture',
            'public_date',
            'report_type',
            'location',
            'description'
        ]
    

class PetReportWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pet_Report
        fields = [
            'user_id',
            'breed_id',
            'title',
            'resolved',
            'special_marks',
            'picture',
            'report_type',
            'location',
            'description'
        ]

class UserRegistrationSerializer(serializers.ModelSerializer):

    middle_name = serializers.CharField(required=False)
    photo = serializers.URLField(required=False)


    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'middle_name', 'phone']
        extra_kwargs = {"password":{"write_only": True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only = True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('incorrect credentials')
        


"""
User
Blog
Review
Pet_type
Breed
Pet_Report_Serializer
    user_id = UserSerializer(read_only=True)
    breed_id = Breed_Serializer(read_only=True)

"""