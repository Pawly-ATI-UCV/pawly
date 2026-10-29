from django import template
from django.utils import formats, timezone
from django.utils.translation import gettext as _

register = template.Library()


@register.filter
def ago(value):
    # Fecha corta como en el diseño, por ejemplo hace 2 h o ayer
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
    # Hora corta de la lista de chats, por ejemplo 10:45 o ayer
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
