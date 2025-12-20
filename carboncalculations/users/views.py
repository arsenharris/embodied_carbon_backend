from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class CustomUserList(APIView):
    def get(self,request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response (serializer.data)
    
    def post (self,request):
        serializer=CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status= status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST) 
    def delete (self, request, pk):
        user = self.get_object(pk)
        if request.user !=user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomUserDetail(APIView):
    def get_object(self,pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        user= self.get_object(pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

class CustomAuthToken(ObtainAuthToken):
    def post(self,request, *args, **kwargs): 
        serializer = self.serializer_class(
            data=request.data,
            context = {'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user =serializer._validated_data['user']

        token, _ =Token.objects.get_or_create(user=user)

        return Response(
            {
                'token': token.key,
                'user_id':user.id,
                'email': user.email
            }
        )