from rest_framework import generics, mixins, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from account.api.permissions import IsOwnerOrReadOnly
from profiles.models import Profile
from profiles.api.serializers import ProfileSerializer, ProfileDetailSerializer
# from posts.Question.models import Question

class ProfileAPIView(mixins.CreateModelMixin,
generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # # authentication_classes = [SessionAuthentication]
    serializer_class = ProfileSerializer
    passed_id = None

    def get_queryset(self):
        request = self.request
        qs = Profile.objects.all()
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs


    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)

    
    def perform_create(self):
        return serializers.save(self.request.user)



class ProfileAPIDetailView(mixins.UpdateModelMixin,mixins.DestroyModelMixin, generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # authentication_classes = []
    serializer_class = ProfileDetailSerializer
    queryset = Profile.objects.all()
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)