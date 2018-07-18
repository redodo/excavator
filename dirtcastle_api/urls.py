from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers

from . import views


router = routers.SimpleRouter()
router.register(r'tokens', views.TokenViewSet)
router.register(r'annotators', views.AnnotatorViewSet)

annotators_router = routers.NestedSimpleRouter(router, r'annotators', lookup='annotator')
annotators_router.register(r'patterns', views.AnnotatorPatternViewSet, base_name='annotator-patterns')
annotators_router.register(r'documents', views.AnnotatorDocumentViewSet, base_name='annotator-documents')


annotator_documents_router = routers.NestedSimpleRouter(annotators_router, r'documents', lookup='document')
annotator_documents_router.register(r'patterns', views.AnnotatorDocumentPatternViewSet, base_name='annotator-document-patterns')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(annotators_router.urls)),
    path('', include(annotator_documents_router.urls)),
    path('admin/', admin.site.urls),
]
