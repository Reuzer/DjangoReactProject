import random
from django.core.management.base import BaseCommand
from faker import Faker
from animalSearch.models import (
    User, Blog, Message, Review, Notification,
    Pet_type, Breed, Pet_Report, FavoriteReports, FavoriteReportItem
)

fake = Faker('ru_RU')  # Для русскоязычных данных

class Command(BaseCommand):
    help = 'Populates the database with fake data'

    def handle(self, *args, **options):
        self.stdout.write('Creating fake data...')
        
        # Очистка старых данных (осторожно!)
        # User.objects.all().delete()
        
        self.create_users()
        self.create_blogs()
        self.create_messages()
        self.create_reviews()
        self.create_notifications()
        self.create_pet_types_and_breeds()
        self.create_pet_reports()
        self.create_favorites()
        
        self.stdout.write(self.style.SUCCESS('Successfully populated the database!'))

    def truncate_text(self, text, max_length=50):
        """Обрезает текст до max_length символов"""
        return text[:max_length] if text else ""

    def create_users(self, count=10):
        for _ in range(count):
            User.objects.create(
                username=fake.user_name()[:30],
                first_name=fake.first_name()[:30],
                last_name=fake.last_name()[:30],
                middle_name=fake.middle_name()[:30],
                email=fake.email(),
                phone=fake.phone_number()[:30],
                photo=fake.image_url(),
                password='testpass123'  # Простой пароль для теста
            )
        self.stdout.write(f'Created {count} users')

    def create_blogs(self, count=15):
        users = list(User.objects.all())
        for _ in range(count):
            Blog.objects.create(
                picture=fake.image_url(),
                title=self.truncate_text(fake.sentence(nb_words=4)),
                description=self.truncate_text(fake.text(max_nb_chars=200)),
                short_desc=self.truncate_text(fake.sentence(nb_words=6))
            )
        self.stdout.write(f'Created {count} blog posts')

    def create_messages(self, count=20):
        users = list(User.objects.all())
        for _ in range(count):
            sender, receiver = random.sample(users, 2)
            Message.objects.create(
                sender_id=sender,
                receiver_id=receiver,
                text=self.truncate_text(fake.text(max_nb_chars=200))
            )
        self.stdout.write(f'Created {count} messages')

    def create_reviews(self, count=15):
        users = list(User.objects.all())
        for _ in range(count):
            Review.objects.create(
                user_id=random.choice(users),
                photo=fake.image_url(),
                text=self.truncate_text(fake.text(max_nb_chars=200)),
                rating=random.randint(1, 5))
        self.stdout.write(f'Created {count} reviews')

    def create_notifications(self, count=20):
        users = list(User.objects.all())
        for _ in range(count):
            Notification.objects.create(
                user_id=random.choice(users),
                text=self.truncate_text(fake.sentence(nb_words=10)),
                read=fake.boolean())
        self.stdout.write(f'Created {count} notifications')

    def create_pet_types_and_breeds(self):
        pet_types = ['Собака', 'Кошка', 'Попугай', 'Хомяк', 'Черепаха']
        breeds_data = {
            'Собака': ['Лабрадор', 'Овчарка', 'Такса', 'Бульдог'],
            'Кошка': ['Сиамская', 'Персидская', 'Сфинкс', 'Британская'],
            'Попугай': ['Волнистый', 'Какаду', 'Ара', 'Неразлучник'],
            'Хомяк': ['Сирийский', 'Джунгарский', 'Роборовского'],
            'Черепаха': ['Красноухая', 'Среднеазиатская', 'Морская']
        }
        
        for type_name in pet_types:
            pet_type = Pet_type.objects.create(type_name=type_name)
            for breed_name in breeds_data[type_name]:
                Breed.objects.create(pet_type_id=pet_type, breed=breed_name)
        
        self.stdout.write('Created pet types and breeds')

    def create_pet_reports(self, count=30):
        users = list(User.objects.all())
        breeds = list(Breed.objects.all())
        report_types = ['lost', 'found']
        
        for _ in range(count):
            Pet_Report.objects.create(
                user_id=random.choice(users),
                breed_id=random.choice(breeds),
                title=self.truncate_text(fake.sentence(nb_words=3)),
                resolved=fake.boolean(),
                special_marks=self.truncate_text(fake.sentence(nb_words=5)),
                picture=fake.image_url(),
                report_type=random.choice(report_types),
                location=self.truncate_text(fake.city()),
                description=self.truncate_text(fake.text(max_nb_chars=200)))
        self.stdout.write(f'Created {count} pet reports')

    def create_favorites(self, count=10):
        users = list(User.objects.all())
        reports = list(Pet_Report.objects.all())
        
        for user in users[:count]:  # Для первых N пользователей
            fav, created = FavoriteReports.objects.get_or_create(user_id=user)
            selected_reports = random.sample(reports, min(5, len(reports)))
            for report in selected_reports:
                FavoriteReportItem.objects.create(
                    favorite=fav,
                    report=report)
        
        self.stdout.write(f'Created favorites for {count} users')