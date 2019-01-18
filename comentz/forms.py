from django import forms
from django.utils.translation import ugettext as _

class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    parent_id = forms.IntegerField(widget=forms.HiddenInput,required=False)
    content = forms.CharField(widget=forms.Textarea)
    class Meta:
        widgets = {
            # 'content': forms.TextInput(attrs={'class':'form-control',})
            # 'content': forms.Textarea(attrs={'class':'form-control','placeholder': _('Введіть Ваш коментар')}),
        }