from django.contrib import admin
from django.urls import path

app_name = 'profile'

from .views import (
    ProfileAPIView,
    ProfileAPIDetailView
)



urlpatterns = [
    path('',ProfileAPIView.as_view(), name='profile-list'),
    path('<int:id>/',ProfileAPIDetailView.as_view(), name='detail')

]