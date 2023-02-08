from django.contrib.auth.models import User
from django.db import models


class BondableUser(User):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20)

    class Meta:
        ordering = ["name"]
