from django.contrib.auth.models import User
from rest_framework import serializers

from homes.models import Home

from .models import BondableUser


class BondableUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = BondableUser
        fields = ("id", "username", "name", "email", "type",)

