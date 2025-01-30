from django.urls import path
from . import views

app_name = 'summary'

urlpatterns = [
    path('', views.upload_pdf, name='upload'),
    path('result/<int:summary_id>/', views.result, name='result'),
]