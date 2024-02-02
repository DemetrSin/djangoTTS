from django import forms

from .models import CustomUser


class UserProfileForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-1'}))
    # email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-1'}))

    class Meta:
        model = CustomUser
        fields = ['username']
