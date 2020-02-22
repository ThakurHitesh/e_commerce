import datetime
import uuid
from django.db import models
from .services import now
from api.constants import CONST_NAME_LENGTH, CONST_DESC_LENGTH

class TimeStamp(models.Model):
    """
    abstact timestamp model  
    """
    created_at = models.DateTimeField(default=now, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)
    modified_at = models.DateTimeField(null=True, blank=True)
    is_deleted =  models.BooleanField(default=False)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)

    class Meta:
        abstract = True
        index_together = (('id', 'created_at', 'deleted_at'))
        ordering = ('-created_at',)

    def __str__(self):
        return "{}".format(self.id)

    @classmethod
    def get_active_objects(cls, **kwargs):
        queryset = cls.objects.filter(is_deleted = False)
        if kwargs:
            return queryset.filter(**kwargs)
        return queryset

class BaseNameModel(TimeStamp):
    """
    abstract name model
    """
    name = models.CharField(max_length=CONST_NAME_LENGTH)
    description = models.TextField(max_length=CONST_DESC_LENGTH, null=True, blank=True)

    class Meta:
        abstract = True
    
    def __str__(self):
        return "{}".format(self.name)

class BaseUniqueNameModel(TimeStamp):
    """
    abstract name model
    """
    name = models.CharField(max_length=CONST_NAME_LENGTH, unique=True)
    description = models.TextField(max_length=CONST_DESC_LENGTH, null=True, blank=True)

    class Meta:
        abstract = True
    
    def __str__(self):
        return "{}".format(self.name)