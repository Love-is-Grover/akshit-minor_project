from django.contrib import admin
from .models import Feedback,Image,Audio

# Register your models here.
admin.site.register(Feedback)
admin.site.register(Image)
admin.site.register(Audio)