from django.contrib import admin
from .models import Meme


@admin.register(Meme)
class MemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'prompt', 'created_at')
    search_fields = ('prompt',)