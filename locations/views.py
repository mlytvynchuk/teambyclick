from django.shortcuts import render


def load_cities(request):
    country_id = request.GET.get("country")
    cities = City.objects.filter(country_id=country_id).order_by("name")
    return render(request, "cities/city_dropdown_list_options.html", {"cities": cities})

