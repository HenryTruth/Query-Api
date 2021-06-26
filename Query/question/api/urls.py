from django.contrib import admin
from django.urls import path

app_name = 'question'

from .views import (
    QuestionAPIView,
    QuestionAPIDetailView
)



urlpatterns = [
    path('',QuestionAPIView.as_view(), name='question-list'),
    path('<int:id>/',QuestionAPIDetailView.as_view(), name='detail')

]