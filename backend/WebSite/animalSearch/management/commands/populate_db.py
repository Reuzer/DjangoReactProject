import random
from django.core.management.base import BaseCommand
from faker import Faker
from animalSearch.models import (
    User, Blog, Message, Review, Notification, Pet_type, Breed,
    Pet_Report, FavoriteReports
)

fake = Faker("ru_RU")


class Command(BaseCommand):
    help = "Создает фейковые данные для базы"

    def handle(self, *args, **kwargs):
        self.stdout.write("Создание пользователей...")
        users = self.create_users(10)

        self.stdout.write("Создание блогов...")
        self.create_blogs(10)

        self.stdout.write("Создание сообщений...")
        self.create_messages(users, 10)

        self.stdout.write("Создание отзывов...")
        self.create_reviews(users, 10)

        self.stdout.write("Создание уведомлений...")
        self.create_notifications(users, 10)

        self.stdout.write("Создание типов животных и пород...")
        pet_types = self.create_pet_types_and_breeds()

        self.stdout.write("Создание объявлений...")
        self.create_pet_reports(users, pet_types, 10)

        self.stdout.write("Создание избранных объявлений...")
        self.create_favorite_reports(users, 5)

        self.stdout.write(self.style.SUCCESS("✅ Фейковые данные успешно созданы!"))

    def create_users(self, n):
        users = []
        for _ in range(n):
            user = User(
                username=fake.unique.user_name(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                middle_name=fake.first_name(),
                photo = fake.image_url(),
                email=fake.unique.email(),
                phone=fake.phone_number()
            )
            user.set_password("testpassword123")  # безопасно устанавливаем пароль
            user.save()
            users.append(user)
        return users

    def create_blogs(self, n):
        for _ in range(n):
            Blog.objects.create(
                picture=fake.image_url(),
                title=fake.sentence(nb_words=6),
                description=fake.text(max_nb_chars=300),
                short_desc=fake.sentence(nb_words=12)
            )

    def create_messages(self, users, n):
        for _ in range(n):
            sender, receiver = random.sample(users, 2)
            Message.objects.create(
                sender_id=sender,
                receiver_id=receiver,
                text=fake.text(max_nb_chars=50)
            )

    def create_reviews(self, users, n):
        for _ in range(n):
            Review.objects.create(
                user_id=random.choice(users),
                photo = fake.image_url(),
                text=fake.text(max_nb_chars=300),
                rating=random.randint(1, 5)
            )

    def create_notifications(self, users, n):
        for _ in range(n):
            Notification.objects.create(
                user_id=random.choice(users),
                text=fake.text(max_nb_chars=50)
            )

    def create_pet_types_and_breeds(self):
        pet_types = ["Собака", "Кошка", "Попугай", "Хомяк"]
        breeds = {
            "Собака": ["Лабрадор", "Овчарка", "Спаниель"],
            "Кошка": ["Британец", "Сиамская", "Мейн-кун"],
            "Попугай": ["Волнистый", "Ара", "Жако"],
            "Хомяк": ["Джунгарик", "Сирийский", "Роборовский"]
        }

        pet_type_objs = {}
        for pet in pet_types:
            pet_type = Pet_type.objects.create(type_name=pet)
            pet_type_objs[pet] = pet_type

            for breed in breeds[pet]:
                Breed.objects.create(pet_type_id=pet_type, breed=breed)

        return list(pet_type_objs.values())

    def create_pet_reports(self, users, pet_types, n):
        for _ in range(n):
            pet_type = random.choice(pet_types)
            Pet_Report.objects.create(
                user_id=random.choice(users),
                pet_type_id=pet_type,
                title=fake.sentence(nb_words=6),
                special_marks=fake.sentence(nb_words=8),
                picture=fake.image_url(),
                report_type=random.choice(["lost", "found"]),
                location=fake.address(),
                description=fake.text(max_nb_chars=100)
            )

    def create_favorite_reports(self, users, n):
        reports = list(Pet_Report.objects.all())
        for user in users:
            fav = FavoriteReports.objects.create(user_id=user)
            if reports:
                fav.reports.add(*random.sample(reports, min(n, len(reports))))
