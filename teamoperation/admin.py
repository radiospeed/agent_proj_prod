from django.contrib import admin

# Register your models here.
from .models import Operative, AWTeam, Mission
admin.site.register(Operative)
admin.site.register(AWTeam)
admin.site.register(Mission)
