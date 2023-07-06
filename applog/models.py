from django.db import models
from users.models import BondableUser
from homes.models import Home


# create applog models here
class AppLog(models.Model):
    app = models.CharField(max_length=100)
    home = models.ForeignKey(Home, on_delete=models.CASCADE)
    in_charge = models.ForeignKey(BondableUser, on_delete=models.CASCADE, null=True, blank=True)
    appuser = models.ForeignKey(BondableUser, related_name="userapplogs", on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField()
    description = models.CharField(max_length=100)
    data = models.JSONField()

    def __str__(self):
        return f"{self.home.name} - {self.appuser.name}"

    class Meta:
        ordering = ["-created"]

