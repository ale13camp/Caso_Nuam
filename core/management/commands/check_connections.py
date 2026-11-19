import json

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import DatabaseError, connection
from pymongo.errors import PyMongoError

from core.audit import mongo_client


class Command(BaseCommand):
    help = 'Comprueba ambas conexiones sin mostrar credenciales. Devuelve error si alguna falta.'

    def handle(self, *args, **options):
        report = {'relational': connection.vendor, 'relational_ok': False, 'mongodb': 'sin_configurar'}
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
                report['relational_ok'] = cursor.fetchone()[0] == 1
        except DatabaseError:
            report['relational_ok'] = False
        if settings.MONGODB_URI:
            try:
                with mongo_client() as client:
                    client.admin.command('ping')
                report['mongodb'] = 'conectado'
            except PyMongoError:
                report['mongodb'] = 'error_de_conexion'
        self.stdout.write(json.dumps(report, ensure_ascii=False))
        if (
            not report['relational_ok']
            or report['mongodb'] != 'conectado'
            or connection.vendor != 'postgresql'
        ):
            raise CommandError('Integración incompleta: se requieren PostgreSQL y MongoDB conectados.')
