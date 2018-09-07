from time import time

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
        start = time()

        # TODO: implement persistent annotation settings with strategies
        #       and included/excluded annotators
        # TODO: accept a JSON object with 'text' and options
        # TODO: implement object matching framework to create complex
        #       objects from annotations, such as an container order
        text = request.body.decode('utf-8')
        annotated_text = request.annotation_agent.annotate(text)
        annotated_text = annotated_text.disambiguate(discard_others=True)

        delta = time() - start

        data = {'took': delta * 1000}
        data.update(annotated_text.to_dict())

        # Remove annotation spans from data
        for line in data['lines']:
            for annotation in line['annotations']:
                annotation.pop('span')

        response = Response(data)
        # TODO: figure out a more elegant way to mark a request as
        #       non-interfering with the annotation agent
        response.refresh_agent = False
        return response
