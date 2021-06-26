from rest_framework.serializers import(           
    ModelSerializer,
    SerializerMethodField,
    ValidationError
)

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from like.models import Like

def create_like_serializer(model_type="post", id=None, user=None):
    class LikeCreateSerializer(ModelSerializer):
        class Meta:
            model = Like
            fields = [
                'id',
                'like',
                'date_posted'
            ]
        def __init__(self,*args, **kwargs):
            self.model_type = model_type
            self.id = id
            return super(LikeCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.objects.filter(model=model_type)

            if not model_qs.exists() or model_qs.count() != 1:
                raise ValidationError("This is not a valid content type")
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(id=self.id)
            if not obj_qs.exists() or obj_qs.count() != 1:
                raise ValidationError("this is not a valid id for this content type")
            return data

        def create(self, validated_data):
            like = validated_data.get("like")
            if user:
                main_user = user
            else:
                main_user = User.objects.all().first()
            model_type = self.model_type
            id = self.id
            like = Like.objects.create_by_model_type(
                model_type, id, like, main_user,
                )
            return like

    return LikeCreateSerializer



class LikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = [
            'id',
            'user',
            'like'
        ]

        read_only_fields = ['user']



class LikeDetailSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = [
            'id',
            'user',
            'like'
        ]

        read_only_fields = ['user']


    
