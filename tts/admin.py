from django.contrib import admin

from .models import AudioFile, UserAction

admin.site.register(AudioFile)
admin.site.register(UserAction)
