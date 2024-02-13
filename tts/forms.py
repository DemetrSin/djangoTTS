from django import forms
from django.core.validators import MaxLengthValidator

from .models import AudioFile


class TextToSpeechForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        required=False
    )

    class Meta:
        model = AudioFile
        fields = ['text', 'text_file']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TextToSpeechForm, self).__init__(*args, **kwargs)

        if user and not user.is_premium:
            self.fields['text'].validators.append(MaxLengthValidator(
                limit_value=1000,
                message="Without premium status you can't input more than 1000 symbols"
            )
            )
        else:
            self.fields['text'].validators.append(MaxLengthValidator(limit_value=10000))



class AudioToTextForm(forms.ModelForm):
    class Meta:
        model = AudioFile
        fields = ['audiofile']
