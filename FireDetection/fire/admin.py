from django.contrib import admin


from FireDetection.fire.models import Interfaces

# Register your models here.

class InterfacesAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    empty_value_display = '---'
    pass

admin.site.register(Interfaces, InterfacesAdmin)