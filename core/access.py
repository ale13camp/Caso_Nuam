from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

OPERATOR = 'Operador'
CONSULTANT = 'Consultor'
AUDITOR = 'Auditor'
TECH_ADMIN = 'Administrador técnico'
BUSINESS_ROLES = (OPERATOR, CONSULTANT, AUDITOR)


def roles_for(user):
    return set(user.groups.values_list('name', flat=True)) if user.is_authenticated else set()


def has_business_access(user, allowed):
    roles = roles_for(user)
    return bool(
        user.is_active
        and TECH_ADMIN not in roles
        and roles.intersection(allowed)
        and user.broker_id
        and user.broker.active
    )


def business_required(*allowed):
    def decorator(view):
        @login_required
        @wraps(view)
        def wrapped(request, *args, **kwargs):
            if not has_business_access(request.user, allowed):
                raise PermissionDenied
            return view(request, *args, **kwargs)

        return wrapped

    return decorator


def navigation(request):
    user = request.user
    if not user.is_authenticated:
        return {}
    return {
        'can_consult': has_business_access(user, BUSINESS_ROLES),
        'can_operate': has_business_access(user, (OPERATOR,)),
        'can_audit': has_business_access(user, (AUDITOR,)),
        'can_admin': user.is_active and user.is_staff and TECH_ADMIN in roles_for(user),
        'role_names': ', '.join(sorted(roles_for(user))) or 'Sin perfil asignado',
    }
