from rest_framework.serializers import ModelSerializer

from .models import Token, Annotator, Pattern, Document


class TokenSerializer(ModelSerializer):
    class Meta:
        model = Token
        fields = ('name', 'pattern')


class AnnotatorSerializer(ModelSerializer):
    class Meta:
        model = Annotator
        fields = ('name', 'patterns', 'documents')


class DocumentSerializer(ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'patterns', 'data')


class PatternSerializer(ModelSerializer):
    class Meta:
        model = Pattern
        fields = ('id', 'pattern')
