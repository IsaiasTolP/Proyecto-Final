import os
from django.core.management.base import BaseCommand
from django.conf import settings
from accounts.models import Profile

class Command(BaseCommand):
    help = 'Elimina imágenes del sistema de archivos que no están asociadas a ningún objeto Profile'

    def handle(self, *args, **kwargs):
        media_root = settings.MEDIA_ROOT
        image_dir = os.path.join(media_root, 'profile_pics')

        if not os.path.exists(image_dir):
            self.stdout.write(self.style.WARNING(f'El directorio {image_dir} no existe.'))
            return

        referenced_files = set(
            os.path.basename(profile.pfp.name)
            for profile in Profile.objects.exclude(pfp='')
        )

        deleted_files = []

        for fname in os.listdir(image_dir):
            fpath = os.path.join(image_dir, fname)
            if os.path.isfile(fpath) and fname not in referenced_files and fname != 'default.jpg':
                os.remove(fpath)
                deleted_files.append(fname)

        if deleted_files:
            self.stdout.write(self.style.SUCCESS(f'Se eliminaron {len(deleted_files)} archivos huérfanos:'))
            for f in deleted_files:
                self.stdout.write(f' - {f}')
        else:
            self.stdout.write(self.style.SUCCESS('No se encontraron archivos huérfanos.'))
