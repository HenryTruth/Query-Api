from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.

class LikeManager(models.Manager):

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(LikeManager, self).filter(content_type=content_type, object_id= obj_id)
        return qs


    def create_by_model_type(self, model_type, id, like, user):
        model_qs = ContentType.objects.filter(model=model_type)
        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(id=id)
            if obj_qs.exists() and obj_qs.count() == 1:
                instance = self.model()
                instance.like = like
                instance.user = user
                instance.content_type = model_qs.first()
                instance.object_id = obj_qs.first().id
                instance.save()
                return instance
        return None 


class Like(models.Model):
    LIKE = 'L'

    ACTIVITY_TYPES = (
        (LIKE, 'Like'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    date_posted = models.DateTimeField(default=timezone.now)

    objects = LikeManager()


    def __str__(self):
        return str(self.like)

