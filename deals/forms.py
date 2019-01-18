from django import forms
from .models import Deal,City
# from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _
class SearchForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ('speciality', 'country', 'city')

        widgets = {
            'speciality': forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'choices-multiple-remove-button','placeholder':_('Введіть спеціальності')}),
            'country': forms.Select(attrs={'class': 'form-control','placeholder': _('Введіть спеціальності')}),
            'city': forms.Select(attrs={'class': 'form-control', })
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.city_set.order_by('name')


class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ('title', 'description', 'speciality', 'country', 'city')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset