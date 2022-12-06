from django.contrib import admin
from recipes.models import Tag, Recipe, User

admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(User)
