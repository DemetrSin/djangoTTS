from django.urls import path

from . import views

urlpatterns = [
    path('convert_text_to_speech', views.TextToSpeechView.as_view(), name='convert_text_to_speech'),
    path('tts_files', views.TtsFilesView.as_view(), name='tts_files')
]