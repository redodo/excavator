from rest_framework import viewsets

from . import serializers
from .models import Token, Pattern, Annotator, Document


class TokenViewSet(viewsets.ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = serializers.TokenSerializer


class AnnotatorViewSet(viewsets.ModelViewSet):
    queryset = Annotator.objects.all()
    serializer_class = serializers.AnnotatorSerializer


class AnnotatorPatternViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PatternSerializer

    def get_queryset(self):
        return Annotator.objects.get(pk=self.kwargs['annotator_pk']).patterns.all()


class AnnotatorDocumentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DocumentSerializer

    def get_queryset(self):
        return Annotator.objects.get(pk=self.kwargs['annotator_pk']).documents.all()


class AnnotatorDocumentPatternViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PatternSerializer

    def get_queryset(self):
        return Document.objects.get(pk=self.kwargs['document_pk'], annotator=self.kwargs['annotator_pk']).patterns.all()
