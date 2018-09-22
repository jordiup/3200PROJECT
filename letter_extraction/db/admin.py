from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import Person, Location, Document, PersonLocation

admin.site.register(Person)
admin.site.register(Location)
admin.site.register(Document)
admin.site.register(PersonLocation)