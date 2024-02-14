from django.contrib import admin

from .models import AnonymousFiles, CustomUser, Subscription

admin.site.register(CustomUser)
admin.site.register(AnonymousFiles, list_display=('created_at',))
admin.site.register(Subscription)

