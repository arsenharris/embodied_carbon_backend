from django.urls import path
from . import views

urlpatterns = [
    path('calculations/', views.EmbodiedCarbonList.as_view()),
    path('materials/a1/coeffs/', views.MaterialsCoefficients.as_view()),
    path('materials/a1/presets/', views.MaterialsPresets.as_view()),
]