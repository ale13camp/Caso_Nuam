from django.db import IntegrityError, transaction
from django.test import TestCase

from core.models import Broker, Factor, Qualification


class IntegrityTests(TestCase):
    def setUp(self):
        self.a = Broker.objects.create(code='A', name='Corredor A')
        self.b = Broker.objects.create(code='B', name='Corredor B')
        self.data = dict(
            broker=self.a,
            fiscal_year=2026,
            market='ACCIONES',
            instrument='DEMO',
            payment_date='2026-11-18',
            sequence=10001,
            dividend_number=1,
        )

    def test_business_key_is_unique_inside_broker(self):
        Qualification.objects.create(**self.data)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Qualification.objects.create(**self.data)
        Qualification.objects.create(**{**self.data, 'broker': self.b})

    def test_official_key_is_unique_and_requires_no_broker(self):
        data = {**self.data, 'origin': 'official', 'broker': None}
        Qualification.objects.create(**data)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Qualification.objects.create(**data)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Qualification.objects.create(**{**self.data, 'origin': 'official'})
        with self.assertRaises(IntegrityError), transaction.atomic():
            Qualification.objects.create(**{**self.data, 'broker': None})

    def test_factor_bounds_and_uniqueness(self):
        qualification = Qualification.objects.create(**self.data)
        Factor.objects.create(
            qualification=qualification, position=8, amount_cents=12345, scaled_value=12345678
        )
        with self.assertRaises(IntegrityError), transaction.atomic():
            Factor.objects.create(qualification=qualification, position=8)
        for value in (-1, 100000001):
            with self.assertRaises(IntegrityError), transaction.atomic():
                Factor.objects.create(qualification=qualification, position=9, scaled_value=value)
        for position in (7, 38):
            with self.assertRaises(IntegrityError), transaction.atomic():
                Factor.objects.create(qualification=qualification, position=position)

    def test_foreign_key_cannot_reference_missing_broker(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Qualification.objects.create(**{**self.data, 'broker': None, 'broker_id': 999999})
                transaction.get_connection().check_constraints()
