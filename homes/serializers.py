from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (
    BondableUser,
    Home,
    DayShift,
    WeeklyShiftAggregate,
    MonthlyShiftAggregate,
)


class HomeSerializer(serializers.ModelSerializer):
    # creator = serializers.ReadOnlyField(source="creator.username")

    class Meta:
        model = Home
        fields = ("name", "address", "budget",)

class DayShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayShift
        fields = (
            "location",
            "day",
            "occupancy",
            "active_beds",
            "admissions",
            "discharges",
        )

class WeeklyShiftAggregateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyShiftAggregate
        fields = (
            "home",
            "week_number",
            "year",
            "planned_admissions",
            "planned_discharges",
            "expected_end_of_life",
            "agency_nurse_hours",
            "agency_senior_carer_hours",
            "agency_carer_hours",
        )

class MonthlyShiftAggregateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyShiftAggregate
        fields = (
            "home",
            "month",
            "year",
            "planned_admissions",
            "planned_discharges",
            "expected_end_of_life",
            "agency_nurse_hours",
            "agency_senior_carer_hours",
            "agency_carer_hours",
        )


