from django.urls import path
from . import views

app_name = 'image_processing'

urlpatterns = [
    path('', views.home, name='home'),
    path('api/process-image/', views.process_image_api, name='process_image_api'),
    path('api/extract-attributes/', views.extract_attributes_api, name='extract_attributes_api'),
    path('api/history/', views.get_processing_history, name='get_processing_history'),
]
