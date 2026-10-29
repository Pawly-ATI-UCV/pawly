from datetime import timedelta

from django.utils import timezone


def badges(request):
    # Números del menú con los mensajes sin responder y las novedades del último día
    if not request.user.is_authenticated:
        return {}

    from .views import build_notifications, get_chats

    day_ago = timezone.now() - timedelta(days=1)
    return {
        'unread_messages': sum(1 for chat in get_chats(request.user) if chat.unread),
        'new_notifications': sum(1 for item in build_notifications(request.user) if item['date'] >= day_ago),
    }
