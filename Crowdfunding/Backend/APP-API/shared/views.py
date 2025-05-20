from rest_framework.views import APIView
from django.http import FileResponse
import os
from django.conf import settings

class DownloadPdf(APIView):
    def get(self, request):
        ruta_pdf = os.path.join(settings.MEDIA_ROOT, 'docs', 'CrowdFundMe-Manual-creador.pdf')
        return FileResponse(open(ruta_pdf, 'rb'), as_attachment=True, filename='CrowdFundMe-Manual-creador.pdf')