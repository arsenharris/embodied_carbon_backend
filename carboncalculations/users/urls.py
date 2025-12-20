from django.urls import path
from . import views 

urlpatterns = [
    path ('users/' , views.CustomUserList.as_view()), 
    path ('users/<int:pk>/', views.CustomUserDetail.as_view()),
    path('api-auth-token/', views.CustomAuthToken.as_view()),

]