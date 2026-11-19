from types import SimpleNamespace
from unittest.mock import patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from core.models import AuditEvent, Broker, User


class MongoTransport:
    """Sustituye solo la frontera de red para inspeccionar los documentos emitidos."""

    def __init__(self, acknowledged=True):
        self.documents = {}
        self.acknowledged = acknowledged
        self.write_concern = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def __getitem__(self, name):
        return self

    def with_options(self, **options):
        self.write_concern = options['write_concern']
        return self

    def update_one(self, query, update, upsert=False):
        if upsert and self.acknowledged:
            self.documents.setdefault(query['_id'], update['$setOnInsert'])
        return SimpleNamespace(acknowledged=self.acknowledged)


class AuditAcknowledgementTests(TestCase):
    def setUp(self):
        self.broker = Broker.objects.create(code='TEST', name='Corredor de prueba')
        self.user = User.objects.create_user(username='actor', broker=self.broker)
        self.event = AuditEvent.objects.create(
            broker=self.broker,
            actor=self.user,
            action='connection_test',
            record_id='demo-1',
            changes={'description': 'Prueba'},
        )

    def test_unacknowledged_write_never_marks_outbox_delivered(self):
        transport = MongoTransport(acknowledged=False)
        with patch('core.audit.mongo_client', return_value=transport):
            with self.assertRaises(CommandError):
                call_command('sync_audit')
        self.event.refresh_from_db()
        self.assertIsNone(self.event.delivered_at)

    def test_acknowledged_delivery_maps_actor_broker_and_event_then_marks_sql(self):
        transport = MongoTransport()
        with patch('core.audit.mongo_client', return_value=transport):
            call_command('sync_audit')
        self.event.refresh_from_db()
        self.assertIsNotNone(self.event.delivered_at)
        self.assertEqual(transport.write_concern.document, {'w': 'majority', 'wtimeout': 5000})
        self.assertEqual(
            transport.documents[str(self.event.event_id)],
            {
                '_id': str(self.event.event_id),
                'event_id': str(self.event.event_id),
                'user_id': self.user.pk,
                'broker_id': self.broker.pk,
                'occurred_at': self.event.occurred_at,
                'action': 'connection_test',
                'record_id': 'demo-1',
                'source': 'system',
                'changes': {'description': 'Prueba'},
            },
        )

    def test_retry_after_sql_mark_loss_reuses_uuid_without_replacing_log(self):
        transport = MongoTransport()
        with patch('core.audit.mongo_client', return_value=transport):
            call_command('sync_audit')
            AuditEvent.objects.filter(pk=self.event.pk).update(delivered_at=None)
            call_command('sync_audit')
        self.event.refresh_from_db()
        self.assertEqual(list(transport.documents), [str(self.event.event_id)])
        self.assertIsNotNone(self.event.delivered_at)
