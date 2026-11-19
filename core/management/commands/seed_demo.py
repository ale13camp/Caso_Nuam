import secrets
from datetime import date

from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.access import AUDITOR, CONSULTANT, OPERATOR, TECH_ADMIN
from core.models import Broker, Factor, Qualification, User


class Command(BaseCommand):
    help = 'Crea datos ficticios repetibles y contraseñas aleatorias (solo DEBUG=true).'

    @transaction.atomic
    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError('Los datos demo solo se cargan con DEBUG=true en un entorno de desarrollo.')
        brokers = {}
        for code in ('A', 'B'):
            brokers[code], _ = Broker.objects.get_or_create(
                code=f'DEMO-{code}', defaults={'name': f'Corredor Ficticio {code}'}
            )
        groups = {
            name: Group.objects.get_or_create(name=name)[0]
            for name in (OPERATOR, CONSULTANT, AUDITOR, TECH_ADMIN)
        }
        groups[TECH_ADMIN].permissions.set(
            Permission.objects.filter(
                content_type__app_label__in=['auth', 'core'], content_type__model__in=['group', 'user']
            )
        )
        accounts = [
            ('operador_a', OPERATOR, 'A'),
            ('operador_b', OPERATOR, 'B'),
            ('consultor_a', CONSULTANT, 'A'),
            ('consultor_b', CONSULTANT, 'B'),
            ('auditor_a', AUDITOR, 'A'),
            ('auditor_b', AUDITOR, 'B'),
            ('admin_tecnico', TECH_ADMIN, None),
        ]
        credentials = []
        for username, role, broker_code in accounts:
            if User.objects.filter(username=username).exists():
                continue  # No sobrescribir cuentas ni cambiar sus contraseñas/permisos.
            password = secrets.token_urlsafe(18)
            user = User.objects.create_user(
                username=username,
                password=password,
                broker=brokers.get(broker_code),
                is_staff=role == TECH_ADMIN,
            )
            user.groups.add(groups[role])
            credentials.append(f'{username}\t{password}\t{role}')
        for broker, instrument, origin, sequence in [
            (None, 'NUAM-DEMO-OFICIAL', 'official', 1),
            (brokers['A'], 'NUAM-DEMO-LOCAL-A', 'local', 10001),
            (brokers['B'], 'NUAM-DEMO-LOCAL-B', 'local', 10001),
        ]:
            qualification, _ = Qualification.objects.get_or_create(
                broker=broker,
                origin=origin,
                fiscal_year=2026,
                market='ACCIONES',
                instrument=instrument,
                payment_date=date(2026, 11, 18),
                sequence=sequence,
                dividend_number=1,
                defaults={'source': 'system'},
            )
            for position in range(8, 38):
                Factor.objects.get_or_create(
                    qualification=qualification,
                    position=position,
                    defaults={
                        'amount_cents': 10000 if position == 8 else 0,
                        'scaled_value': 100000000 if position == 8 else 0,
                    },
                )
        if credentials:
            self.stdout.write(
                'Credenciales nuevas: guarda esta salida en un lugar local y no la subas a Git.'
            )
            self.stdout.write('usuario\tcontraseña\tperfil')
            for line in credentials:
                self.stdout.write(line)
        self.stdout.write(
            self.style.SUCCESS('Datos ficticios disponibles. Las cuentas existentes no se modificaron.')
        )
