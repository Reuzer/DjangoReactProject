from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework import status
from django.db.models import Avg
from .models import Pet_Report, Blog, Pet_type, Review, Breed, User
from .serializers import Pet_Report_Serializer, Blog_Serializer, Pet_type_Serializer, Breed_Serializer, Review_Serializer, UserSerializer


class Pet_Report_List(APIView):

    def get(self, request):
        pets = Pet_Report.objects.order_by('public_date')
        serializer = Pet_Report_Serializer(pets, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = Pet_Report_Serializer(data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class Pet_Report_Detail(RetrieveAPIView):
    queryset = Pet_Report.objects.all()
    serializer_class = Pet_Report_Serializer



class Pet_Report_List_Lost(APIView):

    def get(self, request):
        pets = Pet_Report.objects.lost_pets().order_by('')
        serializer = Pet_Report_Serializer(pets, many=True)
        return Response(serializer.data)
    

class Review_List(APIView):

    def get(self, request):
        avg_rating = Review.objects.aggregate(Avg('rating'))
        reviews = Review.objects.all()
        serializer = Review_Serializer(reviews, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = Review_Serializer(data = request.data)

        if (serializer.is_valid()):
            serializer.save
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class Related_Breed(APIView):

    def get(self, request):
        breeds = Breed.objects.filter(pet_type = 1)
        serializer = Breed_Serializer(breeds, many=True)
        return Response(serializer.data)


class getAllMessagesById(APIView):
    def get(self, request):
        user = User.objects.get(id=2)
        reviews = user.reviews.all()
        serializer = Review_Serializer(reviews, many=True)
        return Response(serializer.data)


