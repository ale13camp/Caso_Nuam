from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET

from .access import AUDITOR, BUSINESS_ROLES, OPERATOR, business_required
from .models import Qualification


def visible_qualifications(user):
    return Qualification.objects.filter(Q(origin='official') | Q(origin='local', broker_id=user.broker_id))


@never_cache
@login_required
@require_GET
def home(request):
    return render(request, 'core/home.html')


@never_cache
@business_required(*BUSINESS_ROLES)
@require_GET
def qualifications(request):
    records = visible_qualifications(request.user)
    return render(request, 'core/qualifications.html', {'records': records[:100]})


@never_cache
@business_required(*BUSINESS_ROLES)
@require_GET
def qualification_detail(request, pk):
    record = get_object_or_404(visible_qualifications(request.user), pk=pk)
    return render(request, 'core/detail.html', {'record': record})


@never_cache
@business_required(OPERATOR)
@require_GET
def entry(request):
    return render(
        request,
        'core/placeholder.html',
        {
            'title': 'Ingresar calificación',
            'description': 'El ingreso guiado en tres pasos y el cálculo de factores se implementarán en la clase 11.',
            'steps': ['Datos del evento', 'Montos y factores', 'Vista previa y confirmación'],
        },
    )


@never_cache
@business_required(OPERATOR)
@require_GET
def upload(request):
    return render(
        request,
        'core/placeholder.html',
        {
            'title': 'Carga CSV',
            'description': 'La validación del archivo, la vista previa y la confirmación del lote se implementarán en la clase 12.',
            'steps': ['Seleccionar archivo', 'Revisar validación', 'Confirmar y ver resumen'],
        },
    )


@never_cache
@business_required(AUDITOR)
@require_GET
def history(request):
    return render(
        request,
        'core/placeholder.html',
        {
            'title': 'Historial de auditoría',
            'description': 'Esta ruta está reservada al auditor de su corredor. La consulta del log se implementará junto con las operaciones de la clase 12.',
            'steps': [],
        },
    )
