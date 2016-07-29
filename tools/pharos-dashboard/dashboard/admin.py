from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Booking)
admin.site.register(Pod)
admin.site.register(Resource)
admin.site.register(Server)
admin.site.register(UserResource)