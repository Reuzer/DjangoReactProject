from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator

class report_type(models.TextChoices):
    LOST = "lost"
    FOUND = 'found'

class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(5)]
    )
    phone = models.CharField(
        max_length=30,
        validators=[MinLengthValidator(5)]    
    )
    registration_date = models.DateTimeField(auto_now_add=True)

class Blog(models.Model):
    picture = models.URLField
    title = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(5)] 
    )
    description = models.TextField
    short_desc = models.CharField(max_length=255)
    post_date = models.DateTimeField(auto_now_add = True)

class Message(models.Model): 
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.TextField
    rating = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ])
    date = models.DateTimeField(auto_now_add=True)

class Notification(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

class Breed(models.Model):
    breed = models.CharField(max_length=100)

class Pet_type(models.Model):
    type_name = models.CharField(max_length=100)
    breed = models.ForeignKey(Breed, on_delete=models.SET_NULL, null=True)

class Pet(models.Model):
    pet_type = models.ForeignKey(Pet_type, on_delete=models.SET_NULL, null=True)
    color = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    special_marks = models.TextField

class Pet_Report(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    picture = models.URLField
    pet = models.ForeignKey(Pet, on_delete=models.SET_NULL, null=True)
    public_date = models.DateTimeField(auto_now_add=True)
    change_date = models.DateTimeField
    report_type = models.CharField(max_length=20, choices = report_type.choices)
    location = models.CharField(max_length=255)
    description = models.TextField

