from django.contrib import admin
from django.urls import path

app_name = 'answer'

from .views import (
    AnswerAPIView,
    AnswerAPIDetailView
)



urlpatterns = [
    path('',AnswerAPIView.as_view(), name='answer-list'),
    path('<int:id>/',AnswerAPIDetailView.as_view(), name='detail')

]