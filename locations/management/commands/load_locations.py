import csv
from django.core.management.base import BaseCommand
from locations.models import Country, City


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open("locations.csv") as f:
            reader = csv.reader(f)
            countries = Country.objects.all()
            cities = City.objects.all()
            next(reader)
            for row in reader:
                city_name, country_name, _, __ = row
                country, created = Country.objects.get_or_create(name=country_name)
                city, created = City.objects.get_or_create(
                    name=city_name, country=country
                )
