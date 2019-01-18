from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models

from django.urls import reverse
from django.utils import timezone

from comentz.models import Comment
from locations.models import Country, City
from users import models as usr_models


# class Country(models.Model):
#     name = models.CharField(max_length=30)
#
#     def __str__(self):
#         return self.name
#
# class City(models.Model):
#     country = models.ForeignKey(Country, on_delete=models.CASCADE)
#     name = models.CharField(max_length=30)
#
#     def __str__(self):
#         return self.name


class Deal(models.Model):
    title = models.CharField(max_length=100,verbose_name='Назва проекту')
    description = models.TextField(verbose_name='Опис')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    speciality = models.ManyToManyField(usr_models.Speciality,related_name='deals',blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('deal-detail',kwargs={'id': self.id})

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type



