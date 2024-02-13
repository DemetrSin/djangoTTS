from django import forms

from .models import AnonymousFiles, CustomUser


class UserProfileForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-1'}))

    class Meta:
        model = CustomUser
        fields = ['username']


class AnonymousHomeTTSForm(forms.ModelForm):
    class Meta:
        model = AnonymousFiles
        fields = ['text']
