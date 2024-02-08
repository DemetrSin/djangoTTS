from django.urls import path

from . import views

urlpatterns = [
    path('convert_text_to_speech', views.TextToSpeechView.as_view(), name='convert_text_to_speech'),
    path('tts_files', views.TtsFilesView.as_view(), name='tts_files'),
    path('history', views.UsersHistoryView.as_view(), name='history'),
    path('stt', views.STTView.as_view(), name='stt')
]
