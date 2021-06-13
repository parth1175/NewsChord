from django.contrib import admin
from .models import NewsSource
# Register your models here.
class NewsSourceAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(NewsSource, NewsSourceAdmin)
