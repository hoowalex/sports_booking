from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('trainer', 'Trainer'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

class Training(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField()
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_trainings')
    participants = models.ManyToManyField(User, related_name='joined_trainings', blank=True)
    max_participants = models.PositiveIntegerField(default=15, verbose_name="Максимум місць")

    def __str__(self):
        return self.title

