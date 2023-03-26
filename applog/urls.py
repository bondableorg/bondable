from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListCreateAppLogAPIView.as_view(), name='get_post_applog'),
    path('<int:pk>/', views.RetrieveUpdateDestroyAppLogAPIView.as_view(), name='get_delete_update_applog'),
]