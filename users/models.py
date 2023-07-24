from django.contrib.auth.models import User
from django.db import models


class BondableUser(User):
    type = models.CharField(max_length=20)

    class Meta:
        ordering = ["-date_joined"]
