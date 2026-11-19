from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from pymongo.errors import PyMongoError

from core.audit import deliver_event
from core.models import AuditEvent


class Command(BaseCommand):
    help = 'Entrega hasta 100 eventos pendientes a MongoDB; los fallidos quedan para reintento.'

    def handle(self, *args, **options):
        delivered = 0
        for event in AuditEvent.objects.filter(delivered_at__isnull=True)[:100]:
            try:
                deliver_event(event)
            except (PyMongoError, ImproperlyConfigured):
                raise CommandError(
                    'No se pudo entregar el evento. Revisa la conexión localmente y reintenta; permanece pendiente.'
                ) from None
            AuditEvent.objects.filter(pk=event.pk, delivered_at__isnull=True).update(
                delivered_at=timezone.now()
            )
            delivered += 1
        self.stdout.write(f'Eventos entregados: {delivered}.')
