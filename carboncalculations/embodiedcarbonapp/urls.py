from django.urls import path
from . import views

urlpatterns = [
    path('calculations/', views.EmbodiedCarbonList.as_view()),
    path('calculations/export/pdf/', views.EmbodiedCarbonExportPDF.as_view()),
    path('materials/a1/coeffs/', views.MaterialsCoefficients.as_view()),
    path('materials/a1/presets/', views.MaterialsPresets.as_view()),
    path('materials/a3/electricity_factors/', views.MaterialsElectricityFactors.as_view()),
]