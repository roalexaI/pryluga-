from django import template

register = template.Library()


@register.filter
def tiene_acceso(user, codigo_opcion):
    return user.tiene_acceso(codigo_opcion)


@register.filter
def puede(user, accion_opcion):
    """
    Uso: user|puede:"reservas:crear"
    """
    try:
        opcion, accion = accion_opcion.split(':')
        return user.puede(opcion, accion)
    except Exception:
        return False