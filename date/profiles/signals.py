from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Relationship


@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Relationship)
def post_save_add_to_match(sender, instance, created, **kwargs):
    sender_ = instance.sender # наследование экземпляра класса Relationship
    receiver_ = instance.receiver
    if instance.status == 'accepted':
        sender_.match.add(receiver_.user)
        receiver_.match.add(sender_.user)
        sender_.save()
        receiver_.save()


@receiver(pre_delete, sender=Relationship)
def pre_delete_remove_from_match(sender, instance, **kwargs): # сигнал для удаления друг друга из друзей
    sender_ = instance.sender
    receiver_ = instance.receiver
    sender_.match.remove(receiver_.user) # выбираем именно user, так как связь в модели ManyToMany
    receiver_.match.remove(sender_.user)
    sender_.save()
    receiver_.save()
