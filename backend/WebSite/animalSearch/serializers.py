from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate, get_user_model



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
            'role'     
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
        fields = ['photo', 'text', 'rating']
    
    def create(self, validated_data):
        user = self.context['request'].user
        review = Review.objects.create(user_id=user, **validated_data)
        return review


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
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Pet_Report
        fields = [
            'id',
            'user_id',
            'breed_id', 
            'title',
            'resolved',
            'special_marks',
            'thumbnail',
            'picture',
            'public_date',
            'report_type',
            'location',
            'description'
        ]

    def get_thumbnail(self, obj):
        if obj.picture:           
            return f"{obj.picture.url}?width=400&height=400"
        return None
    

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
    
    def validate(self, data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Требуется авторизация")

        # Проверяем только при создании (не при обновлении)
        if self.instance is None:
            description = data.get('description', '').strip()

            duplicate_exists = Pet_Report.objects.filter(
                user_id=request.user,
                description__iexact=description,
                resolved=False
            ).exists()

            if duplicate_exists:
                raise serializers.ValidationError({
                    'non_field_errors': ['У вас уже есть активное объявление с таким же описанием и местоположением']
                })

        return data

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user
        return super().create(validated_data)

class UserRegistrationSerializer(serializers.ModelSerializer):

    middle_name = serializers.CharField(required=False)
    photo = serializers.URLField(required=False)


    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'middle_name', 'phone', 'photo']
        extra_kwargs = {"password":{"write_only": True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):  
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            
            if not user:
                raise serializers.ValidationError('Неверные учетные данные')
            
            if not user.is_active:
                raise serializers.ValidationError('Аккаунт деактивирован')
            
            attrs['user'] = user
            return attrs
        
        raise serializers.ValidationError('Необходимо указать username и password')
        

class PetReportShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet_Report
        fields = ('id', 'title', 'created_at')  # добавьте нужные поля

class FavoriteReportItemSerializer(serializers.ModelSerializer):
    report = PetReportShortSerializer(read_only=True)
    
    class Meta:
        model = FavoriteReportItem
        fields = ('id', 'report', 'added_at')
        read_only_fields = ('added_at',)

class FavoriteReportsSerializer(serializers.ModelSerializer):
    reports = PetReportShortSerializer(many=True, read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = FavoriteReports
        fields = ('id', 'user_id', 'reports')

class AddToFavoriteSerializer(serializers.Serializer):
    report_id = serializers.PrimaryKeyRelatedField(
        queryset=Pet_Report.objects.all(),
        source='report'
    )

    def create(self, validated_data):
        favorite, _ = FavoriteReports.objects.get_or_create(
            user_id=self.context['request'].user
        )
        report = validated_data['report']
        
        fav_item, created = FavoriteReportItem.objects.get_or_create(
            favorite=favorite,
            report=report
        )
        
        if not created:
            raise serializers.ValidationError("Это объявление уже в избранном")
            
        return fav_item


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