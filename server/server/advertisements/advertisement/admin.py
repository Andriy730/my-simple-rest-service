from django.contrib import admin

from .models import Advertisement, Tag


admin.site.register(Tag)
admin.site.register(Advertisement)
