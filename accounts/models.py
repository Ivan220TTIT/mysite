from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class DesignRequest(models.Model):
    STATUS_CHOICES = (
    ('new', 'New'),
    ('in_progress', 'In Progress'),
    ('done', 'Done'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Category')
    title = models.CharField(max_length=100, verbose_name='Kitchen')
    description = models.TextField(verbose_name='Design preferences')
    photo = models.ImageField(upload_to='requests/', verbose_name='Photo of the room or a plan')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Status')
    comment =models.TextField(blank=True, null=True,verbose_name='Comments')
    design_image = models.ImageField(upload_to='requests/', blank=True, null=True, verbose_name='Image of the room or a plan')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Data create')

    def clean(self):
        if self.pk:
            old_status = DesignRequest.objects.get(pk=self.pk).status
            if old_status != self.status and self.status == 'new':
                raise ValidationError('Status is new')

        if self.status == 'in_progress' and not self.comment:
            raise ValidationError('Status is in_progress')

        if self.status == 'done' and not self.design_image:
            raise ValidationError('Status is done')

    def __str__(self):
        return f"{self.title} от {self.user.username}"

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Category name')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

# Create your models here.
