from rest_framework import generics, mixins, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from account.api.permissions import IsOwnerOrReadOnly
from like.models import Like
from like.api.serializers import LikeSerializer, LikeDetailSerializer, create_like_serializer
# from posts.answer.models import answer

class LikeAPIView(mixins.CreateModelMixin,
generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # authentication_classes = [SessionAuthentication]
    serializer_class = LikeSerializer
    passed_id = None

    def get_queryset(self):
        request = self.request
        qs = Like.objects.all()
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs


    def get_serializer_class(self):
        model_type = self.request.GET.get("type")
        id = self.request.GET.get("id")
        return create_like_serializer(
            model_type=model_type,
            id=id,
            user=self.request.user
        )


    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



class LikeAPIDetailView(mixins.UpdateModelMixin,mixins.DestroyModelMixin, generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # authentication_classes = []
    serializer_class = LikeDetailSerializer
    queryset = Like.objects.all()
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)