from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.ProjectsList.as_view()),
    path('calculations/', views.EmbodiedCarbonList.as_view()),
    path('calculations/<int:id>/', views.EmbodiedCarbonList.as_view()),
    path('calculations/export/pdf/', views.EmbodiedCarbonExportPDF.as_view()),
    path('materials/a1/coeffs/', views.MaterialsCoefficients.as_view()),
    path('materials/a1/presets/', views.MaterialsPresets.as_view()),
    path('product/requirements/', views.ProductRequirements.as_view()),
    path('compare/', views.CompareProducts.as_view()),
    path('projects/<int:id>/', views.ProjectDetail.as_view()),
    path('projects/<int:project_id>/calculations/', views.ProjectCalculationsList.as_view()),
    path('projects/<int:project_id>/calculations/<int:calc_id>/', views.ProjectCalculationDetail.as_view()),
]