from rest_framework import viewsets
from rest_framework.response import Response

from . import serializers
from .mixins import WriteableNestedViewSetMixin
from .models import Token, Pattern, Annotator, Document


class TokenViewSet(WriteableNestedViewSetMixin, viewsets.ModelViewSet):
    model = Token
    queryset = Token.objects.all()
    serializer_class = serializers.TokenSerializer


class AnnotatorViewSet(WriteableNestedViewSetMixin, viewsets.ModelViewSet):
    model = Annotator
    queryset = Annotator.objects.all()
    serializer_class = serializers.AnnotatorSerializer


class DocumentViewSet(WriteableNestedViewSetMixin, viewsets.ModelViewSet):
    model = Document
    queryset = Document.objects.all()
    serializer_class = serializers.DocumentSerializer


class PatternViewSet(WriteableNestedViewSetMixin, viewsets.ModelViewSet):
    model = Pattern
    queryset = Pattern.objects.all()
    serializer_class = serializers.PatternSerializer

    def filter_lookup_fields(self, lookup_fields):
        """Prevent relating document patterns to the parent annotator"""
        if 'documents__pk' in lookup_fields:
            lookup_fields.pop('annotators__pk')
        return lookup_fields


class AnnotateViewSet(viewsets.ViewSet):
    def get(self, request):
        return Response('hello world')
