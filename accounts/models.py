from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class DesignRequest(models.Model):
    STATUS_CHOICES = (
    ('новая', 'Новая'),
    ('в процессе', 'В процессе'),
    ('сделано', 'Сделано'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Категория')
    title = models.CharField(max_length=100, verbose_name='Комната')
    description = models.TextField(verbose_name='Дизайнерские предпочтения')
    photo = models.ImageField(upload_to='requests/', verbose_name='Фото комнаты или её план')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    comment =models.TextField(blank=True, null=True,verbose_name='Комментарии')
    design_image = models.ImageField(upload_to='requests/', blank=True, null=True, verbose_name='Фотография комнаты или её плана')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def clean(self):
        if self.pk:
            old_status = DesignRequest.objects.get(pk=self.pk).status
            if old_status != self.status and self.status == 'Новая':
                raise ValidationError('Новый статус')

        if self.status == 'В процессе' and not self.comment:
            raise ValidationError('Статус в процессе')

        if self.status == 'Сделано' and not self.design_image:
            raise ValidationError('Готовый статус')

    def __str__(self):
        return f"{self.title} от {self.user.username}"

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Именованная категория')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

# Create your models here.
