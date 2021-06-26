from django.urls import path, include
from django.contrib import admin


from .views import UserDetailAPIView, UserQuestionAPIView

app_name='user'

urlpatterns = [
    path('<username>/', UserDetailAPIView.as_view(), name='detail'),
    path('<username>/questions/', UserQuestionAPIView.as_view(), name='question-list'),

]