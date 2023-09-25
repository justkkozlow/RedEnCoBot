from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from app import views

app_name = 'app'

urlpatterns = [
    path('pdf/equipment/<int:pk>/', views.pdf_view, name='equipment-pdf-view'),
    path('pdf/general/<int:pk>/', views.general_catalog_pdf_view, name='general-catalog-pdf-view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
