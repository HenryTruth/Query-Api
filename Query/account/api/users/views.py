from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, permissions
from question.api.serializers import QuestionInlineSerializer
from question.models import Question
from .serializers import UserDetailSerializer
from account.api.permissions import AnonPermissionOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly



class UserDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserDetailSerializer
    lookup_field = 'username'


    def get_serializer_context(self):
        return {'request':self.request}


class UserQuestionAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = QuestionInlineSerializer

    def get_queryset(self, *args, **kwargs):
        username = self.kwargs.get("username", None)
        if username is None:
            return Question.objects.none()
        return Question.objects.filter(user__username=username)