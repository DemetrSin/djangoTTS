from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path('convert_text_to_speech',
         login_required(
             function=views.TextToSpeechView.as_view(),
             login_url='login'
         ),
         name='convert_text_to_speech'),
    path('tts_files',
         login_required(
             function=views.TtsFilesView.as_view(),
             login_url='login'
         ),
         name='tts_files'),
    path('history',
         login_required(
             function=views.UsersHistoryView.as_view(),
             login_url='login'
         ),
         name='history'),
    path('stt',
         login_required(
             function=views.AudioToTextView.as_view(),
             login_url='login'
         ),
         name='stt'),
    path('process_speech/',
         login_required(
             function=views.SpeechToTextView.as_view(),
             login_url='login'
         ),
         name='process_speech'),
]
