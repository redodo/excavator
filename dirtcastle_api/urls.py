from django.contrib import admin
from django.urls import path, include
from rest_framework_extensions.routers import ExtendedDefaultRouter

from . import views


router = ExtendedDefaultRouter()

router.register(r'tokens', views.TokenViewSet, base_name='token')

annotator_router = router.register(r'annotators', views.AnnotatorViewSet, base_name='annotator')

annotator_document_router = annotator_router.register(
    r'documents',
    views.DocumentViewSet,
    base_name='annotators-document',
    parents_query_lookups=['annotator__pk'],
)
annotator_document_router.register(
    r'patterns',
    views.PatternViewSet,
    base_name='annotators-documents-pattern',
    parents_query_lookups=['annotators__pk', 'documents__pk'],
)

annotator_router.register(
    r'patterns',
    views.PatternViewSet,
    base_name='annotators-pattern',
    parents_query_lookups=['annotators__pk'],
)

router.register(r'annotate', views.AnnotateViewSet, base_name='annotate')


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
