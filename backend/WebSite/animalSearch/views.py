from rest_framework.views import APIView
from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from django.db.models import Avg, Count, Prefetch
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import ValidationError
from .permissions import IsAdmin, IsOwnerOrAdminOrReadOnly, IsOwner
from rest_framework.parsers import MultiPartParser, FormParser
from .filters import PetReportFilter
from typing import Optional, Dict, Any, List
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from rest_framework.request import Request


class Pet_Report_List(APIView):
    """API для работы со списком объявлений о животных."""
    
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request: Request) -> Response:
        """
        Получение списка всех объявлений о животных.
        
        Returns:
            Response: Список объявлений в формате JSON или 404 если нет объявлений
        """
        if Pet_Report.objects.exists():
            pet_reports = Pet_Report.objects.order_by('public_date')
            serializer = PetReportReadSerializer(pet_reports, many=True)
            return Response(serializer.data)
        else: 
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request: Request) -> Response:
        """
        Создание нового объявления о животном.
        
        Args:
            request: Запрос с данными нового объявления
            
        Returns:
            Response: Созданное объявление или ошибки валидации
        """
        serializer = PetReportWriteSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class Pet_Report_Detail(APIView):
    """API для работы с конкретным объявлением о животном."""
    
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk: int) -> Pet_Report:
        """
        Получение объекта объявления по ID с проверкой прав доступа.
        
        Args:
            pk: ID объявления
            
        Returns:
            Pet_Report: Объект объявления
            
        Raises:
            Http404: Если объявление не найдено
        """
        obj = get_object_or_404(Pet_Report, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request: Request, pk: int) -> Response:
        """
        Получение детальной информации об объявлении.
        
        Args:
            request: Запрос
            pk: ID объявления
            
        Returns:
            Response: Детали объявления в формате JSON
        """
        pet_report = self.get_object(pk)
        serializer = PetReportReadSerializer(pet_report)
        return Response(serializer.data)

    def put(self, request: Request, pk: int) -> Response:
        """
        Обновление информации об объявлении.
        
        Args:
            request: Запрос с новыми данными
            pk: ID объявления
            
        Returns:
            Response: Обновленное объявление или ошибки валидации
        """
        pet_report = self.get_object(pk)
        serializer = PetReportWriteSerializer(
            pet_report,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int) -> Response:
        """
        Удаление объявления.
        
        Args:
            request: Запрос
            pk: ID объявления
            
        Returns:
            Response: Пустой ответ с кодом 204 при успешном удалении
        """
        pet_report = self.get_object(pk)
        pet_report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Pet_Report_List_Lost(APIView):
    """API для получения списка потерянных животных."""
    
    def get(self, request: Request) -> Response:
        """
        Получение списка потерянных животных.
        
        Returns:
            Response: Список потерянных животных в формате JSON
        """
        pets = Pet_Report.objects.lost_pets().order_by('id')
        serializer = PetReportReadSerializer(pets, many=True)
        return Response(serializer.data)
    

class Review_List(APIView):
    """API для работы с отзывами."""
    
    def get(self, request: Request) -> Response:
        """
        Получение списка всех отзывов.
        
        Returns:
            Response: Список отзывов в формате JSON
        """
        reviews = Review.objects.all()
        serializer = ReviewReadSerializer(reviews, many=True)
        return Response(serializer.data)
    
    @permission_classes([IsAuthenticated])
    def post(self, request: Request) -> Response:
        """
        Создание нового отзыва.
        
        Args:
            request: Запрос с данными отзыва
            
        Returns:
            Response: Созданный отзыв или ошибки валидации
        """
        serializer = ReviewWriteSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class Related_Breed(APIView):
    """API для работы с породами животных."""
    
    permission_classes = [AllowAny]
    
    def get(self, request: Request) -> Response:
        """
        Получение списка всех пород животных.
        
        Returns:
            Response: Список пород в формате JSON
        """
        breeds = Breed.objects.all()
        serializer = BreedSerializer(breeds, many=True)
        return Response(serializer.data)


class getAllMessagesById(APIView):
    """API для получения сообщений конкретного пользователя (тестовый)."""
    
    def get(self, request: Request) -> Response:
        """
        Получение всех сообщений пользователя с ID=2.
        
        Returns:
            Response: Список сообщений в формате JSON
        """
        user = User.objects.get(id=2)
        reviews = user.reviews.all()
        serializer = ReviewReadSerializer(reviews, many=True)
        return Response(serializer.data)


