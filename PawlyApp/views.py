from datetime import timedelta

from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy
from django.views.decorators.http import require_POST

from SecurityApp.models import User

from .forms import ApplicationForm, MessageForm, PetForm
from .models import Application, Chat, Message, Pet, Post

# Opciones rápidas del formulario de postulación
HOME_OPTIONS = {
    'yard': gettext_lazy('Tengo patio'),
    'no-pets': gettext_lazy('Sin otras mascotas'),
    'kids': gettext_lazy('Tengo niños'),
    'apartment': gettext_lazy('Vivo en apartamento'),
}


def get_chats(user):
    chats = list(user.chats.all().order_by('-created_at'))
    for chat in chats:
        chat.other = chat.other_member(user)
        # Mensajes de la otra persona después del último mensaje propio
        chat.unread = 0
        for message in chat.messages.all():
            chat.unread = 0 if message.sender_id == user.id else chat.unread + 1
    return chats


def build_notifications(user):
    items = []

    # Las notificaciones salen de las postulaciones que recibe y de los mensajes
    for application in Application.objects.filter(chat__members=user).exclude(applicant=user):
        url = reverse('chat_detail', args=[application.chat.id]) if hasattr(application, 'chat') else ''
        items.append({'kind': 'adoption', 'date': application.created_at, 'user': application.applicant,
                      'pet': application.pet, 'url': url or reverse('pet_profile', args=[application.pet.id])})
    for chat in user.chats.all():
        message = chat.messages.exclude(sender=user).last()
        if message:
            items.append({'kind': 'chat', 'date': message.created_at, 'user': message.sender,
                          'url': reverse('chat_detail', args=[chat.id])})

    items.sort(key=lambda item: item['date'], reverse=True)
    return items[:30]


@login_required
def home(request):
    context = {
        'title': _('Inicio'), 'section': 'home',
        'posts': Post.objects.all(),
        'pets': Pet.objects.filter(for_adoption=True).exclude(owner=request.user)[:3],
        'people': User.objects.filter(is_active=True).exclude(id=request.user.id).order_by('-date_joined')[:3],
    }
    return render(request, 'home.html', context)


@login_required
def search(request):
    query = request.GET.get('q', '').strip()
    kind = request.GET.get('type', 'users')
    users, pets, posts = [], [], []

    # Busca en personas, mascotas en adopción y publicaciones
    if query:
        users = User.objects.filter(is_active=True).exclude(id=request.user.id).filter(
            Q(username__icontains=query) | Q(profile__full_name__icontains=query) | Q(profile__city__icontains=query))
        pets = Pet.objects.filter(for_adoption=True).filter(Q(name__icontains=query) | Q(location__icontains=query))
        posts = Post.objects.filter(text__icontains=query)

    context = {
        'title': _('Resultados para "%(query)s"') % {'query': query} if query else _('Buscar'),
        'section': 'search', 'query': query, 'kind': kind, 'users': users, 'pets': pets, 'posts': posts,
    }
    return render(request, 'search.html', context)


@login_required
def adoption_feed(request):
    # Mascotas en adopción de los demás usuarios
    pets = Pet.objects.filter(for_adoption=True).exclude(owner=request.user)
    context = {'title': _('Adopción'), 'section': 'adoption', 'pets': pets}
    return render(request, 'adoption_feed.html', context)


@login_required
def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, for_adoption=True)
    context = {
        'title': f"{pet.name} · {_('Adopción')}", 'section': 'adoption', 'pet': pet,
        'application': Application.objects.filter(pet=pet, applicant=request.user).first(),
        # Adopciones que el dueño entregó, la mascota ya no es suya
        'owner_adoptions': Application.objects.filter(status='accepted', chat__members=pet.owner)
                                              .exclude(applicant=pet.owner).count(),
    }
    return render(request, 'pet_detail.html', context)


@login_required
def application_form(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, for_adoption=True)

    # No se puede postular a su propia mascota ni dos veces a la misma
    if pet.owner == request.user or Application.objects.filter(pet=pet, applicant=request.user).exists():
        return redirect('pet_detail', pet_id=pet.id)

    form = ApplicationForm(request.POST or None)
    options = request.POST.getlist('options')
    if request.method == 'POST' and form.is_valid():
        application = form.save(commit=False)
        application.pet = pet
        application.applicant = request.user
        application.save()

        # Se abre un chat con el dueño y el mensaje de la postulación va de primero
        text = application.message
        if options:
            text += '\n\n' + ', '.join(str(HOME_OPTIONS[option]) for option in options if option in HOME_OPTIONS)
        chat = Chat.objects.create(application=application)
        chat.members.add(pet.owner, request.user)
        Message.objects.create(chat=chat, sender=request.user, text=text)
        return redirect(reverse('pet_detail', args=[pet.id]) + '?postulacion=enviada')

    context = {
        'title': _('Postularte para adoptar a %(pet)s') % {'pet': pet.name},
        'section': 'adoption', 'modal': True, 'pet': pet, 'form': form, 'options': options,
    }
    return render(request, 'application_form.html', context)


@login_required
def chat_list(request):
    chats = get_chats(request.user)

    # En escritorio se ve abierta la conversación más reciente
    chat = chats[0] if chats else None
    context = {
        'title': _('Mensajes'), 'section': 'messages', 'chats': chats, 'chat': chat,
        'other': chat.other if chat else None,
    }
    return render(request, 'chat_list.html', context)


@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, members=request.user)
    form = MessageForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        message = form.save(commit=False)
        message.chat = chat
        message.sender = request.user
        message.save()
        return redirect('chat_detail', chat_id=chat.id)

    other = chat.other_member(request.user)
    context = {
        'title': _('Conversación con %(name)s') % {'name': other.display_name()}, 'section': 'messages',
        'chat': chat, 'other': other, 'chats': get_chats(request.user), 'form': form,
    }
    return render(request, 'chat_detail.html', context)


