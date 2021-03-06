from django.contrib import admin

# Register your models here.
from .models import Track, Album, Purchase, Customer


class TrackInline(admin.StackedInline):
    model = Track
    extra = 1


class AlbumAdmin(admin.ModelAdmin):
    inlines = [TrackInline]


admin.site.register(Track)
admin.site.register(Album, AlbumAdmin)

admin.site.register(Purchase)
admin.site.register(Customer)