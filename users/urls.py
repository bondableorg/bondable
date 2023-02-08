from django.urls import path
from . import views


urlpatterns = [
    path('', views.ListCreateLocationAPIView.as_view(), name='get_post_users'),
    path('<int:pk>/', views.RetrieveUpdateDestroyLocationAPIView.as_view(), name='get_delete_update_user'),
]