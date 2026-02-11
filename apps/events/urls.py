from django.urls import path

from .views import EventsViewSet


urlpatterns = [
    path('', EventsViewSet.as_view({'get': 'list', 'post': 'create'}), name='events-list-create'),
    path('<int:pk>/', EventsViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='events-detail'),
]