from django.core.management.base import BaseCommand
from projects.models import ProjectImage

class Command(BaseCommand):
    help = 'Reprocesa las imágenes del proyecto según los nuevos procesadores'

    def handle(self, *args, **kwargs):
        updated = 0
        for img in ProjectImage.objects.all():
            if img.image:
                img.image = img.image
                img.save()
                updated += 1
        self.stdout.write(self.style.SUCCESS(f'{updated} imágenes reprocesadas.'))
