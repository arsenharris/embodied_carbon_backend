from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Custom user model extended with organisation name."""
    organization_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username