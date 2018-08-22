from django.contrib import admin
from app01 import models
# Register your models here.
admin.site.register(models.UserInfo)
admin.site.register(models.UserGroup)
admin.site.register(models.Role)