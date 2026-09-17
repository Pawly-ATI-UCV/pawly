from django.shortcuts import render
from django.utils import timezone
from .models import Post


def post_list(request):
    # Filtramos solo los posts publicados y los ordenamos por fecha de publicación descendente
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    # Pasamos los posts al archivo HTML mediante el contexto
    return render(request, 'PawlyApp/post_list.html', {'posts': posts})