from django.contrib import admin
from . import models

admin.site.register(models.Route)
admin.site.register(models.FavoriteRoute)
admin.site.register(models.RouteRate)
admin.site.register(models.Comment)
admin.site.register(models.CommentRate)