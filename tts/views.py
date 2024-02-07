import os

from django.conf import settings
from django.shortcuts import render
from django.views import View

from .text_to_speech import AudioConverter


from .forms import TextToSpeechForm
from .models import AudioFile, UserAction


class TextToSpeechView(View):
    template_name = 'tts/convert_text_to_speech.html'

    def get(self, request, *args, **kwargs):
        form = TextToSpeechForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = TextToSpeechForm(request.POST, request.FILES)
        audio_file_url = None

        if form.is_valid():
            text = form.cleaned_data['text']
            instance = form.save(commit=False)
            instance.user = request.user

            if 'text_file' in request.FILES:
                instance.text_file = request.FILES['text_file']
                instance.filename = request.FILES['text_file'].name
                instance.save()

            audio_converter = AudioConverter()
            output_file = None

            if text:
                output_file = audio_converter.text_to_speech(
                    text=text,
                    output_file=f"{text.split()[0]}.mp3"
                )
            elif '.docx' in instance.filename:
                text_from_docx = audio_converter.docx_to_text(
                    docx_path=f'media/text_files/{instance.filename.replace(" ", "_")}'
                )
                output_file = audio_converter.text_to_speech(
                    text=text_from_docx,
                    output_file=instance.filename.replace('.docx', '.mp3')
                )
            elif '.pdf' in instance.filename:
                text_from_pdf = audio_converter.pdf_to_text(
                    pdf_path=f'media/text_files/{instance.filename.replace(" ", "_")}'
                )
                output_file = audio_converter.text_to_speech(
                    text=text_from_pdf,
                    output_file=instance.filename.replace('.pdf', '.mp3')
                )
            elif '.txt' in instance.filename:
                text_from_file = audio_converter.read_txt(
                    txt_file=f'media/text_files/{instance.filename.replace(" ", "_")}'
                )
                output_file = audio_converter.text_to_speech(
                    text=text_from_file,
                    output_file=instance.filename.replace('.txt', '.mp3')
                )

            audio_file_url = f"{settings.MEDIA_URL}{output_file}"

            if '.mp3' in output_file:
                instance.audiofile = audio_file_url.removeprefix('/media/')
                instance.audiofile.name = output_file
                UserAction.objects.create(user=request.user, action=f"Created an {output_file}")
            if '.zip' in output_file:
                instance.zipfile.name = os.path.basename(output_file)
                UserAction.objects.create(user=request.user, action=f"Created an {os.path.basename(output_file)}")
            instance.save()
        else:
            return render(request, self.template_name, {'form': form, 'audio_file_url': audio_file_url})

        return render(request, self.template_name, {
            'form': form,
            'audio_file_url': audio_file_url,
            'output_file': output_file
        }
                      )


class TtsFilesView(View):
    template_name = 'tts/tts_files.html'

    def get(self, request, *args, **kwargs):
        user_files = AudioFile.objects.filter(user=request.user)
        return render(request, self.template_name, {'user_files': user_files})


class UsersHistoryView(View):
    template_name = 'tts/history.html'

    def get(self, request, *args, **kwargs):
        user_actions = UserAction.objects.filter(user=request.user)
        return render(request, self.template_name, {'user_actions': user_actions})