@login_required
@require_POST
def application_cancel(request, chat_id):
    # Solo quien se postuló puede cancelar
    chat = get_object_or_404(Chat, id=chat_id, application__applicant=request.user, application__status='pending')
    chat.application.status = 'cancelled'
    chat.application.save()
    return redirect('chat_detail', chat_id=chat.id)


@login_required
@require_POST
def application_accept(request, chat_id):
    # Solo el dueño acepta y la mascota pasa al adoptante
    chat = get_object_or_404(Chat, id=chat_id, application__pet__owner=request.user, application__status='pending')
    application = chat.application
    application.status = 'accepted'
    application.save()
    pet = application.pet
    pet.owner = application.applicant
    pet.for_adoption = False
    pet.save()

    # Las demás postulaciones a esa mascota quedan rechazadas
    Application.objects.filter(pet=pet, status='pending').update(status='rejected')
    return redirect('chat_detail', chat_id=chat.id)


@login_required
@require_POST
def application_reject(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, application__pet__owner=request.user, application__status='pending')
    chat.application.status = 'rejected'
    chat.application.save()
    return redirect('chat_detail', chat_id=chat.id)


@login_required
def notifications(request):
    items = build_notifications(request.user)

    # Se agrupan en hoy, ayer y antes
    today = timezone.localdate()
    groups = {'today': [], 'yesterday': [], 'before': []}
    for item in items:
        day = timezone.localtime(item['date']).date()
        if day == today:
            groups['today'].append(item)
        elif day == today - timedelta(days=1):
            groups['yesterday'].append(item)
        else:
            groups['before'].append(item)

    context = {'title': _('Notificaciones'), 'section': 'notifications', 'groups': groups, 'has_items': bool(items)}
    return render(request, 'notifications.html', context)


@login_required
def my_profile(request):
    context = {
        'title': _('Mi perfil'), 'section': 'profile', 'pets': request.user.pets.all(),
        'applications': request.user.applications.all(),
        'posts': Post.objects.filter(author=request.user),
    }
    return render(request, 'my_profile.html', context)


@login_required
def account_settings(request):
    context = {'title': _('Ajustes'), 'section': 'profile'}
    return render(request, 'account_settings.html', context)


@login_required
def pet_profile(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    context = {'title': f"{pet.name} · {_('Mis mascotas')}", 'section': 'profile', 'pet': pet}
    return render(request, 'pet_profile.html', context)


@login_required
def pet_create(request):
    return pet_form(request, Pet(owner=request.user), _('Nueva mascota'))


@login_required
def pet_edit(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    return pet_form(request, pet, _('Editar a %(name)s') % {'name': pet.name})


def pet_form(request, pet, title):
    # Crear y editar usan el mismo formulario
    form = PetForm(request.POST or None, request.FILES or None, instance=pet)
    if request.method == 'POST':
        temperament = request.POST.getlist('temperament')
        if form.is_valid():
            pet = form.save(commit=False)
            pet.temperament = ','.join(temperament)
            pet.save()
            return redirect('pet_profile', pet_id=pet.id)
    else:
        temperament = pet.temperament.split(',')

    context = {'title': title, 'section': 'profile', 'pet': pet, 'form': form, 'temperament': temperament}
    return render(request, 'pet_edit.html', context)


@login_required
@require_POST
def pet_delete(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    pet.delete()
    return redirect('my_profile')


@login_required
def user_profile(request, user_id):
    account = get_object_or_404(User, id=user_id, is_active=True)
    if account == request.user:
        return redirect('my_profile')

    context = {
        'title': account.display_name(), 'section': 'search', 'account': account, 'pets': account.pets.all(),
        'posts': Post.objects.filter(author=account),
    }
    return render(request, 'user_profile.html', context)


@login_required
def post_create(request):
    context = {'title': _('Nueva publicación'), 'section': 'home', 'modal': True}
    return render(request, 'post_create.html', context)


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {'title': _('Publicación de %(name)s') % {'name': post.author.display_name()}, 'section': 'home',
               'post': post}
    return render(request, 'post_detail.html', context)


@login_required
def report(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {'title': _('Reportar publicación'), 'section': 'home', 'modal': True, 'post': post}
    return render(request, 'report.html', context)


@login_required
def report_account(request, user_id):
    account = get_object_or_404(User, id=user_id, is_active=True)
    context = {'title': _('Reportar cuenta'), 'section': 'search', 'modal': True, 'account': account}
    return render(request, 'report.html', context)


# Solo entra el rol administrador
@login_required
@permission_required('SecurityApp.moderate_content', raise_exception=True)
def admin_panel(request):
    month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    context = {
        'title': _('Panel de administración'),
        'users': User.objects.annotate(pets_count=Count('pets')).order_by('-date_joined')[:20],
        'active_users': User.objects.filter(is_active=True).count(),
        'new_users': User.objects.filter(date_joined__gte=month_start).count(),
        'pets_count': Pet.objects.count(),
        'new_pets': Pet.objects.filter(created_at__gte=month_start).count(),
        'adoptions': Application.objects.filter(status='accepted').count(),
        'applications_month': Application.objects.filter(created_at__gte=month_start).count(),
    }
    return render(request, 'admin_panel.html', context)


@login_required
@permission_required('SecurityApp.ban_user', raise_exception=True)
@require_POST
def user_ban(request, user_id):
    account = get_object_or_404(User, id=user_id)

    # Vetar o quitar el veto, el administrador no se puede vetar a sí mismo
    if account != request.user:
        account.is_active = not account.is_active
        account.save()
    return redirect('admin_panel')
