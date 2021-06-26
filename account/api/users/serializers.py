import datetime
from django.contrib.auth.models import User
from django.utils import timezone

from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.reverse import reverse as api_reverse

from question.api.serializers import QuestionInlineSerializer

class UserDetailSerializer(ModelSerializer):
    uri = SerializerMethodField(read_only=True)
    question = SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'uri',
            'id',
            'username',
            'question'
        ]

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse("api-user:detail",kwargs={"username":obj.username}, request=request)

    def get_question(self,obj):
        request = self.context.get('request')
        limit = 10
        if request:
            limit_query = request.GET.get('limit')
            try:
                limit = int(limit_query)
            except:
                pass

        qs = obj.question_set.all().order_by("-date_posted")
        data = {
            'uri':self.get_uri(obj) + "questions/",
            'recent':QuestionInlineSerializer(qs[:limit], context={'request':request},many=True).data
        }
        return data