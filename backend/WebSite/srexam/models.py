from django.db import models
from animalSearch.models import User; #Так как в я менял класс User в settings.py (для приложения animalSearch, пользователя импортирую именно от туда)

class srexam(models.Model):
    name = models.CharField("Название экзамена", max_length=255)
    created_at = models.DateTimeField("Дата создания записи", auto_now_add=True)
    exam_date = models.DateField("Дата проведения экзамена")
    image = models.ImageField("Изображение задания", upload_to="exam_images/", blank=True, null=True)
    students = models.ManyToManyField(User, related_name="exams", verbose_name="Студенты")
    is_public = models.BooleanField("Опубликовано", default=False)

    def __str__(self):
        return self.name
