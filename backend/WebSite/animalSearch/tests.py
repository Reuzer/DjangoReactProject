import json  
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()

class Tests(APITestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            first_name='Максим',
            middle_name='Сынович',
            last_name="Фараонов",
            password='testpass123',
            phone='1234567890'
        )
        
        # Создаем тестовые данные
        self.pet_type = Pet_type.objects.create(type_name='Собака')
        self.breed = Breed.objects.create(
            pet_type_id=self.pet_type,
            breed='Хаски'
        )
        
        # Создаем тестовое объявление с правильными полями
        self.report = Pet_Report.objects.create(
            user_id=self.user,
            title='Lost Dog',
            description='Black labrador',
            report_type='lost',
            breed_id=self.breed,
            location='Park',
            special_marks='Black collar',
            resolved=False
        )
        
        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.user)

    # 1. Тест регистрации пользователя
    def test_user_registration(self):
        url = reverse('register_user')
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'first_name': 'Олег',
            'middle_name': 'Олегович',
            'last_name': 'Олегов',
            'password': 'newpass123',
            'phone': '9876543210'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    # 2. Тест входа пользователя
    def test_user_login(self):
        url = reverse('login_user')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('tokens', response.data)

    # 3. Тест создания объявления - ИСПРАВЛЕН
    def test_create_pet_report(self):
        url = reverse('Pet_Report_List')
        # Формируем данные в формате JSON
        data = {
            'user_id': self.user.id,
            'title': 'Found Cat',
            'description': 'White cat found near mall with blue collar',
            'report_type': 'found',
            'breed_id': self.breed.id,
            'location': 'Shopping Mall',
            'special_marks': 'Blue collar',
            'resolved': False
        }
        
        # Отправляем как JSON
        response = self.client.post(url, data)
        
        # Для отладки
        if response.status_code != 201:
            print(f"Ошибка при создании объявления: {json.dumps(response.data, indent=2)}")
            
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Pet_Report.objects.count(), 2)

    # 4. Тест получения списка объявлений
    def test_get_pet_reports(self):
        url = reverse('Pet_Report_List')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) > 0)

    # 5. Тест получения одного объявления
    def test_get_single_pet_report(self):
        url = reverse('report_detail', kwargs={'pk': self.report.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Lost Dog')

    # 6. Тест обновления объявления
    def test_update_pet_report(self):
        url = reverse('report_detail', kwargs={'pk': self.report.pk})
        data = {
            'title': 'Updated Title',
            'description': 'Updated description with more details',
            'report_type': 'lost',
            'breed_id': str(self.breed.id),
            'location': 'Updated location',
            'special_marks': 'Updated marks',
            'resolved': 'true'
        }
        # Исправлен формат запроса на multipart
        response = self.client.put(url, data, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.report.refresh_from_db()
        self.assertEqual(self.report.title, 'Updated Title')
        self.assertTrue(self.report.resolved)

    # 7. Тест создания отзыва
    def test_create_review(self):
        url = reverse('Review_list')
        data = {
            'text': 'Great service!',
            'rating': 5,
            'photo': ''
        }
        response = self.client.post(url, data, format='json')
        if response.status_code != 201:
            print(f"Ошибка при создании отзыва: {response.data}")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Review.objects.count(), 1)

    # 8. Тест добавления в избранное
    def test_add_to_favorites(self):
        url = reverse('manage-favorite')
        data = {'report_id': self.report.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(FavoriteReportItem.objects.filter(report=self.report).exists())

    # 9. Тест удаления из избранного
    def test_remove_from_favorites(self):
        # Сначала добавляем в избранное
        favorite = FavoriteReports.objects.create(user_id=self.user)
        FavoriteReportItem.objects.create(favorite=favorite, report=self.report)
        
        url = reverse('delete-favorite', kwargs={'report_id': self.report.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(FavoriteReportItem.objects.filter(report=self.report).exists())

    # 10. Тест фильтрации объявлений
    def test_filter_reports(self):
        url = reverse('pet-reports-filter') + '?report_type=lost'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) > 0)
        self.assertEqual(response.data[0]['report_type'], 'lost')