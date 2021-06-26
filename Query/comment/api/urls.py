from django.contrib import admin
from django.urls import path

app_name = 'comment'

from .views import (
    CommentAPIView,
    CommentAPIDetailView
)



urlpatterns = [
    path('',CommentAPIView.as_view(), name='comment-list'),
    path('<int:id>/',CommentAPIDetailView.as_view(), name='detail')

]