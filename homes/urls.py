from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListCreateLocationAPIView.as_view(), name='get_post_locations'),
    path('<int:pk>/', views.RetrieveUpdateDestroyLocationAPIView.as_view(), name='get_delete_update_location'),
    path('aggregates/<int:id>', views.get_aggregations, name='get_aggregations'),
]