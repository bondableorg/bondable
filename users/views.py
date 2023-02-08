from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from .models import BondableUser
from .permissions import IsOwnerOrReadOnly
from .serializers import BondableUserSerializer
from .pagination import CustomPagination


class ListCreateLocationAPIView(ListCreateAPIView):
    serializer_class = BondableUserSerializer
    queryset = BondableUser.objects.all()
    # permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)

    def perform_create(self, serializer):
        serializer.save()


class RetrieveUpdateDestroyLocationAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = BondableUserSerializer
    queryset = BondableUser.objects.all()





