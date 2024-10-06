from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ROLE_CHOICES = (
        ('mentor', 'Mentor'),
        ('learner', 'Learner'),
    )
    role = models.CharField(max_length=20, choices=[('mentor', 'Mentor'), ('learner', 'Learner')])
    id_number = models.PositiveIntegerField(unique=True)  # Unique ID for both Mentor and Learner

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Learner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional student fields if needed


class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional mentor fields if needed


class CustomUser(AbstractUser):
    # Additional fields for CustomUser can be defined here

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    # Override groups and user_permissions to avoid conflicts
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Use a custom related name
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions_set',  # Use a custom related name
        blank=True,
        help_text=('Specific permissions for this user.'),
        verbose_name='user permissions',
    )