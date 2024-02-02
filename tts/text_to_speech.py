import os

import fitz
from django.conf import settings
from docx import Document
from gtts import gTTS


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

    def pdf_to_text(self, pdf_path, text_path=None):
        pdf_document = fitz.open(pdf_path)
        text = ""
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            text += page.get_text()

        pdf_document.close()

        return text

    def docx_to_text(self, docx_path):
        doc = Document(docx_path)
        text = []

        for paragraph in doc.paragraphs:
            text.append(paragraph.text)

        return '\n'.join(text)
