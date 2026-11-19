from django.core.management.base import BaseCommand, CommandError

from core.access import OPERATOR, has_business_access
from core.models import AuditEvent, User


class Command(BaseCommand):
    help = 'Crea un evento ficticio de conexión en el outbox, para comprobar entrega a Atlas.'

    def add_arguments(self, parser):
        parser.add_argument('--username', required=True)

    def handle(self, *args, **options):
        user = User.objects.filter(username=options['username']).first()
        if not user or not has_business_access(user, (OPERATOR,)):
            raise CommandError('Indica un operador activo asociado a un corredor activo.')
        event = AuditEvent.objects.create(
            broker=user.broker,
            actor=user,
            action='connection_test',
            record_id='demo-clase10',
            source='system',
            changes={'description': 'Prueba ficticia de conexión; no representa una operación de negocio.'},
        )
        self.stdout.write(
            f'Evento pendiente creado: {event.event_id}. Ejecuta sync_audit y comprueba ese _id en Atlas.'
        )
