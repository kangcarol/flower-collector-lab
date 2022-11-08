from django.contrib import admin
# import your models here
from .models import Flower, Care, Garden

# Register your models here
admin.site.register(Flower)
admin.site.register(Care)
admin.site.register(Garden)