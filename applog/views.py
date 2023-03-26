import datetime
from django.http import JsonResponse
from django_filters import rest_framework as filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

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

