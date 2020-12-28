from django.contrib import admin
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "body", "is_answered") 
    # добавляем интерфейс для поиска по тексту постов
    search_fields = ("email",) 
    empty_value_display = "-пусто-" 


admin.site.register(Contact, ContactAdmin)