import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q


class Broker(models.Model):
    code = models.CharField('código', max_length=20, unique=True)
    name = models.CharField('nombre', max_length=120)
    active = models.BooleanField('activo', default=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    broker = models.ForeignKey(
        Broker, verbose_name='corredor', on_delete=models.PROTECT, null=True, blank=True
    )


class Qualification(models.Model):
    class Origin(models.TextChoices):
        OFFICIAL = 'official', 'Oficial'
        LOCAL = 'local', 'Local'

    broker = models.ForeignKey(Broker, on_delete=models.PROTECT, null=True, blank=True)
    origin = models.CharField(max_length=10, choices=Origin.choices, default=Origin.LOCAL)
    fiscal_year = models.PositiveSmallIntegerField('ejercicio')
    market = models.CharField('mercado', max_length=40)
    instrument = models.CharField('instrumento', max_length=60)
    payment_date = models.DateField('fecha de pago')
    sequence = models.PositiveIntegerField('secuencia')
    dividend_number = models.PositiveIntegerField('número de dividendo')
    source = models.CharField(
        'vía',
        max_length=10,
        choices=[('manual', 'Manual'), ('csv', 'CSV'), ('system', 'Sistema')],
        default='manual',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fiscal_year', 'instrument', 'pk']
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(origin='official', broker__isnull=True) | Q(origin='local', broker__isnull=False)
                ),
                name='origin_matches_broker',
            ),
            models.UniqueConstraint(
                fields=[
                    'broker',
                    'fiscal_year',
                    'market',
                    'instrument',
                    'payment_date',
                    'sequence',
                    'dividend_number',
                ],
                condition=Q(origin='local'),
                name='unique_local_event',
            ),
            models.UniqueConstraint(
                fields=['fiscal_year', 'market', 'instrument', 'payment_date', 'sequence', 'dividend_number'],
                condition=Q(origin='official'),
                name='unique_official_event',
            ),
        ]
        indexes = [
            models.Index(
                fields=['broker', 'fiscal_year', 'market', 'instrument'], name='broker_year_market_idx'
            )
        ]

    def __str__(self):
        return f'{self.instrument} · {self.fiscal_year} · {self.get_origin_display()}'


class Factor(models.Model):
    qualification = models.ForeignKey(Qualification, related_name='factors', on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField()
    amount_cents = models.BigIntegerField(default=0)
    scaled_value = models.BigIntegerField(default=0)

    class Meta:
        ordering = ['position']
        constraints = [
            models.UniqueConstraint(fields=['qualification', 'position'], name='unique_factor_position'),
            models.CheckConstraint(
                condition=Q(position__gte=8, position__lte=37), name='factor_position_range'
            ),
            models.CheckConstraint(
                condition=Q(scaled_value__gte=0, scaled_value__lte=100000000), name='factor_value_range'
            ),
        ]


class AuditEvent(models.Model):
    """Outbox relacional; no se expone en Django Admin ni en formularios."""

    event_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    broker = models.ForeignKey(Broker, on_delete=models.PROTECT)
    actor = models.ForeignKey(User, on_delete=models.PROTECT)
    occurred_at = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=40)
    record_id = models.CharField(max_length=80)
    source = models.CharField(max_length=20, default='system')
    changes = models.JSONField(default=dict)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['occurred_at', 'pk']
