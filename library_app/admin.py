from django.contrib import admin
from . import models

admin.site.register(models.Book)
admin.site.register(models.Person)
admin.site.register(models.AddReadBook)
admin.site.register(models.SavedBook)
admin.site.register(models.Comment)
admin.site.register(models.FavouriteBooks)
admin.site.register(models.FriendShip)
