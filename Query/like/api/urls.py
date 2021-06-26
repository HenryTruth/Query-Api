from django.contrib import admin
from django.urls import path

app_name = 'like'

from .views import (
    LikeAPIView,
    LikeAPIDetailView
)



urlpatterns = [
    path('',LikeAPIView.as_view(), name='like-list'),
    path('<int:id>/',LikeAPIDetailView.as_view(), name='detail')

]