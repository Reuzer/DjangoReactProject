from django.db import models
from django.utils import timezone;
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator




class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(8)]
    )
    phone = models.CharField(
        max_length=30,
        validators=[MinLengthValidator(5)]    
    )
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Blog(models.Model):
    picture = models.URLField
    title = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(5)] 
    )
    description = models.TextField
    short_desc = models.CharField(max_length=255)
    post_date = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
        ordering = ['-post_date']


class Message(models.Model): 
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='sent_messages', null=True)
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='received_messages', null=True)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return f'Сообщения {self.sender.name} отправленные к {self.receiver.name}'
    
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.TextField
    rating = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ])
    date = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return f'Отзыв от {self.user.name}'
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Notification(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__ (self):
        return f'Оповещение к пользователю {self.user.name}'
    
    class Meta:
        verbose_name = 'Оповещение'
        verbose_name_plural = 'Оповещения'


class Pet_type(models.Model):
    type_name = models.CharField(max_length=100)

    def __str__ (self):
        return self.type_name
    
    class Meta:
        verbose_name = 'Животное'
        verbose_name_plural = 'Животные'
    

class Breed(models.Model):
    pet_type = models.ForeignKey(Pet_type, on_delete=models.CASCADE)
    breed = models.CharField(max_length=100)

    def __str__ (self):
        return self.breed
    
    class Meta:
        verbose_name = 'Порода'
        verbose_name_plural = 'Породы'


class Report_type(models.TextChoices):
    LOST = "lost", "Потеряно"
    FOUND = 'found', "Найдено"


class Pet_Report_Manager(models.Manager):

    def lost_pets(self):
        return self.filter(report_type="lost")
    
    def found_pets(self):
        return self.filter(report_type="found")


class Pet_Report(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    pet_type = models.ForeignKey(Pet_type, on_delete=models.SET_NULL, null=True)
    color = models.CharField(max_length=100, null=True)
    size = models.CharField(max_length=50)
    special_marks = models.CharField(max_length=255)
    picture = models.URLField(null=True)
    public_date = models.DateTimeField(default=timezone.now)
    change_date = models.DateTimeField(auto_now=True, null=True)
    report_type = models.CharField(max_length=20, choices = Report_type.choices)
    location = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    objects = Pet_Report_Manager()

    def __str__(self):
        return f'Объявление пользователя: {self.user_id.name}, статус: {self.report_type}'

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering=['-public-date']

    #verbose_name
class FavoriteReports(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_reports')
    reports = models.ManyToManyField(Pet_Report, related_name='favorited_by')

    def __str__(self):
        return f"Избранные объявления пользователя {self.user.name}"
        
    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные объявления'

