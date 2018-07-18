from rest_framework import serializers

from . import models


class TokenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Token
        fields = ('name', 'pattern', 'url')


class AnnotatorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Annotator
        fields = ('name', 'patterns', 'documents', 'url')


class PatternSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Pattern
        fields = ('id', 'pattern', 'url')


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Document
        fields = ('id', 'annotator', 'patterns', 'data', 'url')
