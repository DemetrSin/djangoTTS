from django.contrib import admin

from .models import AnonymousFiles, CustomUser

admin.site.register(CustomUser)
admin.site.register(AnonymousFiles)
