from rest_framework.serializers import(           
    ModelSerializer,
    SerializerMethodField,
    ValidationError
)

from django.contrib.auth.models import User

from django.contrib.contenttypes.models import ContentType
from comment.models import Comment
from like.models import Like
from like.api.serializers import LikeSerializer

from profiles.api.serializers import ProfileSerializer 
from profiles.models import Profile


def create_comment_serializer(model_type="post", id=None, user=None):
    class CommentCreateSerializer(ModelSerializer):
        class Meta:
            model = Comment
            fields = [
                'id',
                'comment',
                'date_posted'
            ]
        def __init__(self,*args, **kwargs):
            self.model_type = model_type
            self.id = id
            return super(CommentCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.objects.filter(model=model_type)

            if not model_qs.exists() or model_qs.count() != 1:
                raise ValidationError("This is not a valid content type")
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(id=self.id)
            if not obj_qs.exists() or obj_qs.count() != 1:
                raise ValidationError("This is not a valid id for this content type")
            return data

        def create(self, validated_data):
            comment = validated_data.get("comment")
            if user:
                main_user = user
            else:
                main_user = User.objects.all().first()
            model_type = self.model_type
            id = self.id
            comment = Comment.objects.create_by_model_type(
                model_type, id, comment, main_user,
                )
            return comment

    return CommentCreateSerializer



class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'comment',
            'date_posted'
        ]

        read_only_fields = ['user']




class CommentDetailSerializer(ModelSerializer):
    profile = SerializerMethodField(read_only=True)
    likes =  SerializerMethodField(read_only=True)
    like_num = SerializerMethodField(read_only=True)
    class Meta:
        model = Comment
        fields = [
            'id',
            'profile',
            'comment',
            'likes',
            'like_num',
            'date_posted'
        ]
        read_only_fields = ['user']

    def get_profile(self, obj):
        request = self.context.get('request')
        qs = Profile.objects.filter(id=obj.user.id)
        res = ProfileSerializer(qs, context={"request":request} ,many=True).data
        return res

    def get_likes(self, obj):
        c_qs = Like.objects.filter_by_instance(obj)
        like = LikeSerializer(c_qs, many=True).data
        return like

    def get_like_num(self, obj):
        c_qs = Like.objects.filter_by_instance(obj).count()
        return c_qs

    
