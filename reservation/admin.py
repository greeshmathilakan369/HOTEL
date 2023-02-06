from django.contrib import admin

# Register your models here.
from reservation.models import *

admin.site.register(User)
admin.site.register(Booking)