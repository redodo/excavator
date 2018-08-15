from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from . import serializers
from .helpers import create_annotation_agent
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


class AnnotateText(APIView):
    def post(self, request):
        agent = create_annotation_agent()
        annotated_text = agent.annotate(request.body.decode('utf-8'))
        return Response(annotated_text.to_dict())
