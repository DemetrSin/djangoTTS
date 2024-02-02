import os
import fitz

from django.conf import settings
from gtts import gTTS

# from django.core.files.storage import default_storage


class AudioConverter:

    def read_txt(self, txt_file):
        with open(file=txt_file, mode='r', encoding='utf-8') as file:
            content = file.read()
        return content

    def text_to_speech(self, text, output_file):
        output_path = os.path.join(settings.MEDIA_ROOT, output_file)
        tts = gTTS(text, lang='en', slow=False)
        tts.save(output_path)
        return output_file

    # def handle_uploaded_file(self, uploaded_file):
    #     filename = uploaded_file.name
    #     file_path = os.path.join(settings.MEDIA_ROOT, filename)
    #     with default_storage.open(file_path, 'w+') as destination:
    #         for chunk in uploaded_file.chunks():
    #             destination.write(chunk.decode('utf-8'))
    #     return file_path

    def pdf_to_txt(self, pdf_path, text_path=None):
        pdf_document = fitz.open(pdf_path)
        text = ""
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            text += page.get_text()

        pdf_document.close()

        # with open(text_path, 'w', encoding='utf-8') as text_file:
        #     text_file.write(text)

        return text