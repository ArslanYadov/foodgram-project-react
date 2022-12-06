from django.contrib import admin
from recipes.models import Ingredient, Recipe, Tag, User

admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(User)
