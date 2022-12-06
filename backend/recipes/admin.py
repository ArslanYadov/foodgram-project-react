from django.contrib import admin
from recipes.models import Ingredient, Tag, Recipe, User


admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(User)
