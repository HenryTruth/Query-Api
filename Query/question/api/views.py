from rest_framework import generics, mixins, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from account.api.permissions import IsOwnerOrReadOnly
from question.models import Question
from question.api.serializers import QuestionSerializer, QuestionDetailSerializer
from rest_framework import status

class QuestionAPIView(mixins.CreateModelMixin,
generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = QuestionSerializer
    passed_id = None
    search_fields = ['question']
    ordering_fields = ['date_posted']
    queryset = Question.objects.all()


    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    



class QuestionAPIDetailView(mixins.DestroyModelMixin, generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = QuestionDetailSerializer
    queryset = Question.objects.all()
    lookup_field = 'id'


    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            data = {'detail':'Successfully deleted', 'status':200}
            self.perform_destroy(instance)
        except:
            pass
        return Response(data)