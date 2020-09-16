from django.contrib import admin
from deals.models import Deal, Country, City


class DealAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Deal._meta.fields]
    search_fields = ["title"]

    class Meta:
        model = Deal


admin.site.register(Deal, DealAdmin)


class CountryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Country._meta.fields]

    class Meta:
        model = Country


admin.site.register(Country, CountryAdmin)


class CityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in City._meta.fields]

    class Meta:
        model = City


admin.site.register(City, CityAdmin)
