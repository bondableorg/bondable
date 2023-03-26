import datetime
from django.http import JsonResponse
from django_filters import rest_framework as filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .models import AppLog
# from .permissions import IsOwnerOrReadOnly
from .serializers import AppLogSerializer

# from .pagination import CustomPagination
# from .filters import LocationFilter


class ListCreateAppLogAPIView(ListCreateAPIView):
    serializer_class = AppLogSerializer
    queryset = AppLog.objects.all()
    # permission_classes = [IsAuthenticated]
    # pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)

    def perform_create(self, serializer):
        serializer.save()


class RetrieveUpdateDestroyAppLogAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AppLogSerializer
    queryset = AppLog.objects.all()
    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

