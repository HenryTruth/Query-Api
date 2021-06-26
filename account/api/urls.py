from django.urls import path,include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token


from .views import AuthView,RegisterAPIView

app_name='account'

urlpatterns = [
    path('', AuthView.as_view()),
    path('register/', RegisterAPIView.as_view()),
    path('refresh/', refresh_jwt_token),
]