class UserRegistrationAPIView(APIView):
    """API для регистрации новых пользователей."""
    
    permission_classes = [AllowAny]

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Регистрация нового пользователя.
        
        Args:
            request: Запрос с данными пользователя
            
        Returns:
            Response: Данные пользователя и токены или ошибки валидации
        """
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token),
                          "access": str(token.access_token)}
        return Response(data, status.HTTP_201_CREATED, content_type='application/json')
    

class UserLoginAPIView(APIView):
    """API для аутентификации пользователей."""
    
    permission_classes = [AllowAny]
    
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Аутентификация пользователя.
        
        Args:
            request: Запрос с учетными данными
            
        Returns:
            Response: Данные пользователя и токены или ошибка аутентификации
        """
        try:
            auth_serializer = UserLoginSerializer(data=request.data, context={'request': request})
            auth_serializer.is_valid(raise_exception=True)
            
            user = auth_serializer.validated_data['user']
            read_serializer = UserReadSerializer(user)
            
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': read_serializer.data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK, content_type='application/json')
            
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({'error': 'Ошибка сервера'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class UserLogoutAPIView(APIView):
    """API для выхода пользователя из системы."""
    
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Выход пользователя (инвалидация refresh токена).
        
        Args:
            request: Запрос с refresh токеном
            
        Returns:
            Response: Статус операции
        """
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AvgReportsPerUserAPIView(APIView):
    """API для получения статистики по объявлениям."""
   
    def get(self, request: Request) -> Response:
        """
        Получение среднего количества объявлений на пользователя.
        
        Returns:
            Response: Среднее количество объявлений
        """
        user_reports = (
            Pet_Report.objects.values('user_id')
            .annotate(count=Count('id'))
            .exclude(count=0)
        )
        avg = user_reports.aggregate(avg=Avg('count'))
        return Response({'avg_reports_per_user': avg['avg']})
    

class FavoriteReportsView(APIView):
    """API для работы с избранными объявлениями."""
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request: Request) -> Response:
        """
        Получение списка избранных объявлений пользователя.
        
        Args:
            request: Запрос
            
        Returns:
            Response: Список избранных объявлений
        """
        favorite = get_object_or_404(
            FavoriteReports.objects.prefetch_related(
                Prefetch(
                    'favoritereportitem_set',
                    queryset=FavoriteReportItem.objects.select_related('report'),
                    to_attr='prefetched_items'
                )
            ),
            user_id=request.user
        )
        
        reports_data = [
            {
                'id': item.report.id,
                'title': item.report.title,
                'added_at': item.added_at,
            }
            for item in getattr(favorite, 'prefetched_items', [])
        ]
        
        return Response({
            'user_id': request.user.id,
            'reports': reports_data
        })


class ManageFavoriteView(APIView):
    """API для управления избранными объявлениями."""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request: Request) -> Response:
        """
        Добавление объявления в избранное.
        
        Args:
            request: Запрос с ID объявления
            
        Returns:
            Response: Статус операции
        """
        report_id = request.data.get('report_id')
        if not report_id:
            return Response(
                {'error': 'report_id обязателен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        report = get_object_or_404(Pet_Report, id=report_id)
        favorite, _ = FavoriteReports.objects.get_or_create(user_id=request.user)
        
        if FavoriteReportItem.objects.filter(favorite=favorite, report=report).exists():
            return Response(
                {'error': 'Объявление уже в избранном'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        FavoriteReportItem.objects.create(favorite=favorite, report=report)
        
        return Response(
            {'message': 'Объявление добавлено в избранное'},
            status=status.HTTP_201_CREATED
        )
    
    def delete(self, request: Request, report_id: int) -> Response:
        """
        Удаление объявления из избранного.
        
        Args:
            request: Запрос
            report_id: ID объявления
            
        Returns:
            Response: Статус операции
        """
        favorite = get_object_or_404(FavoriteReports, user_id=request.user)
        
        deleted, _ = FavoriteReportItem.objects.filter(
            favorite=favorite,
            report_id=report_id
        ).delete()
        
        if not deleted:
            return Response(
                {'error': 'Объявление не найдено в избранном'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        return Response(
            {'message': 'Объявление удалено из избранного'},
            status=status.HTTP_204_NO_CONTENT
        )
    

class BlogView(APIView):
    """API для работы с блогами."""
    
    def get(self, request: Request) -> Response:
        """
        Получение списка всех блогов.
        
        Returns:
            Response: Список блогов в формате JSON
        """
        blogs = Blog.objects.all()
        serializer = BlogReadSerializer(blogs, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """
        Создание нового блога.
        
        Args:
            request: Запрос с данными блога
            
        Returns:
            Response: Созданный блог или ошибки валидации
        """
        serializer = BlogWriteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewsStats(APIView):
    """API для получения статистики по отзывам."""
    
    def get(self, request: Request) -> Response:
        """
        Получение средней оценки отзывов.
        
        Returns:
            Response: Средняя оценка
        """
        avg_rating = Review.objects.aggregate(avg_rating=Avg('rating'))
        return Response(avg_rating)


class ReportsCount(APIView):
    """API для получения статистики по объявлениям."""
    
    def get(self, request: Request) -> Response:
        """
        Получение общего количества объявлений.
        
        Returns:
            Response: Количество объявлений
        """
        reports_count = Pet_Report.objects.aggregate(reports_count=Count('id'))
        return Response(reports_count)


class UserPetReportsView(APIView):
    """API для получения объявлений текущего пользователя."""
    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        """
        Получение всех объявлений текущего пользователя.
        
        Args:
            request: Запрос
            
        Returns:
            Response: Список объявлений пользователя
        """
        user = request.user
        pet_reports = user.user_pet_reports.select_related(
            'breed_id__pet_type_id'
        ).order_by('-public_date')
        
        serializer = PetReportReadSerializer(pet_reports, many=True)
        return Response(serializer.data)
    

class FilteredPetReportsView(APIView):
    """API для получения отфильтрованных объявлений."""
    
    def get(self, request: Request) -> Response:
        """
        Получение объявлений с применением фильтров.
        
        Args:
            request: Запрос с параметрами фильтрации
            
        Returns:
            Response: Отфильтрованный список объявлений
        """
        queryset = Pet_Report.objects.all()
        filter_backends = (filters.DjangoFilterBackend,)
        filterset_class = PetReportFilter
        
        filtered_queryset = PetReportFilter(request.GET, queryset=queryset).qs
        
        filtered_queryset = filtered_queryset.order_by('-public_date')
        
        serializer = PetReportReadSerializer(filtered_queryset, many=True)
        return Response(serializer.data)