from django.db import models
from django.contrib.auth.models import User

class DesignRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    title = models.CharField(max_length=100, verbose_name='Kitchen')
    description = models.TextField(verbose_name='Design preferences')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Data create')

    def __str__(self):
        return f"{self.title} от {self.user.username}"

# Create your models here.
