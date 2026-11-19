import json
from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings
from pymongo.errors import ConnectionFailure

from core.models import AuditEvent, Broker, Factor, Qualification, User


class DemoSeedTests(TestCase):
    @override_settings(DEBUG=True)
    def test_seed_is_repeatable_and_never_resets_existing_passwords(self):
        output = StringIO()
        call_command('seed_demo', stdout=output)
        self.assertEqual(Broker.objects.count(), 2)
        self.assertEqual(User.objects.count(), 7)
        self.assertEqual(Qualification.objects.count(), 3)
        self.assertEqual(Factor.objects.count(), 90)
        user = User.objects.get(username='operador_a')
        original = user.password
        self.assertNotIn(original, output.getvalue())
        call_command('seed_demo', stdout=StringIO())
        self.assertEqual(User.objects.get(pk=user.pk).password, original)
        self.assertEqual(Qualification.objects.count(), 3)

    @override_settings(DEBUG=False)
    def test_seed_refuses_production_environment(self):
        with self.assertRaises(CommandError):
            call_command('seed_demo')
        self.assertFalse(User.objects.exists())


class ConnectionCheckTests(TestCase):
    @override_settings(MONGODB_URI='')
    def test_missing_atlas_configuration_is_explicit(self):
        output = StringIO()
        with self.assertRaises(CommandError):
            call_command('check_connections', stdout=output)
        report = json.loads(output.getvalue())
        self.assertEqual(report['mongodb'], 'sin_configurar')
        self.assertIn(report['relational'], ('postgresql', 'sqlite'))


class AuditDeliveryTests(TestCase):
    def setUp(self):
        broker = Broker.objects.create(code='A', name='Corredor A')
        actor = User.objects.create_user(username='demo', broker=broker)
        self.event = AuditEvent.objects.create(
            broker=broker, actor=actor, action='connection_test', record_id='demo'
        )

    @override_settings(MONGODB_URI='')
    def test_delivery_without_configuration_preserves_pending_event(self):
        with self.assertRaises(CommandError):
            call_command('sync_audit')
        self.event.refresh_from_db()
        self.assertIsNone(self.event.delivered_at)

    def test_outage_does_not_lose_pending_event(self):
        # Only the external transport is substituted; the command and SQL outbox are real.
        with patch('core.management.commands.sync_audit.deliver_event', side_effect=ConnectionFailure):
            with self.assertRaises(CommandError):
                call_command('sync_audit')
        self.event.refresh_from_db()
        self.assertIsNone(self.event.delivered_at)
