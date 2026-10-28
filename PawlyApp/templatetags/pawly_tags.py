from django import template
from django.utils import formats, timezone
from django.utils.translation import gettext as _

register = template.Library()


@register.filter
def ago(value):
    # Fecha corta como en el diseño: hace 5 min, hace 2 h, ayer, hace 3 días
    if not value:
        return ''
    seconds = (timezone.now() - value).total_seconds()
    if seconds < 60:
        return _('ahora')
    if seconds < 3600:
        return _('hace %(count)d min') % {'count': seconds // 60}
    if seconds < 86400:
        return _('hace %(count)d h') % {'count': seconds // 3600}
    days = int(seconds // 86400)
    if days == 1:
        return _('ayer')
    if days < 7:
        return _('hace %(count)d días') % {'count': days}
    return formats.date_format(timezone.localtime(value), 'j b')


@register.filter
def short_time(value):
    # Hora de la lista de chats: 10:45, ayer, lun o 8 sep
    if not value:
        return ''
    local = timezone.localtime(value)
    days = (timezone.localdate() - local.date()).days
    if days == 0:
        return formats.date_format(local, 'H:i')
    if days == 1:
        return _('ayer')
    if days < 7:
        return formats.date_format(local, 'D').lower()
    return formats.date_format(local, 'j b')
