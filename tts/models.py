import os

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from zipfile import ZipFile


class AudioFile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    text_file = models.FileField(upload_to='text_files', blank=True, null=True)
    filename = models.CharField(max_length=124, blank=True, null=True)
    audiofile = models.FileField(upload_to='audio_files', blank=True, null=True)
    zipfile = models.FileField(upload_to='zip_files', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk} > {self.user.username} > {self.filename}"

    def delete(self, *args, **kwargs):
        try:
            if self.text_file:
                os.remove(os.path.join(settings.MEDIA_ROOT,  self.text_file.name))
            if self.audiofile:
                os.remove(os.path.join(settings.MEDIA_ROOT, self.audiofile.name))
            if self.zipfile:
                zipfile_path = os.path.join(settings.MEDIA_ROOT, self.zipfile.name)
                get_file_names_from_zip(zipfile_path)
                os.remove(zipfile_path)
        except:
            pass
        super().delete(*args, **kwargs)


@receiver(pre_delete, sender=AudioFile)
def delete_files_on_audiofile_delete(sender, instance, **kwargs):
    try:
        if instance.text_file:
            os.remove(os.path.join(settings.MEDIA_ROOT, instance.text_file.name))
        if instance.audiofile:
            os.remove(os.path.join(settings.MEDIA_ROOT, instance.audiofile.name))
        if instance.zipfile:
            zipfile_path = os.path.join(settings.MEDIA_ROOT, instance.zipfile.name)
            get_file_names_from_zip(zipfile_path)
            os.remove(zipfile_path)
    except:
        pass


class UserAction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=124, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


def get_file_names_from_zip(zipfile_path):
    with ZipFile(zipfile_path, 'r') as zipf:
        file_names = zipf.namelist()
        for file_name in file_names:
            os.remove(os.path.join(settings.MEDIA_ROOT, file_name))
