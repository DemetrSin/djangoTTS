from django.contrib import admin

from .models import AnonymousFiles, CustomUser, Subscription

admin.site.register(CustomUser)
admin.site.register(AnonymousFiles)
admin.site.register(Subscription)
