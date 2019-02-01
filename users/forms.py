from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
# from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _
from .models import Profile, City, Message


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Ваш логін', 'class': 'form-input','id':'username-input'}),

            'first_name': forms.TextInput(attrs={'placeholder': _('Ваше ім\'я'), 'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'placeholder': _('Ваше прізвище'), 'class': 'form-input'}),
            'password1': forms.TextInput(attrs={'placeholder': _('Ваш пароль'), 'class': 'form-input'}),
            'password2': forms.TextInput(attrs={'placeholder': _('Підтвердіть пароль'), 'class': 'form-input'}),

        }

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise ValidationError("This email already used")
        return data

    def clean_password(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        cleaned_data = (password, password2)

        if password != password2:
            raise forms.ValidationError("The password does not match ")

        return cleaned_data

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),


        }

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['status','speciality','country','city','bio','skills','image','facebook','linkedin','language']
        labels = {
            'language':_('Мова платформи'),
        }
        widgets = {
            'bio': forms.Textarea(attrs={'class':'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'speciality': forms.Select(attrs={'class': 'form-control'}),
            'skills' : forms.SelectMultiple(attrs={'class':'form-control','id':'choices-multiple-remove-button'}),
            # 'image': forms.FileInput(attrs={'class': 'form-control'})
            'status' : forms.Select(attrs={'class': 'form-control'}),
            'facebook':forms.TextInput(attrs={'class':'form-control','placeholder':'Facebook link'}),
            'linkedin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'LinkedIn link'}),
            'language':forms.Select(attrs={'class':'form-control','label':"Select your language"})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        # elif self.instance.pk:
        #     self.fields['city'].queryset = self.instance.country.city_set.order_by('name')



# class SearchPeopleForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['speciality','skills','country','city']
#         widgets = {
#             'speciality': forms.SelectMultiple(attrs={'class':'form-control','id':'choices-multiple-remove-button'}),
#             'skills': forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'choices-multiple-remove-button'}),
#             'country': forms.Select(attrs={'class': 'form-control'}),
#             'city': forms.Select(attrs={'class': 'form-control'}),
#
#         }
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['city'].queryset = City.objects.none()
#
#         if 'country' in self.data:
#             try:
#                 country_id = int(self.data.get('country'))
#                 self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
#             except (ValueError, TypeError):
#                 pass  # invalid input from the client; ignore and fallback to empty City queryset
#         elif self.instance.pk:
#             self.fields['city'].queryset = self.instance.country.city_set.order_by('name')
class SearchPeopleForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['speciality','skills', 'country', 'city']

        widgets = {
            'skills': forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'choices-multiple-remove-button','placeholder': _('Введіть навички')}),
            'speciality': forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'choices-multiple-remove-button','placeholder':_('Введіть спеціальності')}),
            'country': forms.Select(attrs={'class': 'form-control','placeholder': _('Введіть спеціальності'),}),
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

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        labels = {'message': ""}