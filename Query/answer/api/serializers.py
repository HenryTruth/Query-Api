from rest_framework.serializers import(           
    ModelSerializer,
    SerializerMethodField,
    ValidationError
)
from rest_framework.reverse import reverse as api_reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from comment.api.serializers import CommentSerializer, CommentDetailSerializer
from question.models import Question
from answer.models import Answer
from comment.models import Comment
from like.models import Like
from like.api.serializers import LikeSerializer

from profiles.api.serializers import ProfileSerializer 
from profiles.models import Profile

def create_answer_serializer(model_type="post", id=None, user=None):
    class AnswerCreateSerializer(ModelSerializer):
        class Meta:
            model = Answer
            fields = [
                'id',
                'answer',
                'date_posted'
            ]
        def __init__(self,*args, **kwargs):
            self.model_type = model_type
            self.id = id
            return super(AnswerCreateSerializer, self).__init__(*args, **kwargs)

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
            answer = validated_data.get("answer")
            if user:
                main_user = user
            else:
                main_user = User.objects.all().first()
            model_type = self.model_type
            id = self.id
            answer = Answer.objects.create_by_model_type(
                model_type, id, answer, main_user,
                )
            return answer

    return AnswerCreateSerializer



class AnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'id',
            'user',
            'answer',
            'date_posted'
        ]

        read_only_fields = ['user']




class AnswerDetailSerializer(ModelSerializer):
    profile = SerializerMethodField(read_only=True)
    comments = SerializerMethodField(read_only=True)
    likes =  SerializerMethodField(read_only=True)
    like_num = SerializerMethodField(read_only=True)
    comment_num = SerializerMethodField(read_only=True)
    class Meta:
        model = Answer
        fields = [
            'id',
            'answer',
            'profile',
            'comments',
            'likes',
            'like_num',
            'comment_num',
            'date_posted'

        ]

        read_only_fields = ['user']

    def get_comment_num(self, obj):
        c_qs = Comment.objects.filter_by_instance(obj).count()
        return c_qs

    def get_like_num(self, obj):
        c_qs = Like.objects.filter_by_instance(obj).count()
        return c_qs

    def get_profile(self, obj):
        request = self.context.get('request')
        qs = Profile.objects.filter(id=obj.user.id)
        res = ProfileSerializer(qs, context={"request":request}, many=True).data
        return res

    def get_comments(self, obj):
        request = self.context.get('request')
        c_qs = Comment.objects.filter_by_instance(obj)
        comment = CommentDetailSerializer(c_qs,context={"request":request}, many=True).data
        return comment

    def get_likes(self, obj):
        c_qs = Like.objects.filter_by_instance(obj)
        like = LikeSerializer(c_qs, many=True).data
        return like


    
