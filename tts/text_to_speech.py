import os
import re
from zipfile import ZipFile

import fitz
from django.conf import settings
from docx import Document
from gtts import gTTS


class AudioConverter:

    @staticmethod
    def read_txt(txt_file):
        with open(file=txt_file, mode='r', encoding='utf-8') as file:
            content = file.read()
        return content

    def text_to_speech(self, text, output_file):
        output_path = os.path.join(settings.MEDIA_ROOT, output_file)
        if len(text) > 100:
            output_files = []
            chunks = self.split_text_into_chunks(text, 200)
            for i, chunk in enumerate(chunks, start=1):
                output_file_i = self.get_new_filename(output_path)
                output_path_i = os.path.join(settings.MEDIA_ROOT, output_file_i)
                tts = gTTS(chunk, lang='en', slow=False)
                tts.save(output_path_i)
                output_files.append(output_file_i)
            zipf = self.pack_to_zip(files_list=output_files, zip_name=output_files[0].replace('.mp3', '.zip'))
            return zipf
        tts = gTTS(text, lang='en', slow=False)
        tts.save(output_path)
        return output_file
    @staticmethod
    def pdf_to_text(pdf_path):
        pdf_document = fitz.open(pdf_path)
        text = ""
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            text += page.get_text()

        pdf_document.close()

        return text

    @staticmethod
    def docx_to_text(docx_path):
        doc = Document(docx_path)
        text = []

        for paragraph in doc.paragraphs:
            text.append(paragraph.text)

        return '\n'.join(text)

    @staticmethod
    def split_text_into_chunks(text, chunk_size):
        words = re.findall(r'\S+\s*', text)

        current_chunk = ""
        chunks = []

        for word in words:
            if len(current_chunk) + len(word) <= chunk_size:
                current_chunk += word
            else:
                chunks.append(current_chunk.strip())
                current_chunk = word

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    @staticmethod
    def get_new_filename(file_path):
        filename, extension = os.path.splitext(file_path)
        counter = 2
        while os.path.exists(file_path):
            file_path = f"{filename}{counter}{extension}"
            counter += 1
        return file_path

    @staticmethod
    def pack_to_zip(files_list, zip_name):
        with ZipFile(file=zip_name, mode='w') as zipf:
            for file in files_list:
                zipf.write(file, os.path.basename(file))
        return zip_name

    @staticmethod
    def unpack_zip(path_to_zip, path_to_unpack):
        with ZipFile(path_to_zip, 'r') as zip_ref:
            zip_ref.extractall(path_to_unpack)
