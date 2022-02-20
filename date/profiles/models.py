from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.conf import settings
from django.db.models import Q
from django.core.mail import send_mail


class ProfileManager(models.Manager):

    def get_all_profiles_to_match(self, sender):
        profiles = Profile.objects.all().exclude(user=sender) # все профили кроме отправителя
        profile = Profile.objects.get(user=sender) # отправитель
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile)) # фильтр отправитель or получатель

        accepted = ([])
        for rel in qs:
            if rel.status == 'accepted': # заносим в список accepted профили подтвержденных друзей
                accepted.add(rel.receiver)
                accepted.add(rel.sender)

        available = [profile for profile in profiles if profile not in accepted]
        # если профиля нет в общем списке профилей, то добавляем его в список available
        return available

    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me) # все профили кроме себя
        return profiles


class Profile(models.Model):
    GENDER_CHOICES = (
        ('М', 'муж'),
        ('Ж', 'жен'),
    )

    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')
    email = models.EmailField(max_length=200, blank=True)
    match = models.ManyToManyField(User, blank=True, related_name='match')

    objects = ProfileManager()

    def save(self, *args, **kwargs):
        super().save()
        if not self.avatar:
            return
        img = Image.open(self.avatar.path)
        width, height = img.size
        watermark = Image.open(settings.MEDIA_ROOT + '/watermark.png')
        watermark.thumbnail((200, 200))
        mark_width, mark_height = watermark.size
        paste_mask = watermark.split()[0]
        x = width - mark_width - 5
        y = height - mark_height - 5
        img.paste(watermark, (x, y), paste_mask)
        img.save(self.avatar.path)

    def __str__(self):
        return f'{self.user} {self.email}'


class RelationshipManager(models.Manager):
    def invitations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        return qs


class Relationship(models.Model):
    STATUS_CHOICES = (
        ('send', 'Симпатия'),
        ('accepted', 'Взаимная симпатия')
    )

    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)

    objects = RelationshipManager()

    def send_match(receiver, sender):
        subject = 'У вас есть пара!'
        message = f'Вы понравились {sender.first_name}!  Почта участника: {sender.email}'
        admin_email = settings.EMAIL
        user_email = [receiver.email]
        return send_mail(subject, message, admin_email, user_email)

    def __str__(self):
        return f'{self.sender}-{self.receiver}-{self.status}'
