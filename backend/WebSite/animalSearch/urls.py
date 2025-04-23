from django.urls import path
from .views import Pet_Report_List, Review_List, Pet_Report_List_Lost, Related_Breed, Pet_Report_Detail, getAllMessagesById

urlpatterns = [
    path('pet_reports/', Pet_Report_List.as_view(), name='Pet_Report_List'),
    path('pet_reports/<int:pk>/', Pet_Report_Detail.as_view(), name='report_detail'),
    path('user/2/reviews', getAllMessagesById.as_view(), name='userReviews'),
    path('pet_reports/lost', Pet_Report_List_Lost.as_view(), name='Pet_Report_List_Lost'),
    path('reviews/', Review_List.as_view(), name='Review_list'),
    path('breeds', Related_Breed.as_view(), name='DogBreeds')
]

