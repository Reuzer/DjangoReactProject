from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from django.db.models import Avg
from .models import Pet_Report, Blog, Pet_type, Review, Breed, User
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken



class Pet_Report_List(APIView):

    def get(self, request):
        pet_reports = Pet_Report.objects.order_by('public_date')
        serializer = PetReportReadSerializer(pet_reports, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PetReportWriteSerializer(data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class Pet_Report_Detail(APIView):
    
    def get(self, request, pk):
        pet_report = Pet_Report.objects.get(pk=pk)
        serializer = PetReportReadSerializer(pet_report)
        return Response(serializer.data)
        
    
    def put(self, request, pk):
        pet_report = Pet_Report.objects.get(pk=pk)
        serializer = PetReportWriteSerializer(pet_report, data = request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        pet_report = Pet_Report.objects.get(pk=pk)
        pet_report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        





class Pet_Report_List_Lost(APIView):

    def get(self, request):
        pets = Pet_Report.objects.lost_pets().order_by('id')
        serializer = PetReportReadSerializer(pets, many=True)
        return Response(serializer.data)
    

class Review_List(APIView):

    def get(self, request):
        avg_rating = Review.objects.aggregate(Avg('rating'))
        reviews = Review.objects.all()
        serializer = ReviewReadSerializer(reviews, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ReviewWriteSerializer(data = request.data)

        if (serializer.is_valid()):
            serializer.save
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class Related_Breed(APIView):

    def get(self, request):
        breeds = Breed.objects.all()
        serializer = BreedSerializer(breeds, many=True)
        return Response(serializer.data)


class getAllMessagesById(APIView):
    def get(self, request):
        user = User.objects.get(id=2)
        reviews = user.reviews.all()
        serializer = ReviewReadSerializer(reviews, many=True)
        return Response(serializer.data)


class UserRegistrationAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token),
                          "access": str(token.access_token)}
        return Response(data, status.HTTP_201_CREATED)
    
class UserLoginAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        auth_serializer = UserLoginSerializer(data = request.data)
        auth_serializer.is_valid(raise_exception=True)
        user = auth_serializer.validated_data
        read_serializer = UserReadSerializer(user)
        token = RefreshToken.for_user(user)
        data = read_serializer.data
        data["tokens"] = {"refresh": str(token),
                          "access": str(token.access_token)}
        return Response(data, status.HTTP_200_OK)
    

class UserLogoutAPIView(APIView):
    permission_classes = (IsAuthenticated)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status = status.HTTP_400_BAD_REQUEST)







