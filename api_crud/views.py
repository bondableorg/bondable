from django.shortcuts import render
from homes.models import Home, WeeklyShiftAggregate, MonthlyShiftAggregate, DayShift

def index(request):
    return render(request, 'dashboard.html', {})
