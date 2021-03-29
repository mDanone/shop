import uuid

from django.db import models


related = '%(app_label)s_%(class)s_related'


class BaseInfo(models.Model):
    """An abstract base class model that provides common fields."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    created_date = models.DateTimeField(auto_now_add=True, editable=False, blank=True)
    modified_date = models.DateTimeField(auto_now_add=True, editable=False, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        abstract = True
