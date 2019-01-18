from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone

from locations.models import Country, City


class Status(models.Model):
    # name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    def __str__(self):
        return self.slug

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



class Speciality(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    slug = models.SlugField(max_length=100,blank=True,null=True)
    def __str__(self):
        return f'{self.name}'


class Language(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return f'{self.name}'

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='default.png',upload_to='profile_pics')
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE,blank=True,null=True)
    bio = models.TextField(blank=True,null=True)
    skills = models.ManyToManyField('Skills',blank=True,related_name='profiles')
    facebook = models.CharField(max_length=200,blank=True,null=True)
    linkedin = models.CharField(max_length=200,blank=True,null=True)
    country = models.ForeignKey(Country,on_delete=models.CASCADE,blank=True,null=True)
    city = models.ForeignKey(City,on_delete=models.CASCADE,blank=True,null=True)
    status = models.ForeignKey(Status,on_delete=models.CASCADE,blank=True,null=True)
    date_registered = models.DateTimeField(default=timezone.now)
    language = models.ForeignKey(Language,on_delete=models.CASCADE,default=2)
    def __str__(self):
        return f'{self.user.username}'

    def save(self,**kwargs):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Skills(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name

# Chat and messages here
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

#Dialogs

class Chat(models.Model):
    DIALOG = 'D'
    CHAT = 'C'
    CHAT_TYPE_CHOICES = (
        (DIALOG, _('Dialog')),
        (CHAT, _('Chat'))
    )

    type = models.CharField(
        _('Тип'),
        max_length=1,
        choices=CHAT_TYPE_CHOICES,
        default=DIALOG
    )
    members = models.ManyToManyField(User, verbose_name=_("Участник"))


    def get_absolute_url(self):
        return 'messages', (), {'chat_id': self.pk}


class Message(models.Model):
    chat = models.ForeignKey(Chat, verbose_name=_("Чат"),on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name=_("Пользователь"),on_delete=models.CASCADE)
    message = models.TextField(_("Сообщение"))
    pub_date = models.DateTimeField(_('Дата сообщения'), default=timezone.now)
    is_readed = models.BooleanField(_('Прочитано'), default=False)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.message

