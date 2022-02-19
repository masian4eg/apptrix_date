from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile, Relationship
from .forms import ProfileModelForm
from django.views.generic import DetailView, ListView
from django.contrib.auth.models import User
from django.db.models import Q


def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }

    return render(request, 'profiles/myprofile.html', context)


class ProfileView(DetailView):
    model = Profile
    template_name = 'profile_client.html'
    context_object_name = 'profile_client'
    queryset = Profile.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def match_received_view(request): # вьюха списка полученных запрос в друзья
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitations_received(profile)
    result = list(map(lambda x: x.sender, qs)) # lambda функция для создания списка профилей, сделавших запрос на добвление в друзья
    is_empty = False
    if len(result) == 0:
        is_empty = True

    context = {
        'qs': result,
        'is_empty': is_empty,
    }  # список из профилей сделавших запрос на добавление в друзья (без указания получателя (себя)), если никого - is_empty

    return render(request, 'profiles/my_match.html', context)


def accept_match(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('profiles:my-match-view')


def reject_match(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('profiles:my-match-view')


class ProfileListView(ListView): # список отправленных и присланных запрос на добавление в друзья
    model = Profile
    template_name = 'profiles/profile_list.html'
    context_object_name = 'qs'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user) # iexact возвращает юзернейм без учета регистра знаков
        profile = Profile.objects.get(user=user) # получаем профиль юзера
        rel_r = Relationship.objects.filter(sender=profile) # список отправленных запросов на добавление в друзья
        rel_s = Relationship.objects.filter(receiver=profile) # список принятых запросов на добавление в друзья
        rel_receiver = []
        rel_sender = [] # пустые списки для добавления в них отправленных и принятых запросов в друзья

        for item in rel_r:
            rel_receiver.append(item.receiver.user)

        for item in rel_s:
            rel_sender.append(item.sender.user)

        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context


def send_match(request): # метод отправляет запрос на добавление в друзья другим пользователям
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:all-profiles-view')


def remove_match(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:all-profiles-view')
