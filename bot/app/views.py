from django.http import FileResponse
from django.shortcuts import get_object_or_404

from .models import EquipmentCatalog, GeneralCatalog


def pdf_view(request, pk):
    equipment_catalog = get_object_or_404(EquipmentCatalog, pk=pk)
    file_path = equipment_catalog.pdf_file.path
    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')


def general_catalog_pdf_view(request, pk):
    general_catalog = get_object_or_404(GeneralCatalog, pk=pk)
    file_path = general_catalog.pdf_file.path
    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
