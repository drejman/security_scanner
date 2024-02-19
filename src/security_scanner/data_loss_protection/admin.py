from django.contrib import admin
from data_loss_protection.models import Pattern, Alert


class AdminAlert(admin.ModelAdmin):
    pass


class AdminPattern(admin.ModelAdmin):
    pass


admin.site.register(Alert, AdminAlert)
admin.site.register(Pattern, AdminPattern)
