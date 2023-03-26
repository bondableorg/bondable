from django.db import models
from users.models import BondableUser
from homes.models import Home


# create applog models here
class AppLog(models.Model):
    app = models.CharField(max_length=100)
    home = models.ForeignKey(Home, related_name="applog", on_delete=models.CASCADE)
    user = models.ForeignKey(BondableUser, related_name="applog", on_delete=models.CASCADE)
    created = models.DateTimeField()
    description = models.CharField(max_length=100)
    data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.home.name} - {self.user.name}"

    class Meta:
        ordering = ["-created"]

