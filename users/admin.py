from django.contrib import admin
from .models import Profile, Speciality, Skills, Country, City, Status, Language, Chat, Message

# Register your models here.

admin.site.register(Profile)
admin.site.register(Speciality)
admin.site.register(Skills)
# admin.site.register(Country)
# admin.site.register(City)
admin.site.register(Status)
admin.site.register(Language)
admin.site.register(Chat)
admin.site.register(Message)
