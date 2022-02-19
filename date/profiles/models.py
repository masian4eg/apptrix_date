from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.conf import settings


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
