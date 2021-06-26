from rest_framework.serializers import SerializerMethodField, ModelSerializer

from profiles.models import Profile
from account.api.serializers import UserPublicSerializer


class ProfileSerializer(ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    # user = SerializerMethodField(read_only=True)
    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'image',
        ]

        read_only_fields = ['user']

    # def get_user(self, obj):
    #     request = self.context.get('request')
    #     # print(request)
    #     user = obj.user
    #     return UserPublicSerializer(user, read_only=True, context={'request':request}).data





class ProfileDetailSerializer(ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'image',
            'bio'
        ]
        read_only_fields = ['user']