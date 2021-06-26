from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.reverse import reverse as api_reverse
from question.models import Question

from answer.models import Answer
from answer.api.serializers import AnswerSerializer, AnswerDetailSerializer

from like.models import Like
from like.api.serializers import LikeSerializer

from profiles.api.serializers import ProfileSerializer 
from profiles.models import Profile



class QuestionSerializer(ModelSerializer):
    uri= SerializerMethodField(read_only=True)
    profile = SerializerMethodField(read_only=True)
    like_num = SerializerMethodField(read_only=True)
    answer_num = SerializerMethodField(read_only=True)

    class Meta:
        model = Question
        fields = [
            'uri',
            'id',
            'profile',
            'question',
            'like_num',
            'answer_num',
            'date_posted'
        ]

        read_only_fields = ['profiles']

    def get_answer_num(self,obj):
        c_qs = Answer.objects.filter_by_instance(obj).count()
        return c_qs

    def get_uri(self,obj):
        request = self.context.get('request')
        return api_reverse("question-api:detail", kwargs={"id":obj.id}, request=request)


    def get_profile(self, obj):
        request = self.context.get('request')
        qs = Profile.objects.filter(id=obj.user.id)
        res = ProfileSerializer(qs, context={"request":request}, many=True).data
        return res

    def get_like_num(self, obj):
        c_qs = Like.objects.filter_by_instance(obj).count()
        return c_qs
        


class QuestionInlineSerializer(QuestionSerializer):
    class Meta:
        model = Question
        fields = [
            'id',
            'question',
            'date_posted'
        ]




class QuestionDetailSerializer(ModelSerializer):
    profile = SerializerMethodField(read_only=True)
    answers = SerializerMethodField(read_only=True)
    likes =  SerializerMethodField(read_only=True)
    class Meta:
        model = Question
        fields = [
            'id',
            'profile',
            'question',
            'answers',
            'likes',
            'date_posted'
        ]

        read_only_fields = ['user', 'profiles']

    def get_profile(self, obj):
        request = self.context.get('request')
        qs = Profile.objects.filter(id=obj.user.id)
        res = ProfileSerializer(qs, context={"request":request}, many=True).data
        return res

    def get_answers(self, obj):
        request = self.context.get('request')
        c_qs = Answer.objects.filter_by_instance(obj)
        answer = AnswerDetailSerializer(c_qs,context={"request":request}, many=True).data
        return answer

    def get_likes(self, obj):
        c_qs = Like.objects.filter_by_instance(obj)
        like = LikeSerializer(c_qs, many=True).data
        return like
