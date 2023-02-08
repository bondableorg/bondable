from django.contrib import admin

from homes.models import MonthlyShiftAggregate, WeeklyShiftAggregate, DayShift, Home

# Register your models here.
admin.site.register(MonthlyShiftAggregate)
admin.site.register(WeeklyShiftAggregate)
admin.site.register(DayShift)
admin.site.register(Home)