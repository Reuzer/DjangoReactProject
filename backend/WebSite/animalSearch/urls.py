from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('pet_reports/', Pet_Report_List.as_view(), name='Pet_Report_List'),
    path('pet_reports/<int:pk>/', Pet_Report_Detail.as_view(), name='report_detail'),
    path('user/2/reviews', getAllMessagesById.as_view(), name='userReviews'),
    path('pet_reports/lost', Pet_Report_List_Lost.as_view(), name='Pet_Report_List_Lost'),
    path('reviews/', Review_List.as_view(), name='Review_list'),
    path('breeds/', Related_Breed.as_view(), name='DogBreeds'),
    path("register/", UserRegistrationAPIView.as_view(), name="register_user"),
    path("login/", UserLoginAPIView.as_view(), name="login_user"),
    path("logout/", UserLogoutAPIView.as_view(), name="logout_user"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh")
]

