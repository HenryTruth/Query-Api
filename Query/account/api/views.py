from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from .serializers import UserRegisterSerializer
from .permissions import AnonPermissionOnly

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_reponse_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER



class AuthView(APIView):
    permission_classes = [AnonPermissionOnly]

    def post(self, request, *args,  **kwargs):
        if request.user.is_authenticated:
            return Response({'detail':'You are already authenticated'}, status=400)
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        qs = User.objects.filter(
            Q(username__iexact=username)|
            Q(email__iexact=username)
        ).distinct()
        if qs.count() == 1:
            user_obj = qs.first()
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            response = jwt_reponse_payload_handler(token, user, request=request)
            data = {'response':response, 'detail':'Successfully logged in', 'status_code':200}
            return Response(data)
        return Response({'detail':'Invalid credentials'}, status=401)


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AnonPermissionOnly]

    # def get_serializer_context(self, *args, **kwargs):
    #     return {'request':self.request}