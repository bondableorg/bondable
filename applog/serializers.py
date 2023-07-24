from django.contrib.auth.models import User
from rest_framework import serializers
from homes.models import Home

from users.models import BondableUser

from .models import AppLog


class AppLogSerializer(serializers.ModelSerializer):
    home = serializers.CharField(max_length=100)
    in_charge = serializers.CharField(max_length=100)
    appuser = serializers.CharField(max_length=100)

    class Meta:
        model = AppLog
        fields = ["app", "home", "in_charge", "appuser", "description", "data", "created"]
        depth = 1

    def create(self, validated_data):
        # get the user from the request
        print(validated_data)
        in_charge = validated_data.pop("in_charge")
        home = validated_data.pop("home")
        appuser = validated_data.pop("appuser")
        # create the applog
        return AppLog.objects.create(
            app=validated_data["app"],
            home=Home.objects.get(name=home),
            in_charge=BondableUser.objects.get(username=in_charge),
            appuser=BondableUser.objects.get(username=appuser),
            created=validated_data["created"],
            description=validated_data["description"],
            data=validated_data["data"],
        )


