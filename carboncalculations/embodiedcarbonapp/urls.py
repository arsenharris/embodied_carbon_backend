from django.urls import path
from . import views

urlpatterns = [
    path('calculations/', views.EmbodiedCarbonList.as_view()),
]