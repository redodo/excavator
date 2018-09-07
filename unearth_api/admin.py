from django.contrib import admin
from .models import Pattern, Token, Annotator, Document


admin.site.register([
    Pattern,
    Token,
    Annotator,
    Document,
])
