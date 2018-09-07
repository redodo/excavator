import json
from django.core.management.base import BaseCommand
from django.db import transaction

from ...models import Annotator, Document, Pattern


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):
        with open(options['filename'], 'rt') as f:
            data = json.load(f)

        for source_annotator in data:
            annotator = Annotator.objects.create(name=source_annotator['name'])
            print(annotator)
            for source_doc in source_annotator['documents']:
                document = Document.objects.create(
                    annotator=annotator,
                    data=source_doc['data'],
                )
                with transaction.atomic():
                    for source_pattern in source_doc['patterns']:
                        pattern = Pattern.objects.create(pattern=source_pattern)
                        document.patterns.add(pattern)
