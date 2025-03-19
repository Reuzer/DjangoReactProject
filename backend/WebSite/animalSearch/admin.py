from django.contrib import admin
from .models import User, Blog, Message, Review, Notification, Breed, Pet_type, Pet, Pet_Report, report_type

# Регистрация модели User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'registration_date')  # что показывать в списке
    search_fields = ('name', 'email')  # поля для поиска
    list_filter = ('registration_date',)  # фильтры
    ordering = ('-registration_date',)  # сортировка по дате регистрации

# Регистрация модели Blog
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'post_date', 'short_desc')
    search_fields = ('title', 'short_desc')
    list_filter = ('post_date',)
    ordering = ('-post_date',)

# Регистрация модели Message
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp')
    search_fields = ('sender__name', 'receiver__name')  # поиск по имени отправителя и получателя
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)

# Регистрация модели Review
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'date')
    search_fields = ('user__name',)
    list_filter = ('rating', 'date')
    ordering = ('-date',)

# Регистрация модели Notification
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'date', 'read')
    search_fields = ('user__name', 'text')
    list_filter = ('read', 'date')
    ordering = ('-date',)

# Регистрация модели Breed
@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('breed',)
    search_fields = ('breed',)

# Регистрация модели Pet_type
@admin.register(Pet_type)
class PetTypeAdmin(admin.ModelAdmin):
    list_display = ('type_name', 'breed')
    search_fields = ('type_name', 'breed__breed')  # поиск по типу и породе
    list_filter = ('breed',)

# Регистрация модели Pet
@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('pet_type', 'color', 'size', 'special_marks')
    search_fields = ('color', 'size', 'special_marks')
    list_filter = ('pet_type',)

# Регистрация модели Pet_Report
@admin.register(Pet_Report)
class PetReportAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'pet', 'report_type', 'public_date', 'location')
    search_fields = ('user_id__name', 'pet__color', 'location', 'report_type')
    list_filter = ('report_type', 'public_date')
    ordering = ('-public_date',)

#admin
#Sergey2005