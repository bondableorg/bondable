from django.contrib import admin
from django.utils.html import format_html

from homes.models import (DayShift, Home, MonthlyShiftAggregate,
                          WeeklyShiftAggregate)

# Register your models here.
admin.site.register(MonthlyShiftAggregate)
admin.site.register(WeeklyShiftAggregate)
admin.site.register(DayShift)


class HomeAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "lead_contact",
        "address",
        "registered_beds",
        "effective_beds",
        "open_dashboard",
    ]

    def open_dashboard(self, item):
        return format_html(
            f'<a href="/dashboard/{item.id}" target="_blank" class="button" '
            f'id="id_admin_dash{item.id}">Dashboard</a>'
        )

    open_dashboard.short_description = "Dashboard"


admin.site.register(Home, HomeAdmin)
