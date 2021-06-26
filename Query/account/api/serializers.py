import datetime

# from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.serializers import ModelSerializer, ValidationError, SerializerMethodField, CharField
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings

from rest_framework.reverse import reverse as api_reverse

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_reponse_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

expire_delta = api_settings.JWT_REFRESH_EXPIRATION_DELTA


class UserPublicSerializer(ModelSerializer):
    uri = SerializerMethodField(read_only=True)
    class Meta:
        model = User 
        fields = [
            'id',
            'username',
            'uri'
        ]

        read_only_fields = ['username']

    def get_uri(self, obj):
        request = self.context.get('request')
        print(request)
        return api_reverse("api-user:detail", kwargs={"username":obj.username}, request=request)


class UserRegisterSerializer(ModelSerializer):
    password = CharField(style={'input_type':'password'}, write_only=True)
    token = SerializerMethodField(read_only=True)
    expires = SerializerMethodField(read_only=True)
    message = SerializerMethodField(read_only=True)
    status_code = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'token',
            'expires',
            'message',
            'status_code'
        ]

        extra_kwargs = {'password': {'write_only':True}, 'email': {'required':True}}

    def get_status_code(self, obj):
        data = {'detail':'Successfully deleted', 'status':200}
        return data

    def get_message(self, obj):
        return 'Thank you for registering. Please verify your email before continuing'

    def get_token(self, obj):
        user = obj
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def validate_email(self,value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise ValidationError("User with this email already exists")
        return value


    def validate_username(self, value):
        qs = User.objects.filter(username__iexact=value)
        if qs.exists():
            raise ValidationError("User with this username already exists")
        return value

 
    def create(self, validated_data):
        user_obj = User(
            username=validated_data.get('username'),
            email=validated_data.get('email')
        )
        user_obj.set_password(validated_data.get('password'))
        user_obj.save()
        return user_obj


    def get_expires(self, obj):
        return timezone.now() + expire_delta - datetime.timedelta(seconds=200)


