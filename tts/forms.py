from django import forms
from django.core.validators import MaxLengthValidator

from .models import AudioFile


class TextToSpeechForm(forms.ModelForm):
    text = forms.CharField(
        validators=[MaxLengthValidator(limit_value=1000)],
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        required=False
    )

    class Meta:
        model = AudioFile
        fields = ['text', 'text_file']


class STTForm(forms.ModelForm):
    class Meta:
        model = AudioFile
        fields = ['audiofile']
