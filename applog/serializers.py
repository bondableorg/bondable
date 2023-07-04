from django.contrib.auth.models import User
from rest_framework import serializers

from .models import AppLog


class AppLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppLog
        fields = "__all__"
        depth = 1


