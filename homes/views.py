import json
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django_filters import rest_framework as filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from scripts.email_service import SendDynamic

from .models import DayShift, Home, MonthlyShiftAggregate, WeeklyShiftAggregate

# from .permissions import IsOwnerOrReadOnly
from .serializers import HomeSerializer

# from .pagination import CustomPagination
# from .filters import LocationFilter


class ListCreateLocationAPIView(ListCreateAPIView):
    serializer_class = HomeSerializer
    queryset = Home.objects.all()
    # permission_classes = [IsAuthenticated]
    # pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    # filterset_class = LocationFilter

    def perform_create(self, serializer):
        serializer.save()


class RetrieveUpdateDestroyLocationAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = HomeSerializer
    queryset = Home.objects.all()
    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


def get_aggregations(request, id):
    home = Home.objects.get(id=id)
    week_number = WeeklyShiftAggregate.objects.all()[0].week_number
    month = MonthlyShiftAggregate.objects.all()[0].month
    day = DayShift.objects.all()[0].day
    week_data = WeeklyShiftAggregate.objects.get(
        year="2023", week_number=week_number, home=home
    )
    month_data = MonthlyShiftAggregate.objects.get(
        year="2023",
        month=month,
        home=home,
    )
    day_data = DayShift.objects.get(day=day, home=home)
    total_hours_worked = day_data.hours_worked

    last_7_days = DayShift.objects.filter(
        day__gte=datetime.date.today() - datetime.timedelta(days=7), home=home
    )

    last_7_days_occupancy = {
        "dates": [d.day for d in last_7_days],
        "occupancy": [day.occupancy for day in last_7_days],
    }

    last_7_days_admissions = {
        "dates": [d.day for d in last_7_days],
        "admissions": [day.admissions_week_to_date for day in last_7_days],
    }

    last_7_days_discharges = {
        "dates": [d.day for d in last_7_days],
        "discharges": [day.discharges_week_to_date for day in last_7_days],
    }

    last_7_days_deaths = {
        "dates": [d.day for d in last_7_days],
        "deaths": [day.deaths_week_to_date for day in last_7_days],
    }

    last_9_months = MonthlyShiftAggregate.objects.filter(home=home).order_by("-month")[
        :9
    ]

    last_9_months_occupancy = {
        "months": [month.month for month in last_9_months],
        "occupancy": [month.occupancy for month in last_9_months],
    }

    return JsonResponse(
        {
            "home_name": home.name,
            "ops_mgr": home.lead_contact.name,
            "todays_occupancy": day_data.occupancy,
            "this_weeks_occupancy": week_data.occupancy,
            "this_months_occupancy": month_data.occupancy,
            "total_hours_worked": total_hours_worked,
            "last_7_days_occupancy": last_7_days_occupancy,
            "last_7_days_admissions": last_7_days_admissions,
            "last_7_days_discharges": last_7_days_discharges,
            "last_7_days_deaths": last_7_days_deaths,
            "last_9_months_occupancy": last_9_months_occupancy,
            "predictions": {
                "planned_admissions": week_data.planned_admissions,
                "planned_discharges": week_data.planned_discharges,
                "expected_end_of_life": week_data.expected_end_of_life,
            },
        }
    )


@csrf_exempt
def send_email(request):
    if request.method == "POST":
        print(request.body)
        data = json.loads(request.body)
        SendDynamic(data)
        return JsonResponse({"message": "Email sent successfully"}, status=200)
    return JsonResponse({"message": "Invalid request"}, status=400)
