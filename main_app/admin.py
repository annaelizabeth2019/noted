from django.contrib import admin
from .models import Flashcard, Set, Group

# Register your models here.
admin.site.register(Flashcard)
admin.site.register(Set)
admin.site.register(Group)