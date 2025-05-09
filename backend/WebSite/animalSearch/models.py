from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    middle_name = models.CharField(max_length=30, verbose_name='Отчество', blank=True)
    photo = models.URLField(blank=True)
    email = models.EmailField(unique=True, verbose_name='Почта')
    phone = models.CharField(
        max_length=30,
        validators=[MinLengthValidator(5)],
        verbose_name='Номер телефона'
    )

    def __str__(self):
        return self.last_name
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Blog(models.Model):
    picture = models.URLField(verbose_name='Картинка')
    title = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(5),
        ],
        verbose_name='Заголовок' 
    )
    description = models.TextField(verbose_name='Описание')
    short_desc = models.CharField(max_length=255, verbose_name='Превью')
    post_date = models.DateTimeField(auto_now_add = True, verbose_name='Дата создания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
        ordering = ['-post_date']


class Message(models.Model): 
    sender_id = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='sent_messages', null=True, verbose_name='Отправитель')
    receiver_id = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='received_messages', null=True, verbose_name='Получатель')
    text = models.TextField(verbose_name='Текст')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__ (self):
        return f'Сообщения {self.sender_id.last_name} отправленные к {self.receiver_id.last_name}'
    
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Review(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name='reviews', verbose_name='Пользователь')
    photo = models.URLField(blank=True)
    text = models.TextField(verbose_name='Текст')
    rating = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ],
    verbose_name='Оценка'
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__ (self):
        return f'Отзыв от {self.user_id.last_name}'
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Notification(models.Model): 
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    read = models.BooleanField(default=False, verbose_name='Прочитано?')

    def __str__ (self):
        return f'Оповещение к пользователю {self.user_id.last_name}'
    
    class Meta:
        verbose_name = 'Оповещение'
        verbose_name_plural = 'Оповещения'


class Pet_type(models.Model):
    type_name = models.CharField(max_length=100, verbose_name='Название')

    def __str__ (self):
        return self.type_name
    
    class Meta:
        verbose_name = 'Животное'
        verbose_name_plural = 'Животные'
    

class Breed(models.Model):
    pet_type_id = models.ForeignKey(Pet_type, on_delete=models.CASCADE, verbose_name='Животное')
    breed = models.CharField(max_length=100, verbose_name='Порода')

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
    user_id = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name='Пользователь')
    breed_id = models.ForeignKey(Breed, on_delete=models.SET_NULL, null=True, verbose_name='Животное')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    resolved = models.BooleanField(default=False, verbose_name='Закрыто?')
    special_marks = models.CharField(max_length=255, verbose_name='Отличительные знаки')
    picture = models.URLField(null=True, verbose_name='Картинка')
    public_date = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    change_date = models.DateTimeField(auto_now=True, null=True, verbose_name='Дата изменения')
    report_type = models.CharField(max_length=20, choices = Report_type.choices, verbose_name='Статус')
    location = models.CharField(max_length=255, verbose_name='Локация')
    description = models.CharField(max_length=255, verbose_name='Описание')

    objects = Pet_Report_Manager()

    def get_absolute_url(self):
        return reverse("report_detail", kwargs={"pk": self.pk})
    

    def __str__(self):
        return f'Объявление пользователя: {self.user_id.last_name}, статус: {self.report_type}'

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering=['-public_date']

    #verbose_name
class FavoriteReports(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_reports', verbose_name='Пользователь')
    reports = models.ManyToManyField(Pet_Report, related_name='favorited_by', verbose_name='Объявления')

    def __str__(self):
        return f"Избранные объявления пользователя {self.user_id.last_name}"
        
    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные объявления'


"""
from animalSearch.models import Pet_Report

report = Pet_Report.objects.first()
print(report.get_absolute_url())  
"""

