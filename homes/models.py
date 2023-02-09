from django.db import models
from users.models import BondableUser

# Create your models here.


class Home(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, blank=True, null=True)
    registered_beds = models.IntegerField(blank=True, null=True)
    effective_beds = models.IntegerField(blank=True, null=True)
    budget = models.IntegerField(blank=True, null=True)
    
    lead_contact = models.ForeignKey(
        BondableUser, on_delete=models.CASCADE, blank=True, null=True
    )
    users = models.ManyToManyField(BondableUser, related_name="locations", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class DayShift(models.Model):
    home = models.ForeignKey(Home, related_name="shifts", on_delete=models.CASCADE)
    day = models.DateField()
    occupancy = models.IntegerField(blank=True, null=True)
    occupancy_percent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    admissions_week_to_date = models.IntegerField(blank=True, null=True)
    discharges_week_to_date = models.IntegerField(blank=True, null=True)
    deaths_week_to_date = models.IntegerField(blank=True, null=True)
    live_enquiries = models.IntegerField(blank=True, null=True)
    hours_worked = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    hours_worked_from_home_in_last_24_hours = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )

    agency_hours_in_last_24_hours = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )

    agency_hours_in_last_24_hours_nurse = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    agency_hours_in_last_24_hours_senior_carer = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    agency_hours_in_last_24_hours_carer = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    incidents_in_last_24_hours = models.BooleanField(blank=True, null=True)
    ASPS_in_last_24_hours = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return f"{self.home.name} - {self.day}"
    class Meta:
        ordering = ["-id"]


class WeeklyShiftAggregate(models.Model):
    home = models.ForeignKey(
        Home, related_name="weekly_aggregates", on_delete=models.CASCADE
    )
    week_number = models.IntegerField()
    year = models.CharField(max_length=4)
    occupancy = models.IntegerField(blank=True, null=True)
    planned_admissions = models.IntegerField(blank=True, null=True)
    planned_discharges = models.IntegerField(blank=True, null=True)
    expected_end_of_life = models.IntegerField(blank=True, null=True)
    agency_nurse_hours = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    agency_senior_carer_hours = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    agency_carer_hours = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )

    def __str__(self):
        return f"{self.home.name} - week:{self.week_number} - year:{self.year}"

class MonthlyShiftAggregate(models.Model):
    home = models.ForeignKey(
        Home, related_name="monthly_aggregates", on_delete=models.CASCADE
    )
    month = models.CharField(max_length=12)
    year = models.CharField(max_length=4)
    occupancy = models.IntegerField(blank=True, null=True)
    nurse_hours = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    carer_hours = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )

    def __str__(self):
        return f"{self.home.name} - month:{self.month} - year:{self.year}"

    class Meta:
        ordering = ["-month"]
