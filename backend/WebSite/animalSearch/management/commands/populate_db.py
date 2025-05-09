from django.core.management.base import BaseCommand
from animalSearch.models import *
from django.utils import timezone
from faker import Faker
import random

fake = Faker('ru_RU')


class Command(BaseCommand):
    help = "Автоматическое заполнение базы данных фиктивными данными"

    def handle(self, *args, **kwargs):
        self.stdout.write("Заполнение базы данных...")

        self.create_users(10)
        self.create_pet_types_and_breeds()
        self.create_blogs(10)
        self.create_reviews(10)
        self.create_messages(20)
        self.create_notifications(10)
        self.create_pet_reports(20)
        self.create_favorite_reports(5)

        self.stdout.write("Готово.")

    def create_users(self, count):
        for _ in range(count):
            User.objects.create_user(
                username=fake.user_name(),
                password='password123',
                email=fake.unique.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                middle_name=fake.middle_name(),
                phone=fake.phone_number(),
                photo=fake.image_url()
            )

    def create_pet_types_and_breeds(self):
        types = ['Собака', 'Кошка', 'Попугай', 'Хомяк']
        for type_name in types:
            pet_type = Pet_type.objects.create(type_name=type_name)
            for _ in range(3):
                Breed.objects.create(
                    pet_type_id=pet_type,
                    breed=fake.word().capitalize()
                )

    def create_blogs(self, count):
        for _ in range(count):
            Blog.objects.create(
                picture=fake.image_url(),
                title=fake.sentence(nb_words=6),
                description=fake.text(max_nb_chars=500),
                short_desc=fake.text(max_nb_chars=100)
            )

    def create_reviews(self, count):
        users = User.objects.all()
        for _ in range(count):
            Review.objects.create(
                user_id=random.choice(users),
                photo=fake.image_url(),
                text=fake.paragraph(nb_sentences=3),
                rating=random.randint(1, 5)
            )

    def create_messages(self, count):
        users = list(User.objects.all())
        for _ in range(count):
            sender, receiver = random.sample(users, 2)
            Message.objects.create(
                sender_id=sender,
                receiver_id=receiver,
                text=fake.text(max_nb_chars=200)
            )

    def create_notifications(self, count):
        for user in User.objects.all():
            for _ in range(count // 2):
                Notification.objects.create(
                    user_id=user,
                    text=fake.sentence(),
                    read=random.choice([True, False])
                )

    def create_pet_reports(self, count):
        users = User.objects.all()
        breeds = Breed.objects.all()
        types = list(Report_type.values)

        for _ in range(count):
            Pet_Report.objects.create(
                user_id=random.choice(users),
                breed_id=random.choice(breeds),
                title=fake.sentence(nb_words=6),
                resolved=random.choice([True, False]),
                special_marks=fake.word(),
                picture=fake.image_url(),
                public_date=fake.date_time_this_year(),
                report_type=random.choice(types),
                location=fake.address(),
                description=fake.text(max_nb_chars=200)
            )

    def create_favorite_reports(self, count):
        users = User.objects.all()
        reports = list(Pet_Report.objects.all())
        for _ in range(count):
            user = random.choice(users)
            fav = FavoriteReports.objects.create(user_id=user)
            fav.reports.set(random.sample(reports, min(len(reports), random.randint(1, 5))))
