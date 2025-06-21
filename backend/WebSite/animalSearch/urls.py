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
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path('pet_reports/avg_count', AvgReportsPerUserAPIView.as_view(), name='avg_pet_report_count'),
    path('favorites/', FavoriteReportsView.as_view(), name='user-favorites'),
    path('favorites/manage/', ManageFavoriteView.as_view(), name='manage-favorite'),
    path('favorites/manage/<int:report_id>/', ManageFavoriteView.as_view(), name='delete-favorite'),
    path('reviews/avg_rating', ReviewsStats.as_view(), name='avg_rating'),
    path('reports/total_count', ReportsCount.as_view(), name='report_count'),
    path('user/pet_reports/', UserPetReportsView.as_view(), name='user-pet-reports'),
    path('pet-reports/filters/', FilteredPetReportsView.as_view(), name='pet-reports-filter'),
]

