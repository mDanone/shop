import uuid

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django_currentuser.db.models import CurrentUserField
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


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, default=None, null=True, blank=True)


class Product(BaseInfo):
    name = models.CharField(max_length=30, default=None, null=True, blank=True)
    created_by = CurrentUserField()
    description = models.TextField()
    price = models.FloatField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=None, blank=True, null=True, related_name='products')


class ProductImage(BaseInfo):
    url = models.ImageField(upload_to='product_photo/')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)


class Cart(BaseInfo):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __repr__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)


class SubCategory(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub')

    def __repr__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
