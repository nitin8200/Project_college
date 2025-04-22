from django.contrib import admin
from .models import Category, Tool, Review, Comparison  # Import your models

# Register each model
admin.site.register(Category)
admin.site.register(Tool)
admin.site.register(Review)
admin.site.register(Comparison)
