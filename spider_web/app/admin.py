from django.contrib import admin
from app.models import *

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Comments)
admin.site.register(News)
admin.site.register(Picture)