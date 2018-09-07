from django.db import models
from django.contrib.postgres.fields import JSONField


class Token(models.Model):
    name = models.CharField(primary_key=True, max_length=32)
    pattern = models.CharField(max_length=256)


class Pattern(models.Model):
    pattern = models.CharField(max_length=256)


class Annotator(models.Model):
    name = models.CharField(primary_key=True, max_length=32)
    patterns = models.ManyToManyField(Pattern, related_name='annotators', blank=True)


class Document(models.Model):
    annotator = models.ForeignKey(
        Annotator,
        related_name='documents',
        on_delete=models.CASCADE,
        blank=True,
    )
    data = JSONField(blank=True, null=True)
    patterns = models.ManyToManyField(Pattern, related_name='documents', blank=True)
