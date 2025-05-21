from django.core.management.base import BaseCommand
from accounts.models import Profile 
class Command(BaseCommand):
    help = 'Reprocesa las imágenes de perfil según los nuevos procesadores'

    def handle(self, *args, **kwargs):
        updated = 0
        for profile in Profile.objects.all():
            if profile.pfp and profile.pfp.name != 'profile_pics/default.jpg':
                profile.pfp = profile.pfp
                profile.save()
                updated += 1
        self.stdout.write(self.style.SUCCESS(f'{updated} imágenes de perfil reprocesadas.'))
